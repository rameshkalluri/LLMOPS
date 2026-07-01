# LLMOps in 5 Days — End-to-End Learning Plan

A focused, hands-on plan to learn **LLMOps** (operationalizing Large Language Model
apps) from zero to a **deployed, monitored, secure, cost-controlled** LLM application —
including **how companies deploy LLM apps on GKE/Kubernetes**. Budget **4–6 hours/day**
(≈2 hr theory + 2–4 hrs hands-on).

> **What is LLMOps?** The practices + tooling to take an LLM app from a notebook demo to
> **reliable, evaluated, monitored, secure, and cost-controlled** production — like
> MLOps, but adapted for prompts, RAG, agents, and generative models.

> **Big-picture analogy:** An LLM is a brilliant but forgetful, occasionally-hallucinating
> **new intern**. LLMOps is everything you do to make that intern **dependable at work**:
> give them the right notes (RAG), clear instructions (prompts), performance reviews
> (evaluation), a manager watching quality (monitoring), safety rules (guardrails), a
> desk to work at (deployment on Cloud Run/GKE), and a budget (cost control).

---

## The 5-Day Map

| Day | Theme | You'll be able to... |
|---|---|---|
| **1** | LLM Foundations & Prompt Engineering | Talk to an LLM well and control cost/behavior |
| **2** | RAG (give the model your data) | Build a grounded Q&A over your own documents |
| **3** | Orchestration, Agents & Fine-Tuning | Build a multi-tool agent; choose how to customize |
| **4** | Evaluation, Deployment & **GKE/Kubernetes** serving | Ship the app to Cloud Run *and* Kubernetes like a company would |
| **5** | Monitoring, Guardrails, Security, Cost & CI/CD | Run it safely, cheaply, and reliably in production |

📁 **Day-by-day notes** live in the `Day1/` … `Day5/` folders (each has a `README.md`
plus topic files with clean, simple analogies).

🧰 **Using a specific stack?** See [`Stack/`](Stack/README.md) — notes mapping a real
production stack (**LiteLLM, Vertex AI, Bedrock, Postgres/pgvector, Arize Phoenix, prompt
management, interaction history**) onto these 5 days.

---

## Prerequisites (Day 0 — Setup)
- **Python 3.10+**, a code editor, and comfort with `pip`/virtualenv.
- An **API key** for at least one provider: OpenAI, Anthropic, or **Google Vertex AI /
  Gemini** (ties into your GCP notes).
