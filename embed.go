package agentskills

import "embed"

// FS contains the approved Wave AI skill sources embedded into the web binary.
//
//go:embed skills/**
var FS embed.FS
