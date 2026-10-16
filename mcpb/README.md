# MCP Registry listing (`com.bimcli/bim-cli`)

Listed at https://registry.modelcontextprotocol.io as `com.bimcli/bim-cli`, as an MCPB
bundle attached to a GitHub release of this repo (`mcpb-v<bim version>`).

The bundle is thin: `server/bim.exe` from the bim-cli release zip, run as `bim mcp`
with `BIM_HOME` pointed at the user's bim-cli install. Without an install it starts
with zero tools.

## Publish a new version

1. Download `bim-cli-windows-amd64.zip` for the tag from `https://dl.bimcli.com/<tag>/`,
   check it against the published `.sha256`, unzip it, and copy `bim.exe` into `<build>/server/`.
2. Copy `mcpb/manifest.json` to `<build>/`, bump `version`, then run
   `npx @anthropic-ai/mcpb validate manifest.json` and
   `npx @anthropic-ai/mcpb pack <build> bim-cli-<ver>.mcpb`.
3. Smoke test: unzip the bundle, pipe an MCP `initialize` + `tools/list` into
   `server/bim.exe mcp` with `BIM_HOME` set to a real install, and expect hundreds of tools.
4. `gh release create mcpb-v<ver> bim-cli-<ver>.mcpb`, then `sha256sum` the downloaded asset.
5. Update `server.json` (`version`, package `identifier`, `version`, `fileSha256`).
6. Run `mcp-publisher login http --domain bimcli.com --private-key <hex>`, then `mcp-publisher publish`.
   Namespace proof: `https://bimcli.com/.well-known/mcp-registry-auth`, served by
   bim-cli `workers/site.js`. The private Ed25519 key is held off-repo by the publisher.