- Install core libs: `pip install openai langchain langchain-community llama-index chromadb tiktoken fastapi uvicorn`.
- Install **Docker** and **kubectl**; have your **GCP project + gcloud** ready (Day 4 GKE).
- Create a **budget/spend limit** on your LLM provider (cost control from Day 1!).
- Bookmark: provider docs, [LangChain](https://python.langchain.com),
  [LlamaIndex](https://docs.llamaindex.ai), [Ragas](https://docs.ragas.io),
  [GKE docs](https://cloud.google.com/kubernetes-engine/docs).

---

## Day 1 — Foundations: LLM Basics & Prompt Engineering
**Theory**
- LLM fundamentals: **tokens, context window, temperature/top-p**, system vs user
  messages, **embeddings**, and **why models hallucinate**.
- Cost & latency drivers: input/output tokens, model size, streaming.
- Prompt engineering: zero/few-shot, chain-of-thought, role prompting, **structured
  output (JSON)**, prompt templates.

**Hands-on**
- Call an LLM API; experiment with **temperature** and **system prompts**.
- Count tokens with `tiktoken`; observe cost/latency trade-offs.
- Build **prompt templates** and force **JSON output**; validate it.

**Deliverable:** a small "prompt toolkit" notebook + notes on what changed behavior.
📁 Notes: [`Day1/`](Day1/README.md)

---

## Day 2 — RAG (Retrieval-Augmented Generation)
**Theory**
- Why RAG: give the model **your** data + fresh facts, reduce hallucination, add citations.
- **Embeddings & vector databases**, similarity search.
- **Chunking** strategies (size/overlap) and why they matter.
- The pipeline: **chunk → embed → store → retrieve → augment → generate**.
- **Advanced RAG:** metadata filtering, **hybrid search**, **re-ranking**.

**Hands-on**
- Build a **minimal RAG** over your own PDFs/markdown using **Chroma**.
- Add **metadata filters** + a **re-ranking** step; compare answer quality.

**Deliverable:** a grounded RAG Q&A that cites its sources.
📁 Notes: [`Day2/`](Day2/README.md)

---

## Day 3 — Orchestration, Agents & Fine-Tuning
**Theory**
- **Orchestration frameworks:** LangChain vs LlamaIndex — chains, retrievers.
- **Memory:** multi-turn conversations.
- **Agents & tools:** function/tool calling, the ReAct loop, when agents help vs hurt.
- **Customization decision:** **Prompting vs RAG vs Fine-tuning** — what each fixes.
- **Fine-tuning basics:** dataset prep (JSONL), **LoRA/PEFT** concept, hosted fine-tunes.

**Hands-on**
- Add **conversation memory**; build an **agent** with 1–2 tools (calculator + your RAG).
- (Optional) Prepare a tiny fine-tuning dataset and run a hosted fine-tune.

**Deliverable:** a multi-turn RAG **agent** that uses tools.
📁 Notes: [`Day3/`](Day3/README.md)

---

## Day 4 — Evaluation, Deployment & Serving on GKE / Kubernetes
**Theory**
- **Evaluation (heart of LLMOps):** offline vs online, **LLM-as-a-judge**, RAG metrics
  (faithfulness, answer relevancy, context precision/recall), golden datasets.
- **Packaging:** wrap the app in an **API (FastAPI)**, containerize with **Docker**.
- **Serverless deploy:** **Cloud Run** (ties to your GCP Day 7 notes).
- **How companies deploy LLM apps on GKE/Kubernetes (manual):** Deployment + Service +
  Ingress, ConfigMaps/Secrets, **HPA autoscaling**, **GPU node pools**, health probes,
  rolling updates — the real production pattern.
- **Model serving for self-hosted/open models:** **vLLM, TGI, KServe**, GPUs on GKE.

**Hands-on**
- Build a **golden Q&A set** and run **Ragas** evaluation; get a score report.
- Wrap the app in **FastAPI** + **Docker**; deploy to **Cloud Run**.
- **Deploy the same container to GKE** with `Deployment` + `Service` + `Ingress` + `HPA`
  (manifests provided in the notes). Optionally serve an open model with **vLLM on a GPU node pool**.

**Deliverable:** the app running on **both Cloud Run and GKE**, with an eval report.
📁 Notes: [`Day4/`](Day4/README.md)

---

## Day 5 — Monitoring, Guardrails, Security, Cost & CI/CD
**Theory**
- **Observability:** tracing prompts/responses, token/cost/latency metrics, user
  feedback; tools like **Langfuse/LangSmith**.
- **Guardrails & safety:** input/output moderation, grounding checks, PII handling.
- **Security:** **prompt injection**, data leakage, the **OWASP Top 10 for LLM apps**.
- **Cost & performance ops:** caching, **semantic caching**, model routing (cheap→expensive),
  batching, rate limiting.
- **CI/CD for LLM apps:** version prompts, run the eval suite as a **quality gate** before deploy.

**Hands-on**
- Add **tracing + metrics** (Langfuse/LangSmith) and a **feedback endpoint**.
- Add a **guardrail** (input moderation + prompt-injection check + output validation).
- Add a **cache** (exact or semantic) and measure cost/latency savings.
- Sketch a **CI/CD pipeline** that runs eval before deploying to Cloud Run/GKE.

**Deliverable:** a deployed, evaluated, monitored, guarded, cost-optimized LLM app —
a full **end-to-end LLMOps** pipeline.
📁 Notes: [`Day5/`](Day5/README.md)

---

## End-to-End Architecture (what you'll have built)

```
                 ┌──────────────────────────── LLMOps Loop ────────────────────────────┐
                 │                                                                      │
User ──> API (FastAPI on Cloud Run / GKE) ──> Guardrails (input) ──> Orchestrator       │
                 │                                              │   (LangChain)          │
                 │                                     ┌────────┴────────┐               │
                 │                                     │  RAG retriever  │──> Vector DB   │
                 │                                     │  + tools/agent  │   (Chroma/…)   │
                 │                                     └────────┬────────┘               │
                 │                                              ▼                        │
                 │                                    LLM (API or self-hosted            │
                 │                                     via vLLM/TGI on GKE GPUs)          │
                 │            Guardrails (output) <─────────────┘                        │
                 ▼                     │                                                 │
           Response            Tracing + Metrics (Langfuse/LangSmith): tokens, cost,     │
                               latency, feedback ──> Evaluation (Ragas) ──> CI/CD ───────┘
```

---

## Prompting vs RAG vs Fine-Tuning (cheat-sheet)

| Technique | Fixes | Effort/Cost | Use when |
|---|---|---|---|
| **Prompt engineering** | Behavior with existing knowledge | Lowest | First thing to try; formatting, tone, reasoning |
| **RAG** | Missing/changing **knowledge**, hallucination | Medium | Model needs *your* data / fresh facts + citations |
| **Fine-tuning** | Consistent **style/format/behavior**, niche tasks | Highest | Prompt+RAG aren't enough; you have good training data |

> Rule of thumb: **Prompt → RAG → Fine-tune**, in that order.

---

## Cloud Run vs GKE for LLM apps (quick contrast — detail in Day 4)

| | **Cloud Run** | **GKE / Kubernetes** |
|---|---|---|
| You manage | Just the container | Cluster + workloads |
| Scales to zero | ✅ | Usually no (pods stay warm) |
| GPUs | Limited | ✅ Full GPU node pools (self-host models) |
| Control | Less | Full (networking, sidecars, operators) |
| Best for | API wrappers calling hosted LLMs | Self-hosted models, complex/regulated platforms |
| Analogy | Renting a serviced pop-up | Running your own workshop |

---

## Key Metrics to Track (LLMOps golden signals)
- **Quality:** faithfulness/groundedness, answer relevancy, eval score vs golden set.
- **Cost:** tokens per request, $/request, cache hit rate.
- **Latency:** time-to-first-token, total response time.
- **Reliability:** error rate, timeout rate, guardrail trigger rate.
- **User signal:** thumbs up/down, resolution rate.

---

## Recommended Tools (by stage)
- **Models:** OpenAI, Anthropic, **Google Vertex AI / Gemini**, Ollama/vLLM (self-host).
- **Orchestration:** LangChain, LlamaIndex.
- **Vector DB:** Chroma (local), pgvector, Pinecone, Weaviate, Vertex AI Vector Search.
- **Evaluation:** Ragas, DeepEval, promptfoo, LLM-as-a-judge.
- **Observability:** Langfuse, LangSmith, Arize Phoenix.
- **Serving/Deploy:** FastAPI, Docker, **Cloud Run**, **GKE**, KServe, vLLM, TGI.
- **Guardrails:** provider moderation APIs, NeMo Guardrails, Guardrails AI.

---

## Daily Habit Checklist
- [ ] 2 hr concept reading/notes
- [ ] 2–4 hr hands-on build
- [ ] Track **tokens + cost** for the day's experiments
- [ ] Commit code + **prompt versions** to Git
- [ ] Set/verify provider **spend limit**
- [ ] **Delete idle GKE clusters / GPU nodes** after labs (Day 4+)

---

## Where to go next (after 5 days)
- Multi-agent systems and complex tool orchestration.
- Advanced fine-tuning (LoRA/QLoRA) and hosting open models at scale (vLLM, TGI, KServe).
- Robust CI/CD with automated eval gates and canary prompt releases.
- Data/feedback flywheel: turn production traces into eval sets and training data.
- Security hardening against the **OWASP LLM Top 10**.
