# Knowledge/Memory/Graph

## Session Start Hook

On new (empty user context) session, immediately:

1. `kg_register_session(cwd="<project root>")` — Register session, get session_id. Always pass the project root directory as `cwd` (e.g. `/home/user/myproject`).
2. `kg_read(session_id="<id>")` — Load graph: active nodes (id+gist), archived node IDs, edges, health stats.

If session is resumed, try `kg_sync(session_id)` first; if that fails, run the full startup sequence above.

### Server Not Reachable

If `kg_register_session` fails (connection refused / MCP server unavailable), offer to start it:
- Tell the user: "Memory server is not running. Start it with `kg-memory start`?"
- If user confirms, run `kg-memory start` via Bash, wait for it, then retry registration.
- If `kg-memory` command not found, suggest: `cd <plugin-dir>/server && ./manage_server.sh start`
- Continue the session normally even if memory remains unavailable — it's optional, not blocking.

## After Loading

Review user-level nodes for working style rules, pitfall patterns, confirmed preferences. Treat as defaults unless user overrides in-session.

When starting a task, glance at archived node IDs. If any feel related to what you're about to do — even loosely — recall them. Err on the side of recalling too many rather than too few. A wasted recall costs one tool call; missing relevant context costs the whole task.

## Details

For full API reference, capture rules, recall strategies, and graph maintenance: `/skill memory`
