# bim-cli Plugin Directory Submission Package

**Status:** Ready for human submission — prerequisites verified 2026-06-26.

---

## Prerequisites checklist (all verified)

- [x] `bim mcp` works as a stdio MCP server (`bim describe --json` lists installed verbs; `bim mcp` launches them as MCP tools)
- [x] `HelloHowAreYouHaveANiceDay/bim-cli-plugin` is public with valid `.claude-plugin/plugin.json` + `.mcp.json`
- [x] Privacy policy live at `https://mcp.bimcli.com/privacy` (200) and `https://bimcli.com/privacy/` (200)
- [x] `plugin.json` `privacy_policy` field points to `https://mcp.bimcli.com/privacy`

---

## Copy-paste submission inputs

| Field | Value |
|---|---|
| **Plugin name** | `bim-cli` |
| **Publisher / author** | `bimcli.com` |
| **Homepage** | `https://bimcli.com` |
| **Source repo** | `https://github.com/HelloHowAreYouHaveANiceDay/bim-cli-plugin` |
| **Privacy policy URL** | `https://mcp.bimcli.com/privacy` |
| **Category** | Development tools |
| **Tags** | `revit`, `aec`, `bim`, `pdf`, `windows`, `offline`, `construction` |
| **Contact / support** | `smalltigergroup@gmail.com` |
| **Platform** | Windows only |

### Short description (≤ 160 chars)

```
Headless Revit export, PDF batch ops, flood/site data — run from Claude Code, offline, no Revit session required.
```

### Long description

```
bim-cli gives Claude Code direct access to AEC workflows that no other MCP covers:
headless Revit sheet export and parameter writes (no running Revit session, no admin),
PDF batch stamping / Bates numbering / splitting / merging, FEMA flood zone lookup by
address or coordinates, and IFC/FBX/glTF conversion via Blender headlessly.

Every installed bim-cli driver and verb is exposed automatically as an MCP tool — the
server calls `bim describe --json` at startup and generates tools dynamically, so adding
a new bim-cli driver makes it available in Claude Code without any manifest update.

Runs entirely on your local Windows machine as a stdio process (`bim mcp`). Nothing
runs in the cloud. Document content, file paths, and Revit models never leave your machine.
Optional anonymous telemetry (verb shape, OS, success/error kind) is opt-out via
`DO_NOT_TRACK=1` or `BIM_TELEMETRY=0`.

Windows-only. Requires bim-cli v0.3.6+ installed (`iwr -useb https://bimcli.com/install.ps1 | iex`).
```

---

## Manifest validation (manual — no Anthropic linter published as of 2026-06-26)

- `name`: lowercase, no spaces ✓
- `version`: semver ✓
- `description`: < 200 chars ✓
- `homepage`: `https://bimcli.com` live 200 ✓
- `category`: `"development"` ✓
- `mcp`: `.mcp.json` present ✓
- `source`: public repo ✓
- `privacy_policy`: `https://mcp.bimcli.com/privacy` live 200 ✓
- `.mcp.json`: `"type": "stdio"`, `"command": "bim"`, `"args": ["mcp"]` ✓

---

## Human steps (exact)

These steps require a human because they involve accepting terms of service and making
publisher attestations. **Do not delegate to an autonomous worker.**

1. **Find the Claude Code plugin directory submission portal.**
   Look for "Submit a plugin" or "List your MCP server" in the Claude Code documentation
   at docs.anthropic.com or the Anthropic developer portal.

2. **Sign in** with the GitHub account owning `HelloHowAreYouHaveANiceDay/bim-cli-plugin`
   or the Anthropic developer account at `smalltigergroup@gmail.com`.

3. **Accept the publisher agreement / terms of service.**
   You are attesting as the individual publisher of bim-cli that:
   - You own `HelloHowAreYouHaveANiceDay/bim-cli-plugin` and are authorized to publish bim-cli.
   - The plugin meets the directory standards (local execution only, privacy policy live, no document content telemetry).
   - The privacy policy at `https://mcp.bimcli.com/privacy` is accurate.

4. **Fill the submission form** using the copy-paste inputs above.

5. **Submit.** Record the confirmation / reference number in a comment on DIM-51 in Linear.

6. **Close DIM-51** in Linear once the listing is confirmed received or goes live.

---

*Prepared by dim-factory 2026-06-26. Prerequisites verified; human steps documented.
The factory stops here — terms acceptance and attestation are human-only actions.*
