SHELL := /bin/bash

TARGET_AGENT_SKILLS_REPO ?= ../../agent-skills
SOURCE_AGENT_SKILLS_DIR := .
RSYNC_FLAGS := -av --delete --exclude='.git/' --exclude='.DS_Store'

.PHONY: help validate-agent-skills check-target-agent-skills-repo publish-agent-skills-dry-run publish-agent-skills

help:
	@printf '%s\n' \
		'Targets:' \
		'  make validate-agent-skills              Validate skill manifest and folders' \
		'  make publish-agent-skills-dry-run       Preview publishing to TARGET_AGENT_SKILLS_REPO' \
		'  make publish-agent-skills               Mirror this folder to TARGET_AGENT_SKILLS_REPO, preserving .git' \
		'' \
		'Variables:' \
		'  TARGET_AGENT_SKILLS_REPO=../../agent-skills  Override target repository path'

validate-agent-skills:
	@python3 scripts/validate_skills.py

check-target-agent-skills-repo:
	@test -d "$(TARGET_AGENT_SKILLS_REPO)" || { echo "TARGET_AGENT_SKILLS_REPO does not exist: $(TARGET_AGENT_SKILLS_REPO)"; exit 1; }
	@test -d "$(TARGET_AGENT_SKILLS_REPO)/.git" || { echo "TARGET_AGENT_SKILLS_REPO is not a git repository: $(TARGET_AGENT_SKILLS_REPO)"; exit 1; }

publish-agent-skills-dry-run: validate-agent-skills check-target-agent-skills-repo
	@echo "Dry run: $(SOURCE_AGENT_SKILLS_DIR)/ -> $(TARGET_AGENT_SKILLS_REPO)/"
	@rsync -n $(RSYNC_FLAGS) "$(SOURCE_AGENT_SKILLS_DIR)/" "$(TARGET_AGENT_SKILLS_REPO)/"

publish-agent-skills: validate-agent-skills check-target-agent-skills-repo
	@echo "Publishing: $(SOURCE_AGENT_SKILLS_DIR)/ -> $(TARGET_AGENT_SKILLS_REPO)/"
	@rsync $(RSYNC_FLAGS) "$(SOURCE_AGENT_SKILLS_DIR)/" "$(TARGET_AGENT_SKILLS_REPO)/"
	@echo "Done. Run: cd $(TARGET_AGENT_SKILLS_REPO) && git status --short"
