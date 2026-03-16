# Maintaining the Knowledge Graph — Detailed Reference

## Self-Reflection Triggers

Patterns that should cause you to pause, reflect, and potentially capture a meta-learning.

### Trigger 1: Spinning Wheels

**Pattern:** 3+ attempts at the same type of action without progress.

**Response:**
1. STOP. Don't try a fourth time.
2. Ask: What am I assuming that might be wrong? Have I seen this before? (`kg_sync()`)
3. If you discover something: capture meta-learning (user level), specific issue (project level).

### Trigger 2: User Correction

**Pattern:** User says "no," "that's wrong," "focus," "step back," "not what I meant."

**Response:**
1. STOP. Don't continue in the same direction.
2. Understand what the user actually wants.
3. Identify the signal you missed: misinterpretation? over-complication? wrong assumption?
4. Capture the pattern at user level.

### Trigger 3: Confusion About Known State

**Pattern:** Asking "where is this data?" or "did X happen?" about something you should know.

**Response:**
1. Red flag — you're guessing instead of tracing.
2. Explicitly trace the data/state flow.
3. Capture: poor code organization → project level; your own pattern → user level.

### Trigger 4: Unexpected Tool/Agent Result

**Pattern:** Output doesn't match expectation.

**Response:**
1. Don't work around it — understand WHY.
2. The mismatch reveals: wrong mental model (user), undocumented behavior (project), or actual bug.

### Trigger 5: Deja Vu

**Pattern:** "I feel like I've solved this before" or "This seems familiar."

**Response:**
1. Check the knowledge graph — you probably have.
2. If found: use existing nodes. If not found but should have been captured: capture now.

## Session Lifecycle

### Session Start

**Always, immediately:**
```
kg_read()
kg_register_session()
```

Then scan the loaded graph for anything relevant to the upcoming task.

### During Session

**Every ~30 minutes or after significant work:**
- Have you captured anything? If not, why not?
- `kg_sync()` to check for updates from other sessions

**After completing a non-trivial task:**
- What did you learn that's worth keeping?
- Are there relationships to record?

### Session End

When user says "wrap up," "ending session," or conversation winds down naturally:

1. **Flush** — Capture any pending insights not yet recorded
2. **Reflect** — "What took longer than expected? What would help next session?"
3. **Maintain** — Run a quick graph health check if time allows
4. **Suggest** — If spare capacity remains, mention `/skill scout` or `/skill extract`

Use `kg_session_stats(session_id)` to check session duration and operation count.

### "Use Remaining Capacity"

When user explicitly says to use spare capacity:
- `/skill scout` — mine conversation history for patterns
- `/skill extract` — map current codebase architecture
- Graph maintenance — review orphaned/disconnected nodes

## Graph Health

### Compaction (Automatic)

System archives low-value nodes when graph exceeds token limits.

**What keeps a node alive:**
- Recent updates (within 7 days)
- Connections to other active nodes (edges)
- Rich content (gist + notes)

**What gets archived first:** Old, isolated, sparse nodes.

**Your role:** If a node is important, update it occasionally or connect it to active knowledge.

### Orphan Detection

Nodes with no edges and no touches are at risk. When creating a node, always consider:
- What does it connect to?
- What edges should exist?

### Maintenance Operations

For manual graph maintenance, use `kg_read()` to audit, then:

**Find disconnected nodes:**
Look for nodes that appear in no edges (neither `from` nor `to`). Either connect them or delete if stale.

**Find duplicates:**
Nodes with overlapping gists or IDs. Merge: keep the richer one, add missing info, delete the other.

**Clean up stale knowledge:**
Nodes about things that no longer exist (removed code, old decisions). Delete with `kg_delete_node()`.

**Verify edges:**
Edges pointing to non-existent files or outdated concepts. Delete with `kg_delete_edge()`.

## First Session in a Project

When the project graph is empty:

1. **Don't capture everything.** Resist the urge to document the whole codebase.
2. **Capture high-value observations:** Surprising architectural choices, non-obvious dependencies, things that confused you initially.
3. **Create foundational nodes** for major components (2-5 nodes max).
4. **Add edges** as you discover relationships during actual work.
5. **Bootstrap from exploration:** As you explore for the user's task, capture incidentally. Don't make a separate documentation pass.

## Anti-Patterns

- **Deferring capture to session end** — Context is lost by then
- **Over-reflecting** — If pausing every 2 minutes, you're overdoing it. Triggers are for notable moments.
- **Ignoring memory traces** — If edges to archived nodes are relevant, recall them
- **Capturing without connecting** — Isolated nodes are less valuable. Always consider edges.
