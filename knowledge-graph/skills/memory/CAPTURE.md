# Capturing Knowledge — Detailed Reference

## The Capture Imperative

Capture knowledge **immediately when you discover it**, not at session end. Context degrades quickly. The insight that took 20 minutes to discover takes 20 seconds to record — but only if you do it now.

## Decision: Should I Capture This?

```
Is this recoverable from existing artifacts (code, docs, config)?
├─ YES → Don't capture. At most, add a `touches` reference.
└─ NO → Continue...

Did discovering this require non-trivial effort?
├─ NO → Probably don't capture.
└─ YES → Continue...

Would this help future sessions avoid repeated work?
├─ YES → Capture it.
└─ NO → Don't capture.
```

## Capture Triggers

| Trigger | What to Capture | Level |
|---------|-----------------|-------|
| Spent 10+ min debugging something | Root cause pattern, not just the fix | project |
| User corrected your approach | What signal you missed, how to recognize it | user |
| Found yourself explaining same thing twice | The explanation as a reusable node | project |
| Discovered undocumented dependency | The relationship as an edge | project |
| Made an architectural decision | The decision AND its rationale | project |
| Recognized a pattern from another project | The generalized pattern | user |
| Got confused about something obvious | Why it's confusing, how to avoid | user |

## Decision: Node vs Edge vs Note

```
Connecting two things that already exist (nodes, files, concepts)?
├─ YES → Create an EDGE
└─ NO → Continue...

Standalone insight that could be referenced later?
├─ YES → Create a NODE
└─ NO → Continue...

Caveat, detail, or context for an existing node?
├─ YES → Add to existing node's `notes`
└─ NO → Continue...

Tentative/weak association?
├─ YES → Add to existing node's `touches`
└─ NO → Reconsider if worth capturing
```

## Edge-First Thinking

Before creating a node, ask: **"Can I express this as a relationship?"**

Edges are more powerful because they:
1. Encode meaning in structure, not just text
2. Connect to existing knowledge
3. Survive better during compaction (connectedness score)

**Example transformation:**

What you might write as a node:
```
id: "api-auth-requires-session"
gist: "API auth system requires active session from handler before validating tokens"
```

Better as an edge:
```
from: "api/auth.py" → to: "session-handler"
rel: "requires-active"
notes: ["token validation fails silently without session"]
```

Same information, but reuses existing references, encodes relationship type explicitly, and is discoverable from either end.

## Compression Techniques

### Level 1: Remove Filler Words

Strip articles, hedging, unnecessary context.

Bad: "I discovered that the configuration file needs to be loaded before the database module initializes, otherwise connections fail"

Good: "config must load before db init; silent connection failure otherwise"

### Level 2: Use References Instead of Descriptions

Don't describe what can be pointed to.

Bad: "The user authentication module that handles login and token validation"

Good: `auth/` or `auth-module` (node ID)

### Level 3: Encode Relationships as Structure

Bad: Node "config-depends-on-env-vars" with gist explaining the dependency

Good: Edge `config.py --reads--> .env` with notes for specifics

### Level 4: Generalize When Patterns Repeat

When you see the same pattern 3+ times, generalize.

Bad: Three nodes: "config-load-order-bug", "auth-init-order-bug", "cache-init-order-bug"

Good: One node:
```
id: "silent-init-order-deps"
gist: "modules with implicit init order deps fail silently; seen in config, auth, cache"
touches: ["config.py", "auth/init.py", "cache/init.py"]
```

### Level 5: The Headline Test

A node's `gist` should read like a newspaper headline — informative but terse.

Bad: "During the debugging session on Tuesday, I found that the reason the API was returning 500 errors was because..."

Good: "API 500s: db pool exhausted under concurrent auth checks"

## What to Capture at Each Level

### User Level (Cross-Project Wisdom)

**Capture:**
- Meta-cognitive patterns: "I tend to X when I should Y"
- User interaction signals: "When user says 'focus', I'm being too scattered"
- Architectural principles: "Agentic pipelines need explicit data contracts"
- Tool/technique insights: "pytest fixtures > manual setup for stateful tests"
- Own failure patterns: "I assume X, but usually Y"

**Don't capture:** Project-specific details, temporary preferences, facts about specific codebases.

**Quality bar:** Would this help in a completely different project?

### Project Level (Codebase-Specific)

**Capture:**
- Architecture decisions and rationale
- Non-obvious dependencies between components
- Debugging discoveries: "X fails when Y because Z"
- Code conventions not in docs
- Performance gotchas, integration points

**Don't capture:** Things obvious from reading code, standard framework behavior, temporary state (WIP).

**Quality bar:** Would a new developer benefit from knowing this?

## API Usage

### Creating a Node
```
kg_put_node(
  level="project",           # or "user"
  id="kebab-case-id",        # descriptive, unique within level
  gist="the insight itself", # terse but complete
  touches=["file.py"],       # optional: related artifacts
  notes=["caveat or context"] # optional: additional details
)
```

**ID conventions:** kebab-case, descriptive, include domain hint (`auth-token-refresh` not `refresh`).

### Creating an Edge
```
kg_put_edge(
  level="project",
  from="source-node-or-path",
  to="target-node-or-path",
  rel="relationship-type",   # depends-on, requires, implements, contradicts, etc.
  notes=["optional context"]
)
```

**Direct artifact references** — reference files without wrapping in nodes:
```
kg_put_edge(level="project", from="src/api/auth.py", to="src/session/handler.py",
            rel="requires-init", notes=["auth.validate() assumes session.current exists"])
```

## Anti-Patterns

- **Capturing obvious things** — "Python uses indentation for blocks"
- **Duplicating documentation** — "The API endpoint /users accepts POST"
- **Storing temporary state** — "Currently working on auth refactor"
- **Creating orphan nodes** — No edges, no touches. Ask: what does this connect to?
- **Over-specifying** — 500-word gist. Use terse gist + notes + edge to file instead
