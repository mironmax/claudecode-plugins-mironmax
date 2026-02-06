# Retrieving Knowledge — Detailed Reference

## Automatic Loading

Every session starts with:
```
kg_read()              # Returns full active graph (both levels)
kg_register_session()  # Enables sync with other sessions
```

This gives you the current state. But the graph may be larger than what's loaded — some nodes are **archived** (hidden to save context space).

## When to Sync

Call `kg_sync(session_id)` when:
- Before making a decision that depends on shared knowledge
- When you suspect another session (or agent) has been active
- Periodically in long sessions (every 30+ minutes)
- After spawning subagents that write to the graph

Sync returns changes from other sessions since your session started.

## Memory Traces

When you see an edge pointing to a node not in your current view:

```
active-node --influenced-by--> archived-node-id
```

This is a **memory trace** — a hint that relevant archived knowledge exists.

### When to Follow

```
Is the archived node's ID relevant to your current task?
├─ YES → Recall it
├─ UNCLEAR → Consider the relationship type
│   ├─ Suggests importance? → Recall it
│   └─ Tangential? → Skip for now
└─ NO → Skip
```

### How to Recall

```
kg_recall(level="project", id="archived-node-id")
```

Node returns to active view with refreshed timestamp (protected from near-term re-archival).

**Recall liberally when:**
- Making architectural decisions
- Debugging something that "feels familiar"
- User asks "why did we do X?"
- You need historical context

### Batch Recall

When exploring a topic, recall several related nodes:
```
kg_recall(level="project", id="old-auth-decision")
kg_recall(level="project", id="session-redesign-2023")
kg_recall(level="project", id="security-audit-findings")
# Now you have full context for the current auth discussion
```

## Reading Strategies

### Strategy 1: Scan for Relevance
After `kg_read()`, scan node IDs and gists for anything relevant to the current task.

### Strategy 2: Follow Edges
Start from a known-relevant node and traverse its edges — what depends on it? What does it depend on?

### Strategy 3: Level-Appropriate Search
- **User level:** Personal preferences, meta-learnings, cross-project patterns
- **Project level:** Architecture, decisions, codebase-specific knowledge

## Subagent Coordination

When spawning subagents that need domain context:
1. Include instruction: "First call `kg_read()` to load knowledge graph"
2. Subagent writes visible to parent via shared server
3. After subagent completes, call `kg_sync()` to see their discoveries

**Skip graph loading for simple subagents** (file operations, searches) — unnecessary context.
