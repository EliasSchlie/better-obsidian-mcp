# better-obsidian-mcp

An MCP server for your Obsidian vault that reads files directly from disk — no Obsidian app required.

## Why not the Local REST API plugin?

The [Local REST API plugin](https://github.com/coddingtonbear/obsidian-local-rest-api) requires Obsidian to be running. This means it can't be used on a remote server, in CI, or when Obsidian is closed.

`better-obsidian-mcp` bypasses Obsidian entirely and reads your vault's markdown files directly. It works anywhere Python runs.

## Features

- **Read notes** — fetch any note's content by title
- **Auto-exposed resources** — drop `.md` files in `mcp_resources/` inside your vault and they're automatically available as MCP resources (useful for persistent context like instructions, templates, or reference docs)
- **Extensible** — add tools, resources, and prompts by dropping functions into `tools.py`, `resources.py`, or `prompts.py`

## MCP Tools

| Tool | Description |
|------|-------------|
| `read_note` | Returns the full content of a note, looked up by title (filename without `.md`) |

## MCP Resources

Any `.md` file placed in `<vault>/mcp_resources/` is automatically exposed as an MCP resource at `file://<name>/`. This is useful for injecting static context (e.g. instructions, personal facts, templates) into Claude sessions.

## Installation

**Requirements:** Python ≥ 3.13, [uv](https://docs.astral.sh/uv/)

```bash
git clone https://github.com/EliasSchlie/better-obsidian-mcp
cd better-obsidian-mcp
uv sync
```

## Configuration

Set the `vault_directory` environment variable to the absolute path of your Obsidian vault.

### Claude Desktop (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "better-obsidian-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/better-obsidian-mcp", "run", "src/better_obsidian_mcp/server.py"],
      "env": {
        "vault_directory": "/path/to/your/obsidian/vault"
      }
    }
  }
}
```

### Remote server (stdio via SSH)

Because there's no dependency on the Obsidian app, you can run this on any machine that has access to your vault files — including a remote server over SSH.

## Extending

The server auto-discovers functions following naming conventions:

- **Tools** (`tools.py`): define `<name>_outer(*args, **kwargs)` returning an inner function
- **Resources** (`resources.py`): define `<name>_outer(*args, **kwargs)` returning `(func, uri)`
- **Prompts** (`prompts.py`): define `<name>_outer(*args, **kwargs)` returning `(func, prompt_name)`

See the existing examples in each file as a starting point.
