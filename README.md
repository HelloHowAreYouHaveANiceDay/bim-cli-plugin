# bim-cli Claude Code Plugin

Claude Code plugin manifest for [bim-cli](https://bimcli.com) -- headless Revit export, PDF
batch export, flood/site data lookup, and offline AEC tasks. Runs from your AI assistant
without Revit or any desktop app open.

**Windows-only.** bim-cli is a Windows-only CLI. This plugin requires a Windows machine with
bim-cli installed.

## What this plugin does

Exposes all installed bim-cli verbs as MCP tools in Claude Code. Each tool maps to a
`bim <format> <verb>` command running locally on your machine. Example tools:

- `bim_pdf_text` -- extract text from a PDF without opening it
- `bim_pdf_stamp` -- apply a Bates stamp or watermark to PDF pages
- `bim_pdf_split`, `bim_pdf_merge` -- split or combine PDF files
- `bim_site_flood_lookup` -- flood zone lookup by address or coordinates
- `bim_blender_convert` -- convert IFC/FBX/glTF headlessly

The tool list is generated dynamically from `bim describe --json` -- adding a new bim-cli
driver or verb makes it available automatically.

## About this plugin repo

This repository contains **only manifest files** (JSON and Markdown). It contains:

- No executable code
- No telemetry of its own
- No secrets or credentials
- No network calls

All execution is local: the plugin simply tells Claude Code how to launch the already-installed
`bim` binary as a local stdio MCP server (`bim mcp`). Nothing runs in the cloud.

## Setup

1. **Install bim-cli** (Windows, run in PowerShell):

   ```powershell
   iwr -useb https://bimcli.com/install.ps1 | iex
   ```

   Verify: `bim describe --json` should list installed drivers.

2. **Add this plugin to Claude Code** via the Claude Code plugin directory, or manually add
   the following to your `.mcp.json` in your project root (or via Claude Code settings):

   ```json
   {
     "mcpServers": {
       "bim": {
         "type": "stdio",
         "command": "bim",
         "args": ["mcp"]
       }
     }
   }
   ```

3. Restart Claude Code. Verify with `bim doctor` that installed drivers are healthy.

## Privacy Policy

bim-cli runs entirely on your local machine. The MCP server (`bim mcp`) does not make
network calls beyond what the individual bim-cli verbs themselves make (e.g. a flood
lookup calls a public FEMA/NFHL endpoint; a PDF operation makes no network calls at all).

**What leaves your machine:**

- Optional anonymous telemetry: verb shape, bim version, OS, success/error kind, latency.
  No file paths, addresses, document content, or user identity are ever sent.
  Set `DO_NOT_TRACK=1` or `BIM_TELEMETRY=0` to opt out entirely.
- Verb-specific network calls declared in `bim describe --json` under each verb's
  `requires` field (e.g. `network:host` for flood lookups).

**What never leaves your machine:**

- Document content (PDF pages, IFC geometry, Revit models).
- File paths or filenames.
- User identity or any personal data.
- MCP argument values.

Full privacy policy: [https://bimcli.com/privacy](https://bimcli.com/privacy)

## License

The files in this repository (the plugin manifest and MCP server declaration) are released
under the MIT License. See [LICENSE](LICENSE).

The MIT License covers only the manifest files in this repo. The bim-cli binary itself is
proprietary software; its license is separate and can be found at
[https://bimcli.com](https://bimcli.com).

## More

- bim-cli docs: [https://bimcli.com](https://bimcli.com)
- MCP listing home: [https://mcp.bimcli.com](https://mcp.bimcli.com)
- Capability schema: `bim describe --json`
- Issues: [https://github.com/HelloHowAreYouHaveANiceDay/bim-cli-plugin/issues](https://github.com/HelloHowAreYouHaveANiceDay/bim-cli-plugin/issues)
