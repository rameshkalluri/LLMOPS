# Embeddings (turning text into meaning-numbers)

## What is an embedding?
An **embedding** turns a piece of text into a **list of numbers (a vector)** that
captures its **meaning**. Texts with **similar meaning** get **similar numbers**.

> **Analogy:** Imagine a giant **map of meaning**. Every sentence gets a **coordinate**
> (like GPS). "Dog" and "puppy" land **close together**; "dog" and "bank loan" land
> **far apart**. Embeddings are those coordinates.

---

## Why it matters for LLMOps
Embeddings are the **foundation of RAG (Day 2)** and semantic search. They let a computer
answer "**which of my documents is most related to this question?**" — by comparing
coordinates, not exact words.

> **Analogy:** Keyword search finds the exact word "car." Embedding search understands
> that "**automobile**," "**vehicle**," and "**sedan**" are **nearby on the map** — so it
> finds them too.

---

## How similarity is measured
- Each text → a vector (e.g., 768 or 1536 numbers).
- Compare vectors with **cosine similarity** (angle between them). Closer = more similar.

> **Analogy:** Two arrows pointing **almost the same direction** = very similar meaning;
> pointing **opposite ways** = unrelated.

---

## Keyword vs semantic (embedding) search

| | **Keyword search** | **Semantic (embedding) search** |
|---|---|---|
| Matches | Exact words | **Meaning** |
| "car" finds | "car" | car, automobile, vehicle, sedan |
| Analogy | Ctrl+F | A **librarian who understands topics** |

- Best real systems combine both = **hybrid search** (Day 2).

---

## Where embeddings live: Vector Databases
Embeddings are stored in a **vector database** (Chroma, pgvector, Pinecone, Weaviate,
Vertex AI Vector Search) that can quickly find the **nearest** vectors to a query.
(Covered in Day 2.)

---

## Tiny mental example
```
"How do I reset my password?"   → [0.12, -0.04, 0.88, ...]
"Steps to change login secret"  → [0.11, -0.03, 0.85, ...]   ← very close! (similar meaning)
"Best pizza in Rome"            → [-0.7, 0.5, 0.02, ...]      ← far away (unrelated)
```

---

## TL;DR (in plain English)
- An **embedding = a coordinate on a map of meaning** (text → vector of numbers).
- **Similar meaning → nearby coordinates**; measured by **cosine similarity**.
- They power **semantic search** (find by meaning, not exact words) and are the
  **foundation of RAG**.
- Stored & searched in a **vector database** (Day 2).
