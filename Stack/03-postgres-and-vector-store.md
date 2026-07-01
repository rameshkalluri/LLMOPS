# Postgres & Vector Store

In your stack, **Postgres is the storage backbone** — and with the **pgvector**
extension it can *also* be your **vector store** for RAG. One database, several jobs.

> **Analogy:** Postgres is the **filing cabinet** of the restaurant. It holds the **guest
> logbook** (interaction history), the **recipe book** (prompts), and normal **business
> records** (app data). Add **pgvector** and the same cabinet gains a **"find dishes by
> taste" index** (semantic search) — no separate cabinet needed.

**Where it fits:** Day 2 (vector store for RAG), Day 3 (memory/history), Day 5
(logging, prompt versions, cost records).

---

## What Postgres stores in an LLM app

| Data | Example | LLMOps layer |
|---|---|---|
| **App/business data** | users, orders, documents | Normal relational (GCP Day 6) |
| **Interaction history** | conversations, prompts, responses, feedback | Memory + observability (Day 3, 5) |
| **Prompt versions** | prompt text + version + metadata | Prompt management (Day 5) |
| **RAG vectors (pgvector)** | chunk embeddings + text + metadata | Retrieval (Day 2) |
| **LiteLLM proxy data** | virtual keys, spend, usage | Gateway governance (Stack §1) |

> **One DB, fewer moving parts** — a big operational win vs running a separate vector DB,
> log store, and prompt store.

---

## pgvector = Postgres as a vector store 🔎
**pgvector** is a Postgres extension that adds a `vector` column type and
**similarity search** — so you can do RAG retrieval (Day 2) **inside Postgres**.

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id          BIGSERIAL PRIMARY KEY,
    content     TEXT,                    -- the chunk text
    embedding   VECTOR(768),             -- the embedding (Day 1/2)
    metadata    JSONB                    -- source, page, date, tenant...
);

-- Retrieve top-5 most similar chunks to a query embedding
SELECT content, metadata
FROM documents
ORDER BY embedding <=> :query_embedding      -- <=> = cosine distance
LIMIT 5;
```

- `<=>` finds nearest vectors (semantic search — Day 2.2).
- Add an **index (HNSW/IVFFlat)** for fast search at scale.
- **`metadata` (JSONB)** enables **metadata filtering** (Day 2.5), e.g., per-tenant or by date.

> **Analogy:** Each row is a **library card** with the passage text, its **map-of-meaning
> coordinate** (embedding), and **labels** (metadata) — all in the cabinet you already run.

---

## pgvector vs a dedicated vector DB

| | **pgvector (Postgres)** | **Dedicated (Pinecone/Weaviate/…)** |
|---|---|---|
| Ops | **One DB you already run** | Another service to run/pay |
| Scale | Great to millions of vectors | Better at very large scale |
| Features | SQL + filters + joins | Vector-specialized features |
| When | Most apps; keep it simple | Huge scale / heavy vector workloads |

> Start with **pgvector** (you already have Postgres). Move to a dedicated vector DB only
> if scale/latency demands it.

---

## Practical tips (LLMOps)
- Keep **embeddings model + dimension** consistent (re-embed everything if you change it).
- Store **metadata** for citations + filtering + **tenant isolation** (Day 5 security).
- Add the right **vector index** and tune it; monitor query latency.
- Separate **transactional** tables from **vector** tables logically; back up regularly.
- For history, log enough to power **memory (Day 3)** and the **feedback flywheel (Day 5)**.

---

## TL;DR (in plain English)
- **Postgres = one filing cabinet** for app data, **interaction history**, **prompt
  versions**, and (via LiteLLM) gateway keys/spend.
- **pgvector** turns that same Postgres into your **vector store** for RAG — embeddings +
  text + metadata, searched with `<=>` (cosine).
- **One DB, fewer moving parts**; use **metadata** for filtering/citations/tenant
  isolation, and add a **vector index** for speed.
- Graduate to a **dedicated vector DB** only if scale truly requires it.
