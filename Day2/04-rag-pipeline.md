# The RAG Pipeline

Two phases: **Ingestion** (prepare your data, done ahead of time) and **Query** (answer a
question, done live).

> **Analogy:** First you **organize the library** (ingestion): tear pages into tidy
> sections and place them on the map of meaning. Then, when someone asks a question
> (query), the librarian **grabs the relevant pages** and the intern **answers from them**.

---

## Phase 1 — Ingestion (build the knowledge base)
```
Documents → Load → Chunk → Embed → Store in Vector DB (+ metadata)
```
1. **Load** files (PDF, markdown, HTML, DB rows).
2. **Chunk** them (Day 2.3).
3. **Embed** each chunk (Day 1.3).
4. **Store** vectors + text + metadata in the vector DB (Day 2.2).

> Run this as a **repeatable pipeline** — re-run when documents change.

---

## Phase 2 — Query (answer time)
```
Question → Embed → Retrieve top-k chunks → Build prompt (context + question) → LLM → Answer (+ citations)
```
1. **Embed** the user's question.
2. **Retrieve** the top-k most similar chunks.
3. **Augment**: insert those chunks into the prompt as CONTEXT.
4. **Generate**: the LLM answers **using only that context**, and cites sources.

---

## The all-important prompt (grounding)
```text
System: Answer ONLY using the CONTEXT below. If the answer isn't there, say
        "I don't know." Cite the source for each claim.

CONTEXT:
{retrieved_chunks_with_sources}

QUESTION: {user_question}

Answer as JSON: {"answer": "...", "sources": ["..."]}
```

> **Analogy:** The exam rule written at the top: "**Use only the provided pages. If it's
> not there, say you don't know. Cite the page.**" This is what stops made-up answers.

---

## Minimal code (concept, LangChain)
```python
# Ingestion
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
db = Chroma.from_texts(chunks, embedding=OpenAIEmbeddings(), metadatas=metas)

# Query
retriever = db.as_retriever(search_kwargs={"k": 4})
docs = retriever.invoke(user_question)          # top-4 relevant chunks
context = "\n\n".join(d.page_content for d in docs)
# ...insert context into the prompt template, then call the LLM
```

---

## Where RAG goes wrong (and the fix)
| Symptom | Likely cause | Fix |
|---|---|---|
| Irrelevant answers | Bad chunking / wrong top-k | Re-chunk; tune k; re-rank (Day 2.5) |
| Misses obvious docs | Embedding/keyword gap | **Hybrid search** (Day 2.5) |
| Hallucinates anyway | Weak grounding prompt | Add "only from context / say I don't know" |
| Right doc, wrong part | Chunks too big | Smaller chunks + re-ranking |
| Slow/expensive | Too many/large chunks | Lower k; smaller chunks; cache (Day 5) |

---

## TL;DR (in plain English)
- RAG has two phases: **Ingestion** (load → chunk → embed → store) and **Query**
  (embed question → retrieve top-k → augment prompt → generate).
- The **grounding prompt** ("use only the context, cite sources, say I don't know") is
  what prevents hallucinations.
- Make ingestion a **repeatable pipeline**; debug quality by tuning **chunking, top-k,
  hybrid search, and re-ranking**.
