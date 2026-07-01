# Advanced RAG (making retrieval actually good)

Basic RAG often retrieves "okay" chunks. These techniques make it **accurate**.

---

## 1. Metadata filtering 🏷️
Store labels with each chunk (date, product, department, language) and **filter** before
or during search.

> **Analogy:** Telling the librarian "only look in the **2024 HR policies** section" —
> instantly ignores irrelevant shelves.

```python
retriever = db.as_retriever(search_kwargs={
    "k": 4, "filter": {"year": 2024, "dept": "HR"}
})
```

- Great for **multi-tenant** apps (filter by customer), freshness, and permissions.

---

## 2. Hybrid search (keyword + vector) 🔀
Combine **semantic** search (meaning) with **keyword** search (exact terms) and merge the
results.

> **Analogy:** The librarian who understands **topics** (semantic) *and* also matches the
> **exact product code** you mentioned (keyword). Together they rarely miss.

- Fixes the classic gap: embeddings can miss **exact IDs, error codes, names**; keywords
  catch those.

---

## 3. Re-ranking (a second, smarter pass) 🥇
First retrieve a bigger set (e.g., top-20) cheaply, then use a **re-ranker** (a
cross-encoder model) to **re-order** and keep the best few (e.g., top-4).

> **Analogy:** A **first-round sort** grabs 20 maybe-relevant pages; then a **senior
> expert reads them** and keeps the **4 truly best** for the intern.

- Big quality win for a small latency/cost cost. Tools: Cohere Rerank, cross-encoders.

---

## 4. Query rewriting / expansion ✍️
Rephrase or expand the user's question before retrieving (fix typos, add synonyms, split
multi-part questions).

> **Analogy:** Turning a vague mumble into a **clear, well-phrased request** the
> librarian can actually act on.

---

## 5. Better context assembly
- **De-duplicate** overlapping chunks.
- Put the **most relevant chunk first** (models pay less attention to the middle — the
  "lost in the middle" problem).
- Include **source labels** for citations.

> **Analogy:** Hand the intern a **tidy, ordered folder** (best page on top), not a
> messy pile with duplicates.

---

## 6. Guardrails for RAG (preview of Day 5)
- If retrieval confidence is low → answer "**I don't know**" instead of guessing.
- Check the answer is **grounded** in the retrieved text (faithfulness — Day 4 eval).

---

## Putting it together (advanced query flow)
```
Question → (rewrite) → hybrid search (keyword + vector) with metadata filter
        → retrieve top-20 → re-rank → keep top-4 → assemble ordered context
        → grounded prompt → LLM → answer + citations
```

---

## TL;DR (in plain English)
- **Metadata filtering** = only search the right shelves (date/dept/tenant/permissions).
- **Hybrid search** = meaning **+** exact keywords → rarely misses (catches IDs/codes).
- **Re-ranking** = a smart second pass that keeps the **truly best** chunks.
- Also help: **query rewriting**, **de-dup + best-first ordering**, and **low-confidence →
  "I don't know."**
