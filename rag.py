"""Small persistent retrieval layer used by the dashboard and learning agent.

The store deliberately has no third-party dependency. It provides the same
retrieve boundary a hosted vector database can implement later.
"""

from __future__ import annotations

import json
import math
import re
import sqlite3
from pathlib import Path


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


class VectorStore:
    """SQLite-backed document store with cosine-style token similarity."""

    def __init__(self, path: str | Path = "learning_vectors.db") -> None:
        self.path = str(path)
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS documents "
                "(id TEXT PRIMARY KEY, text TEXT NOT NULL, metadata TEXT NOT NULL)"
            )

    def add(self, document_id: str, text: str, metadata: dict | None = None) -> None:
        if not text.strip():
            raise ValueError("Document text cannot be empty.")
        with sqlite3.connect(self.path) as connection:
            connection.execute(
                "INSERT OR REPLACE INTO documents (id, text, metadata) VALUES (?, ?, ?)",
                (document_id, text, json.dumps(metadata or {})),
            )

    def search(self, query: str, limit: int = 3) -> list[dict]:
        query_tokens = _tokens(query)
        if not query_tokens:
            return []
        with sqlite3.connect(self.path) as connection:
            rows = connection.execute(
                "SELECT id, text, metadata FROM documents"
            ).fetchall()
        scored = []
        for document_id, text, metadata in rows:
            document_tokens = _tokens(text)
            if not document_tokens:
                continue
            overlap = len(query_tokens & document_tokens)
            score = overlap / math.sqrt(len(query_tokens) * len(document_tokens))
            if score:
                scored.append(
                    {"id": document_id, "text": text, "metadata": json.loads(metadata), "score": score}
                )
        return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]

    def context_for(self, query: str, limit: int = 3) -> str:
        return " ".join(item["text"] for item in self.search(query, limit))
