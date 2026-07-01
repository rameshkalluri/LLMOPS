# Orchestration Frameworks

## Why you need one
Real LLM apps aren't a single API call — they're **many steps**: fetch data, retrieve
chunks, format a prompt, call the LLM, parse output, maybe call again. An **orchestration
framework** wires these steps together.

> **Analogy:** The LLM is one **worker**. An orchestration framework is the **assembly
> line + manager** that moves work between stations (retrieve → prompt → model → parse)
> so you don't hand-wire every wire yourself.

---

## The main frameworks

### LangChain
- General-purpose toolkit for **chains, agents, tools, memory, retrievers**.
- Huge ecosystem of integrations (models, vector DBs, tools).
- *Analogy:* a **big toolbox** for building any LLM workflow.

### LlamaIndex
- Focused on **data/RAG**: loading, indexing, and querying your documents.
- *Analogy:* a **specialist for the library** — great at ingest + retrieval.

> Many teams use **LlamaIndex for RAG data** and **LangChain for orchestration/agents**,
> or just one. You can also build without a framework using plain SDK calls.

---

## Chains = steps wired in sequence
A **chain** connects steps so the output of one feeds the next.

```
user question → retriever → prompt template → LLM → output parser → answer
```

> **Analogy:** A **relay race** — each runner (step) passes the baton (data) to the next.

```python
# Concept: a simple RAG chain (LangChain-style)
chain = prompt | llm | output_parser
answer = chain.invoke({"context": docs, "question": q})
```

---

## Common building blocks
- **Prompt templates** — reusable prompts with placeholders (Day 1).
- **Retrievers** — fetch relevant chunks (Day 2).
- **Output parsers** — turn raw text into structured data (JSON → objects).
- **Memory** — carry conversation history (next note).
- **Tools/Agents** — let the LLM take actions (Day 3.3).

---

## LLMOps cautions ⚠️
- Frameworks add **abstraction & version churn** — pin versions, read the code paths.
- More steps = **more latency + cost** (each LLM call adds up).
- Keep prompts **visible and versioned** (don't lose them inside magic wrappers).
- You can always **drop to plain API calls** for simple, critical paths.

---

## TL;DR (in plain English)
- Orchestration frameworks are the **assembly line + manager** that wire multi-step LLM
  workflows.
- **LangChain** = broad toolbox (chains/agents/tools/memory); **LlamaIndex** = RAG/data specialist.
- A **chain** = steps passed in sequence (retrieve → prompt → LLM → parse).
- Watch **latency, cost, and version churn**; keep prompts visible and versioned.
