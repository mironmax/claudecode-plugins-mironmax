"""Constants for knowledge graph operations."""

# Token estimation
BASE_NODE_TOKENS = 20
CHARS_PER_TOKEN = 4
TOKENS_PER_EDGE = 15

# Compaction
COMPACTION_TARGET_RATIO = 0.9

# Session
SESSION_ID_LENGTH = 8
SESSION_TTL_SECONDS = 24 * 60 * 60  # 24 hours

# Grace periods
GRACE_PERIOD_DAYS = 7
ORPHAN_GRACE_DAYS = 7

# Graph levels
LEVELS = ("user", "project")

# Hardcoded paths (not configurable)
# User:    ~/.claude/knowledge/user.json
# Project: <project>/.claude/knowledge/graph.json
PROJECT_KNOWLEDGE_PATH = ".claude/knowledge/graph.json"
