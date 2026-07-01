# Chunking (cutting docs into pieces)

## Why chunk at all?
You can't dump a 300-page manual into the prompt (context window + cost). So you **cut
documents into smaller pieces (chunks)**, embed each, and retrieve only the **relevant
few**.

> **Analogy:** You don't photocopy the **whole book** for one question — you tear out the
> **few relevant pages**. Chunking decides **how big each "page" is**.

---

## The Goldilocks problem 🐻 (chunk size)

| Chunk size | Problem | Analogy |
|---|---|---|
| **Too big** | Lots of irrelevant text, costly, diluted meaning | Handing over a **whole chapter** for a one-line answer |
| **Too small** | Loses context, meaning gets fragmented | A **single sentence** ripped out — misses the point |
| **Just right** | Focused + enough context | A **tidy paragraph/section** |

- Common starting point: **~300–800 tokens** per chunk (tune per data).

---

## Overlap = don't cut mid-thought ✂️
Add a small **overlap** between consecutive chunks so ideas split across a boundary
aren't lost.

> **Analogy:** When tearing pages, **repeat the last sentence** at the top of the next
> page so a thought spanning the cut **isn't chopped in half**.

- Typical overlap: **10–20%** of chunk size.

---

## Chunking strategies (better → best)
1. **Fixed-size** — every N characters/tokens. Simple, but can cut awkwardly.
2. **Recursive/character** — split on paragraphs → sentences → words (keeps structure).
3. **Semantic / structure-aware** — split by **headings, sections, markdown, code blocks**.
   Best quality; respects the document's natural boundaries.

> **Analogy:** Cutting a cake **randomly** vs **along the slice lines** — cutting along
> natural sections keeps each piece whole and meaningful.

---

## Keep metadata with each chunk
Attach **source, title, page/section, date** to every chunk. This enables **citations**
and **filtering** (e.g., "only 2024 policy docs") on Day 2.5.

---

## Practical tips (LLMOps)
- **Clean the text first** (strip boilerplate, headers/footers, HTML noise).
- Tune **chunk size + overlap** by testing retrieval quality (Day 4 eval).
- For tables/code, prefer **structure-aware** splitting.
- Re-chunk when data changes; keep an **ingestion pipeline** you can re-run.

```python
# Concept: LangChain recursive splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
chunks = splitter.split_text(document_text)
```

---

## TL;DR (in plain English)
- **Chunking = tearing out the right-sized pages** so you retrieve only what's relevant.
- Size is a **Goldilocks** choice: not too big (noisy/costly), not too small (loses meaning).
- Add **overlap** so ideas aren't cut mid-thought; prefer **structure-aware** splitting.
- Keep **metadata** per chunk (for citations + filtering); tune with **evaluation**.
