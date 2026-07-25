"""Reusable utility functions for the AI Code Assistant."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from src.config import HISTORY_FILE, logger


# ---------------------------------------------------------------------------
# Chat History Management
# ---------------------------------------------------------------------------

def load_history() -> list[dict[str, str]]:
    """Load chat history from disk, returning default if not found."""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not load history: %s. Resetting.", exc)
    return _default_history()


def save_history(history: list[dict[str, str]]) -> None:
    """Persist chat history to disk."""
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except OSError as exc:
        logger.error("Failed to save history: %s", exc)


def clear_history() -> None:
    """Clear the saved chat history on disk."""
    try:
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
        logger.info("Chat history cleared.")
    except OSError as exc:
        logger.error("Failed to clear history: %s", exc)


def _default_history() -> list[dict[str, str]]:
    """Return the default conversation history with system prompt."""
    from src.prompts import SYSTEM_PROMPT
    return [{"role": "system", "content": SYSTEM_PROMPT}]


# ---------------------------------------------------------------------------
# File Operations
# ---------------------------------------------------------------------------

def read_file_content(file_path: str) -> tuple[bool, str]:
    """Read a Python file and return (success, content)."""
    path = Path(file_path)
    if not path.exists():
        return False, "File not found."
    if path.suffix not in (".py", ".txt", ".md", ".json", ".log"):
        return False, "Unsupported file type. Please choose a .py or .txt file."
    try:
        content = path.read_text(encoding="utf-8")
        return True, content
    except (OSError, UnicodeDecodeError) as exc:
        logger.error("Failed to read file %s: %s", file_path, exc)
        return False, f"Error reading file: {exc}"


def save_response_to_file(content: str, task: str) -> Optional[Path]:
    """Save AI response to a timestamped file in the data directory."""
    try:
        from src.config import DATA_DIR
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{task}_{timestamp}.txt"
        dest = DATA_DIR / filename
        dest.write_text(content, encoding="utf-8")
        logger.info("Response saved to %s", dest)
        return dest
    except OSError as exc:
        logger.error("Failed to save response: %s", exc)
        return None


# ---------------------------------------------------------------------------
# Export Helpers
# ---------------------------------------------------------------------------

def export_chat_history(history: list[dict[str, str]]) -> str:
    """Format chat history as readable text for export."""
    lines: list[str] = []
    for entry in history:
        role = entry.get("role", "unknown")
        content = entry.get("content", "")
        if role == "system":
            continue
        label = "You" if role == "user" else "Assistant"
        lines.append(f"[{label}]")
        lines.append(content)
        lines.append("-" * 40)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------------------------

def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to max_length, appending '...' if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + "..."


def format_response_for_display(response: str) -> str:
    """Basic formatting cleanup: ensure code blocks render well."""
    response = response.strip()
    if response.startswith("```") and response.endswith("```"):
        return response
    if "```" not in response:
        return response
    return response