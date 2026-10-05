---
name: bim-cli
description: "Use when working with AEC files: PDF drawing sets, Revit, IFC, CAD. Drives the bim CLI."
version: 1.0.1
author: bimcli.com
license: MIT
platforms: [windows]
compatibility: "Windows 10/11 only. Requires bim-cli (https://bimcli.com) on PATH."
metadata:
  hermes:
    tags: [aec, bim, revit, pdf, ifc, autocad, rhino, sketchup, blender, construction, architecture]
    homepage: https://bimcli.com
---

# bim-cli

`bim` is an offline Windows CLI for AEC formats. One dispatcher routes `bim <format> <verb> [args]` to per-format driver binaries (pdf, revit, ifc, acad, rhino, sketchup, blender, image, excel, energy, code, site, ...). Every verb returns JSON on stdout, and the whole surface is self-describing.

## When to Use

- The user hands you a PDF drawing set, a Revit-exported PDF, or a PDF-BIM package: read text, find sheets, extract title blocks, split/merge/stamp/collect pages.
- The user wants something from a Revit model: export sheets to PDF, list sheets/elements, read schedules, run C# against the Revit API.
- The user has IFC, DWG, 3DM, SKP, glTF/FBX files to inspect or convert.
- Any task where you were about to write a one-off PDF/CAD/BIM parser. Check bim first.

## Step 0: is bim installed?

```bash
bim version --json
```

If the command is not found, **do not install it yourself**. Tell the user bim-cli is Windows-only and give them the installer to run in PowerShell:

```powershell
iwr -useb https://bimcli.com/install.ps1 | iex
```

It is per-user, needs no admin rights, and prints `BIM_INSTALLED_OK <version> <path>`. Re-running it upgrades. A shell that was already open needs its PATH refreshed: `export PATH="$PATH:$LOCALAPPDATA/bim-cli"` (bash) or `$env:Path += ";$env:LOCALAPPDATA\bim-cli"` (PowerShell).

Then, on first use in a session or whenever a verb fails unexpectedly, run `bim doctor --json`. Each failed check carries a `fix` field with the exact remediation command. `overall: "degraded"` is normal: it means some driver's host app (Revit, AutoCAD, Rhino, ...) is not installed, or a driver is broken, which only matters if you need that driver. A driver with an empty line in `bim describe --index` or an `error` in `bim version --json` is in that state; skip it or tell the user to re-run the installer.

## Procedure

1. **Find the verb. Never guess verb names.**
   ```bash
   bim describe --index                          # one line per driver: its verbs
   bim describe --driver pdf --verb page.split --json   # args, types, defaults for one verb
   ```
   `bim <format> <verb> --help` prints the same per-verb schema.
2. **Run it.** Multi-word verbs can be written dotted or spaced: `bim pdf page.split` and `bim pdf page split` are the same call. Flags come from the describe schema; positional args are marked `positional: true`.
3. **Check for an error object, not the exit code.** Failures are always `{"ok":false,"error":{"kind","message","hint","retriable"}}`, and can still exit 0. Successes vary by driver: some wrap as `{"ok":true,"result":...}`, others print the result object directly. Read `error.hint` on failure: it usually names the next command.
4. **Parse output with code.** Long operations stream NDJSON (one JSON object per line), often ending with a summary line. For anything bigger than a screenful, redirect to a file and parse it with Python or `jq`.
5. **Destructive verbs** write to `--out` (one file) or `--out-dir` (many files), never in place unless told to. Use `--dry-run` where the schema offers it before overwriting anything the user cares about.

## Two ways to call bim

- **Terminal (default).** Call `bim` directly from the shell. Cheapest in context, and it covers every verb.
- **MCP server.** `bim mcp` is a stdio MCP server that exposes every installed verb as a tool. That is several hundred tools, so only register it when the user wants bim as native tools:
  ```bash
  hermes mcp add bim --command bim --args mcp
  ```

## Driver docs

Each driver entry in `bim describe --json` has a `docs` URL (e.g. `https://bimcli.com/pdf/llms.txt`) with domain notes and workflow patterns. Fetch it when you start real work with a driver. Where the docs and `bim describe` disagree on a verb name or flag, **`bim describe` wins**: it is generated from the installed binary, while the web docs can lag a release.

Bundled notes for the two most common drivers:
- `references/pdf.md`: drawing sets, Revit PDFs, PDF-BIM packages.
- `references/revit.md`: connecting to Revit, exports, model queries, `exec`.

## Pitfalls

- **Pass Windows paths in forward-slash form** (`C:/proj/set.pdf`). Native bim binaries do not understand MSYS `/c/...` paths from git-bash.
- **Host-app drivers need the app.** revit, acad, rhino, sketchup and blender drive an installed desktop app; `bim doctor --json` shows which are usable. pdf, ifc, image and the other file drivers need nothing else.
- **Long ops stream.** Revit launch/export and big PDF jobs emit NDJSON progress lines; wait for the final line instead of killing the process early. Run them in the background if your harness has a short command timeout.
- **Several Revit instances.** If more than one Revit is open, run `bim revit instances` and pin one with `--instance <id>`, otherwise bim picks the newest year and only warns on stderr.

## Reporting friction

When a verb you expected does not exist, an error message was unclear, or you had to fall back to a workaround, send it to the maintainers:

```bash
bim feedback --note "<what you were trying to do and what happened>"
```

It scrubs paths and content and prints exactly what was sent. Mention it to the user when the friction was theirs.

## Verification

Before telling the user a task is done, re-read the output: `bim pdf info <out.pdf>` / `bim pdf pages <out.pdf>` for page counts and sizes, or the verb's own `result` for counts and written paths. Report the real numbers.
