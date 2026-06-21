# bim-cli Claude Code Plugin

Claude Code plugin manifest for [bim-cli](https://bimcli.com) -- AEC tools for headless PDF
processing, flood/site lookups, and offline BIM tasks that run without Revit or any desktop
app open.

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

## Setup

1. **Install bim-cli** (if not already):

   ```powershell
   iwr -useb https://bimcli.com/install.ps1 | iex
   ```

   Verify: `bim describe --json` should list installed drivers.

2. **Add this plugin to Claude Code** via the Claude Code plugin directory, or manually:

   ```json
   {
     "mcpServers": {
       "bim-cli": {
         "type": "stdio",
         "command": "bim",
         "args": ["mcp"]
       }
     }
   }
   ```

   Add this to your Claude Code MCP configuration (`.mcp.json` in your project root, or
   via Claude Code settings).

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

Full privacy policy: [https://mcp.bimcli.com/privacy](https://mcp.bimcli.com/privacy)

## More

- bim-cli docs: [https://bimcli.com](https://bimcli.com)
- MCP listing home: [https://mcp.bimcli.com](https://mcp.bimcli.com)
- Capability schema: `bim describe --json`
- Issues: [https://bimcli.com](https://bimcli.com)
