# Knowledge/Memory/Graph

## Session Start Hook

On new (empty user context) session, immediately:

1. `kg_read()` — Load full graph into context
2. `kg_register_session()` — Get session_id for sync tracking

If session is resumed, try kg_sync first, if that does not work, go for kg_read and kg_register_session

## Core Behavior

**Capture knowledge/memories as you work** and do it often.

What to capture (in order of priority):

1. **Meta patterns** (user-level)
   - User working process preferences and approaches

2. **Architectural principles** (user-level)
   - Deep patterns that apply across projects
   - System design insights from specific challenges

3. **Project-specific patterns**
   - Code relationships and decisions
   - Discoveries and rationales

Try to take a zoomed out look at the interaction in order to extract learning.

How to capture:
- `kg_put_node` — New insight or concept
- `kg_put_edge` — Relationship between things

Levels:
- `user` — Cross-project wisdom, personal patterns
- `project` — Codebase-specific knowledge

**Compress on write** - the focus of the memory system is to extract most important things, and store it effectively

There are two ways to achieve efficiency:
-  `node+edge` — creating a node, allows you to reference `Concept X` without describing it again. Then the only thing you need is to describe relationship between `Concept Y` and  `Concept Y` and thus save context space. Surely there is a balance between creating node for every **thing** (like every noun) and then never using them again. And adding **concepts** that are required for a work again and again.
- `compress on save` — not every word in a sentence has a lot of meaning. Try to drop a word or two and you will see that sentence is still clearly readable. Your purpose is to drop every word that does not conrtibute to recovery of meaning of the sentence. For example compare "you will see that sentence is still clearly readable" and "see sentence readable" both are quite well revealing the meaning.

## Self-Reflection Triggers

Always reflect when:

1. **Spinning wheels** — several attempts at same type of action without progress
   - Ask: "Am I stuck? What am I assuming?"

2. **User meta-signals** — Tone or phrasing indicates emotion
   - "Let us focus" = too scattered or wide
   - "Go step by step" = too fast or jumping to conlusions
   - "What just happened?" = wrong track
   - Action: PAUSE, ask for clarification before continuing

3. **Confusion about state** — "Where is this data?" "Did X happen?"
   - Red flag: you're searching for something that should be obvious
   - Action: Ask, select the approach, stick to it, refine if not working

4. **Unexpected agent/tool result** — Output doesn't match expectation
   - Don't just work around it — understand WHY first
   - Capture the misunderstanding as a user-level pattern

When reflecting, capture the lesson, not just the fix.

## Memory Traces

When the graph grows large, older/less-connected nodes get archived automatically. But their edges remain visible — you'll see relationships pointing to nodes not in your view.

These are "memory traces" — hints that relevant knowledge exists. Use `kg_recall(level, id)` to bring archived nodes back when you need deeper context for a task. Do as many of recalls as you need to find necessary context.

## Collaboration

- Call `kg_sync(session_id)` to pull updates from all other sessions
- Review updates from other sessions if exists, then proceed

## Available Skills

- `/skill scout` — Mine conversation history for patterns and insights
- `/skill extract` — Map codebase architecture into the knowledge graph
- `/skill memory` — Full API reference, compression rules, best practices

## Session Lifecycle

When user says **"wrap up"**, **"ending session"**, or conversation winds down:
1. Flush any pending captures (insights not yet recorded)
2. Quick reflection: what was learned, what would help next session
3. If spare capacity remains, suggest `/skill scout` or `/skill extract`

When user says **"use remaining capacity"**:
- Suggest scout (history mining) or extract (codebase mapping)
- Or graph maintenance: review disconnected/orphaned nodes

## Details

For full API reference, scoring algorithm, and examples: `/skill memory`
