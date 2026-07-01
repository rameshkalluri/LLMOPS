# Embeddings & Vector Databases

## Recap: embeddings = coordinates of meaning
From Day 1: an **embedding** turns text into a vector (numbers) so that **similar meaning
= nearby coordinates**. RAG uses this to find documents related to a question.

---

## What is a vector database?
A **vector database** stores lots of embeddings and can **instantly find the nearest
ones** to a query embedding (nearest-neighbor search).

> **Analogy:** A **super-organized librarian** who has arranged every paragraph on a
> **map of meaning**. You describe what you want; they instantly point to the **closest
> shelves** — even if you didn't use the exact words on the cover.

---

## How retrieval works (the core loop)
```
1. Question → embed it → a query vector
2. Vector DB finds the top-k nearest stored vectors (most similar chunks)
3. Return those chunks (the "relevant pages")
```
- **top-k** = how many pieces to fetch (e.g., top 4). More context vs more noise/cost.

> **Analogy:** "Bring me the **4 most relevant pages**," not the whole library.

---

## Popular vector databases

| Option | Notes | Good for |
|---|---|---|
| **Chroma** | Simple, local, open-source | Learning, prototypes |
| **pgvector** | Postgres extension | Already using Postgres/Cloud SQL |
| **Pinecone** | Managed, serverless | Production, no ops |
| **Weaviate / Qdrant / Milvus** | Open-source, feature-rich | Self-hosted scale |
| **Vertex AI Vector Search** | Google-managed (ties to your GCP notes) | GCP-native production |

> Start with **Chroma** locally; graduate to a managed/self-hosted DB for production.

---

## What gets stored per chunk
Each entry usually has:
- The **embedding** (the vector),
- The **original text** (to put in the prompt),
- **Metadata** (source file, page, date, author, tags) — used for **filtering** (Day 2.5).

> **Analogy:** Each library card has the **topic-location (vector)**, the **text of the
> passage**, and **labels** (book title, chapter, year).

---

## Similarity metrics (quick note)
- **Cosine similarity** (most common), dot product, or Euclidean distance.
- All answer: "**how close are these two meanings?**"

---

## Indexing (why it's fast)
Vector DBs use approximate-nearest-neighbor indexes (e.g., **HNSW**) to search millions
of vectors in milliseconds — trading a tiny bit of accuracy for huge speed.

> **Analogy:** Instead of checking **every book**, the librarian uses a **smart shortcut
> map** to jump near the right shelf instantly.

---

## TL;DR (in plain English)
- A **vector database = a librarian on a map of meaning**: it finds the **nearest chunks**
  to your question fast.
- Retrieval = **embed question → find top-k nearest chunks → return their text**.
- Each stored chunk keeps its **vector + text + metadata** (metadata powers filtering).
- Start with **Chroma**; scale to Pinecone/pgvector/Weaviate/Vertex AI Vector Search.
