# RAG and Web Dashboard Implementation Plan

## Goal

Ground daily learning recommendations in the user's own notes, articles, and
completed work, then expose the resulting plan and progress in a local web
dashboard.

## Current foundation

- `rag.py` provides a persistent SQLite-backed retrieval boundary. It stores
  documents and returns the most relevant context for a learning focus.
- `app.py` accepts retrieved context without changing the existing default
  behavior.
- `dashboard.py` serves a zero-dependency dashboard at `http://127.0.0.1:8000`
  and exposes the same data as `GET /api/plan`.

## Delivery phases

1. **Ingest**: add a CLI/API endpoint for importing Markdown, PDF, and web
   notes; split large documents into overlapping chunks and attach source
   metadata.
2. **Embeddings**: replace token similarity with an embedding provider and a
   production vector database (Chroma, pgvector, or a managed equivalent).
   Keep the `VectorStore.search()` contract stable.
3. **Grounding**: retrieve top-k chunks for the user's level and focus, pass
   them into a prompt/context builder, and return source IDs with each plan.
4. **Dashboard**: add level selection, source upload, retrieval previews,
   completion checkboxes, historical daily logs, and progress charts.
5. **Reliability**: add retrieval-quality tests, citation checks, input-size
   limits, and explicit errors for unavailable embedding/vector services.

## Suggested production shape

`ingest -> chunk -> embed -> vector DB -> retrieve -> context builder ->
AILearningAgent -> dashboard/API`

## Run

```powershell
python dashboard.py
```

To seed context before opening the dashboard:

```python
from rag import VectorStore
store = VectorStore()
store.add("intro", "Prompt engineering improves clarity and evaluation.", {"source": "notes"})
```
