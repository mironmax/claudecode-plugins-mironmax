"""Session management for HTTP MCP server with project path tracking."""

import json
import logging
import os
import time
import uuid
from pathlib import Path
from core.constants import SESSION_ID_LENGTH, SESSION_TTL_SECONDS
from core.exceptions import SessionNotFoundError

logger = logging.getLogger(__name__)

SESSIONS_FILE = Path.home() / ".claude/knowledge/sessions.json"


class HTTPSessionManager:
    """Manages sessions with project_path tracking for multi-project support."""

    def __init__(self, session_ttl: int = SESSION_TTL_SECONDS):
        self.session_ttl = session_ttl
        self._sessions: dict[str, dict] = {}
        self._load_sessions()

    def register(self, project_path: str | None = None) -> dict:
        """
        Register a new session with optional project path.
        Returns {"session_id": str, "start_ts": float}.
        """
        session_id = uuid.uuid4().hex[:SESSION_ID_LENGTH]
        ts = time.time()

        # Resolve project_path to absolute to prevent cwd-dependent behavior
        resolved_project_path = str(Path(project_path).resolve()) if project_path else None

        self._sessions[session_id] = {
            "start_ts": ts,
            "project_path": resolved_project_path,
            "last_activity": ts,
            "op_count": 0,
        }

        logger.info(f"Session registered: {session_id} (project: {resolved_project_path or 'none'})")
        self.save_sessions()  # Persist immediately so project_path survives restarts
        return {"session_id": session_id, "start_ts": ts}

    def ensure_session(self, session_id: str) -> None:
        """
        Re-register a session if it was lost (e.g. server restart).
        Silently creates a new session entry preserving the original ID.
        No-op if session already exists.
        """
        if session_id in self._sessions:
            return

        ts = time.time()
        self._sessions[session_id] = {
            "start_ts": ts,
            "project_path": None,
            "last_activity": ts,
            "op_count": 0,
        }
        logger.info(f"Session auto-recovered: {session_id} (no project_path — was lost on restart)")

    def get_project_path(self, session_id: str) -> str | None:
        """Get project path for a session. Auto-recovers lost sessions."""
        self.ensure_session(session_id)
        self._update_activity(session_id)
        return self._sessions[session_id]["project_path"]

    def get_start_ts(self, session_id: str) -> float:
        """Get session start timestamp. Auto-recovers lost sessions."""
        self.ensure_session(session_id)
        return self._sessions[session_id]["start_ts"]

    def is_valid(self, session_id: str) -> bool:
        """Check if session exists and is not expired."""
        if session_id not in self._sessions:
            return False

        # Check expiration
        session = self._sessions[session_id]
        age = time.time() - session["last_activity"]
        return age <= self.session_ttl

    def _update_activity(self, session_id: str):
        """Update last activity timestamp for a session."""
        if session_id in self._sessions:
            self._sessions[session_id]["last_activity"] = time.time()

    def cleanup_expired(self) -> int:
        """Remove expired sessions. Returns count of removed sessions."""
        current_time = time.time()
        expired = [
            sid for sid, data in self._sessions.items()
            if current_time - data["last_activity"] > self.session_ttl
        ]

        for sid in expired:
            del self._sessions[sid]
            logger.info(f"Session expired: {sid}")

        return len(expired)

    def increment_ops(self, session_id: str) -> None:
        """Increment operation count for a session. Auto-recovers lost sessions."""
        self.ensure_session(session_id)
        self._sessions[session_id]["op_count"] = self._sessions[session_id].get("op_count", 0) + 1
        self._update_activity(session_id)

    def get_stats(self, session_id: str) -> dict:
        """Get session stats: duration, op count, graph sizes. Auto-recovers lost sessions."""
        self.ensure_session(session_id)
        session = self._sessions[session_id]
        now = time.time()
        return {
            "session_id": session_id,
            "duration_seconds": round(now - session["start_ts"]),
            "op_count": session.get("op_count", 0),
            "project_path": session.get("project_path"),
            "started_at": session["start_ts"],
        }

    def count(self) -> int:
        """Return number of active sessions."""
        return len(self._sessions)

    def get_all_project_paths(self) -> set[str]:
        """Get all unique project paths from active sessions."""
        return {
            data["project_path"]
            for data in self._sessions.values()
            if data["project_path"] is not None
        }

    # ========================================================================
    # Session persistence (survive server restarts)
    # ========================================================================

    def _load_sessions(self) -> None:
        """Load sessions from disk on startup."""
        if not SESSIONS_FILE.exists():
            return

        try:
            with open(SESSIONS_FILE) as f:
                saved = json.load(f)

            now = time.time()
            restored = 0
            for sid, data in saved.items():
                # Skip expired sessions
                age = now - data.get("last_activity", 0)
                if age > self.session_ttl:
                    continue
                self._sessions[sid] = data
                restored += 1

            if restored:
                logger.info(f"Restored {restored} session(s) from disk")

        except Exception as e:
            logger.warning(f"Failed to load sessions from {SESSIONS_FILE}: {e}")

    def save_sessions(self) -> None:
        """Save active sessions to disk. Called periodically by store's save loop."""
        try:
            SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

            temp_path = SESSIONS_FILE.with_suffix(".tmp")
            with open(temp_path, 'w') as f:
                json.dump(self._sessions, f, indent=2)
                f.flush()
                os.fsync(f.fileno())

            temp_path.replace(SESSIONS_FILE)

        except Exception as e:
            logger.warning(f"Failed to save sessions: {e}")
            temp_path = SESSIONS_FILE.with_suffix(".tmp")
            if temp_path.exists():
                temp_path.unlink()
