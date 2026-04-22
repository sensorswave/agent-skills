#!/usr/bin/env node

import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  cpSync,
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  rmSync,
  statSync,
  symlinkSync,
} from 'node:fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const SKILLS_DIR = path.join(ROOT, 'skills');
const MANIFEST_PATH = path.join(SKILLS_DIR, 'manifest.json');
const USER_PLATFORMS = ['cursor', 'claude', 'codex'];

function fail(message) {
  console.error(`ERROR: ${message}`);
  process.exit(1);
}

function loadManifest() {
  if (!existsSync(MANIFEST_PATH)) {
    fail(`manifest 缺失: ${MANIFEST_PATH}`);
  }

  const data = JSON.parse(readFileSync(MANIFEST_PATH, 'utf8'));
  if (!Array.isArray(data.skills) || data.skills.length === 0) {
    fail('manifest.skills 不能为空');
  }
  return data.skills;
}

function resolveInstallSet(skills) {
  const byName = new Map(skills.map((item) => [item.name, item]));
  const resolved = [];
  const visited = new Set();
  const visiting = new Set();

  function visit(name) {
    if (visited.has(name)) {
      return;
    }
    if (visiting.has(name)) {
      fail(`manifest 依赖存在循环: ${name}`);
    }

    const item = byName.get(name);
    if (!item) {
      fail(`manifest 依赖未声明: ${name}`);
    }

    visiting.add(name);
    for (const dep of item.dependsOn || []) {
      visit(dep);
    }
    visiting.delete(name);

    visited.add(name);
    resolved.push(item);
  }

  for (const item of skills) {
    if (item.install !== false) {
      visit(item.name);
    }
  }

  return resolved;
}

function usage() {
  console.log(`Usage: wave-agent-skills [OPTIONS]

将 Wave Agent Skills 安装、卸载或校验到指定平台的 skills 目录。

Options:
  --cursor              安装到 Cursor（用户级 ~/.cursor/skills/）
  --claude              安装到 Claude Code（用户级 ~/.claude/skills/）
  --codex               安装到 Codex（用户级 ~/.codex/skills/）
  --all                 安装到所有平台（用户级）
  --project             安装到当前项目（默认 .cursor/skills/，如存在则追加 .claude/.codex）
  --target <dir>        安装到自定义 skills 目录
  --uninstall           从目标目录卸载技能集
  --check               校验目标目录是否完整包含 internal dependency
  --link                使用符号链接/Windows junction 安装，仅建议本地克隆仓库时使用
  --help, -h            显示帮助

Examples:
  npx github:sensorswave/agent-skills --codex
  npx github:sensorswave/agent-skills --all
  npx github:sensorswave/agent-skills --project
  npx github:sensorswave/agent-skills --check --codex
  npx github:sensorswave/agent-skills --target ./custom-skills
`);
}

function parseArgs(argv) {
  const options = {
    targets: [],
    project: false,
    uninstall: false,
    check: false,
    link: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    switch (arg) {
      case '--cursor':
      case '--claude':
      case '--codex':
        options.targets.push({
          type: 'user',
          platform: arg.slice(2),
        });
        break;
      case '--all':
        for (const platform of USER_PLATFORMS) {
          options.targets.push({
            type: 'user',
            platform,
          });
        }
        break;
      case '--project':
        options.project = true;
        break;
      case '--target': {
        const value = argv[index + 1];
        if (!value) {
          fail('--target 需要目录参数');
        }
        options.targets.push({
          type: 'custom',
          dir: value,
        });
        index += 1;
        break;
      }
      case '--uninstall':
        options.uninstall = true;
        break;
      case '--check':
        options.check = true;
        break;
      case '--link':
        options.link = true;
        break;
      case '--help':
      case '-h':
        usage();
        process.exit(0);
      default:
        fail(`未知选项: ${arg}`);
    }
  }

  if (options.uninstall && options.check) {
    fail('--uninstall 与 --check 不能同时使用');
  }

  if (!options.project && options.targets.length === 0) {
    fail('至少需要一个目标参数：--cursor / --claude / --codex / --all / --project / --target');
  }

  return options;
}

