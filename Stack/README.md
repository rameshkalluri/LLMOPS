# Your LLMOps Stack — Reference & Where Each Piece Fits

Notes mapping **your actual tech stack** onto the [LLMOps 5-Day Learning Plan](../LLMOps-5-Day-Learning-Plan.md).

Your stack:
**LiteLLM** · **Vertex AI** · **Bedrock** · **Postgres** · **Vector store** ·
**Arize Phoenix** · **Prompt management** · **Interaction history**

> **Big-picture analogy:** Think of a **restaurant**.
> - **LiteLLM** = the **head waiter** who takes every order and routes it to whichever
>   **kitchen** can cook it (and remembers the bill).
> - **Vertex AI & Bedrock** = two **kitchens** (Google's and Amazon's) that actually cook the dish (the model).
> - **Postgres** = the **filing cabinet** (orders history, receipts, saved recipes) — and with **pgvector**, also the **recipe-by-taste index** (vector store).
> - **Vector store** = the **"find me similar dishes"** index used by RAG.
> - **Arize Phoenix** = the **CCTV + quality inspector** watching every order and grading it.
> - **Prompt management** = the **recipe book** (versioned instructions).
> - **Interaction history** = the **guest logbook** (who asked what, and the reply).

---

## Topics
1. [LiteLLM — the gateway](01-litellm-gateway.md) — one interface to all models; routing, fallbacks, cost, keys.
2. [Vertex AI & Bedrock — the model providers](02-model-providers-vertexai-bedrock.md) — the actual LLMs behind LiteLLM.
3. [Postgres & Vector Store](03-postgres-and-vector-store.md) — app data, history, pgvector for RAG.
4. [Arize Phoenix — observability & eval](04-arize-phoenix.md) — tracing, monitoring, evaluation.
5. [Prompt Management & Interaction History](05-prompt-management-and-history.md) — versioned prompts + conversation logs.

---

## Where each piece fits in the 5-Day framework

| Your tool | What it is | LLMOps layer | Day(s) |
|---|---|---|---|
| **LiteLLM** | Unified LLM gateway/proxy | Model access, routing, cost, keys, logging | 1, 4, 5 |
| **Vertex AI** | Google LLMs (Gemini) + ML platform | Model provider (inference) | 1, 4 |
| **Bedrock** | AWS managed LLMs (Claude, etc.) | Model provider (inference) | 1, 4 |
| **Postgres** | Relational DB (+ pgvector) | Storage: app data, history, prompts, vectors | 2, 3, 5 |
| **Vector store** | Similarity search (pgvector or dedicated) | RAG retrieval | 2 |
| **Arize Phoenix** | LLM tracing/eval (OpenTelemetry) | Observability + evaluation | 4, 5 |
| **Prompt management** | Versioned prompt store | Prompt engineering + CI/CD | 1, 5 |
| **Interaction history** | Stored conversations/traces | Memory + observability + feedback flywheel | 3, 5 |

---

## How it all connects (request flow)

```
                         ┌──────────────── Prompt Mgmt (versioned prompts, in Postgres) ──────────────┐
                         │                                                                            │
User ─► Your App (FastAPI) ─► RAG retrieve (Vector store / pgvector in Postgres)                      │
                         │                     │                                                      │
                         │            build prompt (context + question)                               │
                         │                     ▼                                                      │
                         │             LiteLLM  (the gateway) ──► routes to:                           │
                         │                     ├── Vertex AI  (Gemini)                                 │
                         │                     └── Bedrock    (Claude, etc.)                           │
                         │                     ▲   fallback / load-balance between them                │
                         │                     │                                                       │
                         │        response ◄───┘                                                       │
                         ▼                                                                             │
             Save Interaction History (Postgres)  +  Send traces to Arize Phoenix ◄────────────────────┘
                                                          │
                                                 Evaluation + dashboards (quality, cost, latency)
```

- **LiteLLM** sits between your app and the models → swap Vertex AI ↔ Bedrock without changing app code.
- **Postgres** is your one storage backbone: **app data + interaction history + prompt versions + (pgvector) vectors**.
- **Arize Phoenix** observes every call for **tracing, monitoring, and eval**.

---

## Why this is a strong stack (quick take)
- **Multi-provider resilience** — LiteLLM + Vertex AI + Bedrock means **no single-vendor
  lock-in**, easy fallback, and cost/quality routing across clouds.
- **One database to run** — Postgres (with **pgvector**) can hold RAG vectors, history,
  and prompts, reducing moving parts.
- **Built-in observability/eval** — Arize Phoenix covers the "how is it doing?" layer.
- **Discipline** — prompt management + interaction history give you **versioning** and a
  **feedback flywheel** (the marks of real LLMOps, not just a demo).

---

## TL;DR (in plain English)
- **LiteLLM = head waiter** routing every order to the right **kitchen** (**Vertex AI** /
  **Bedrock**).
- **Postgres = the filing cabinet** for **history, prompts, and (via pgvector) RAG
  vectors**; the **vector store** powers retrieval.
- **Arize Phoenix = CCTV + quality inspector** (tracing, monitoring, eval).
- **Prompt management = versioned recipe book**; **interaction history = the guest
  logbook** that feeds memory and the feedback flywheel.