function resolveTargets(options) {
  const entries = [];

  for (const target of options.targets) {
    if (target.type === 'custom') {
      entries.push({
        label: `custom (${target.dir})`,
        dir: path.resolve(process.cwd(), target.dir),
      });
      continue;
    }

    const homeDir = path.join(os.homedir(), `.${target.platform}`, 'skills');
    entries.push({
      label: target.platform,
      dir: homeDir,
    });
  }

  if (options.project) {
    for (const platform of USER_PLATFORMS) {
      const baseDir = path.join(process.cwd(), `.${platform}`);
      if (platform === 'cursor' || existsSync(baseDir)) {
        entries.push({
          label: `${platform} (project)`,
          dir: path.join(baseDir, 'skills'),
        });
      }
    }
  }

  const deduped = new Map();
  for (const entry of entries) {
    deduped.set(entry.dir, entry);
  }
  return [...deduped.values()];
}

function ensureSkillSource(skill) {
  const skillDir = path.join(SKILLS_DIR, skill.dir);
  const skillFile = path.join(skillDir, skill.skillFile);
  const agentFile = path.join(skillDir, 'agents', 'openai.yaml');

  if (!existsSync(skillFile) || !existsSync(agentFile)) {
    fail(`skill 目录缺少必需文件: ${skillDir}`);
  }

  return skillDir;
}

function removePath(targetPath) {
  rmSync(targetPath, { recursive: true, force: true });
}

function installOneSkill(targetDir, skill, useLink) {
  const src = ensureSkillSource(skill);
  const dst = path.join(targetDir, skill.dir);

  if (existsSync(dst)) {
    const stat = lstatSync(dst);
    if (!stat.isDirectory() && !stat.isSymbolicLink()) {
      fail(`目标路径已被文件占用: ${dst}`);
    }
    removePath(dst);
  }

  if (useLink) {
    const linkType = process.platform === 'win32' ? 'junction' : 'dir';
    symlinkSync(path.resolve(src), dst, linkType);
    return 'linked';
  }

  cpSync(src, dst, {
    recursive: true,
    force: true,
  });
  return 'copied';
}

function uninstallOneSkill(targetDir, skill) {
  const dst = path.join(targetDir, skill.dir);
  if (!existsSync(dst)) {
    return false;
  }

  const stat = lstatSync(dst);
  if (!stat.isDirectory() && !stat.isSymbolicLink()) {
    fail(`目标路径已被文件占用，拒绝删除: ${dst}`);
  }

  removePath(dst);
  return true;
}

function checkTarget(targetDir, skills) {
  if (!existsSync(targetDir)) {
    return [`目标目录不存在: ${targetDir}`];
  }

  const missing = [];
  for (const skill of skills) {
    const skillDir = path.join(targetDir, skill.dir);
    if (!existsSync(skillDir) || !statSync(skillDir).isDirectory()) {
      missing.push(`${skill.dir}: 缺少目录 ${skillDir}`);
      continue;
    }

    const skillFile = path.join(skillDir, skill.skillFile);
    const agentFile = path.join(skillDir, 'agents', 'openai.yaml');
    if (!existsSync(skillFile)) {
      missing.push(`${skill.dir}: 缺少文件 ${skillFile}`);
    }
    if (!existsSync(agentFile)) {
      missing.push(`${skill.dir}: 缺少文件 ${agentFile}`);
    }
  }

  return missing;
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  const skills = resolveInstallSet(loadManifest());
  const targets = resolveTargets(options);

  if (targets.length === 0) {
    fail('没有可操作的目标目录');
  }

  if (options.check) {
    let hasError = false;
    for (const target of targets) {
      const missing = checkTarget(target.dir, skills);
      if (missing.length === 0) {
        console.log(`OK: ${target.label} 安装完整: ${target.dir}`);
        continue;
      }

      hasError = true;
      console.error(`校验失败: ${target.label} -> ${target.dir}`);
      for (const item of missing) {
        console.error(`- ${item}`);
      }
    }

    if (hasError) {
      process.exit(1);
    }
    return;
  }

  for (const target of targets) {
    mkdirSync(target.dir, { recursive: true });
    console.log(`${options.uninstall ? '处理卸载' : '处理安装'}: ${target.label}`);

    for (const skill of skills) {
      if (options.uninstall) {
        const removed = uninstallOneSkill(target.dir, skill);
        console.log(`  ${removed ? '✓' : '⟳'} ${skill.dir}${removed ? '' : ' (不存在，跳过)'}`);
        continue;
      }

      const mode = installOneSkill(target.dir, skill, options.link);
      const action = mode === 'linked' ? '↗' : '✓';
      console.log(`  ${action} ${skill.dir} (${mode})`);
    }

    console.log(`  → 完成: ${target.dir}`);
  }

  if (!options.uninstall && !options.link) {
    console.log('\n提示: 当前 CLI 默认使用复制安装，适合 npx / Windows / 无持久源码目录场景。');
  }
}

main();
