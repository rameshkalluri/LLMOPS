# LLMOps Interview Questions & Answers — Experienced / Senior

A curated set of **experienced-level** interview questions with answers, covering the
full LLMOps lifecycle from the [5-Day Learning Plan](LLMOps-5-Day-Learning-Plan.md) plus
the production stack in [`Stack/`](Stack/README.md): **LiteLLM, Vertex AI, Bedrock,
Postgres/pgvector, Arize Phoenix, prompt management, interaction history**.

> Tip: For senior roles, interviewers care less about definitions and more about
> **trade-offs, failure modes, cost/latency, evaluation, and production war stories**.

<br>

---

<br>

## 1. Fundamentals & Architecture

<br>

### Q1. What is LLMOps, and how does it differ from traditional MLOps?

LLMOps operationalizes **LLM-powered apps** (prompts, RAG, agents, generative models).

Key differences from MLOps: you often **don't train the core model** (you consume APIs or
fine-tune); outputs are **non-deterministic and hard to score** (no simple accuracy);
**prompts and retrieval** are first-class deployable artifacts; **evaluation is
subjective** (LLM-as-judge, human review); cost/latency are dominated by **token-based
inference**; and new risks appear (**prompt injection, hallucination**). The lifecycle
adds prompt versioning, RAG data pipelines, guardrails, and eval gates.

<br>

---

<br>

### Q2. Walk me through the architecture of a production RAG application.

**Ingestion (offline):** load → **chunk** → **embed** → store in a **vector DB** with
metadata.

**Query (online):** **guardrails (input)** → embed question → **retrieve top-k**
(hybrid + re-rank) → **assemble grounded prompt** → **LLM inference** (via a gateway like
LiteLLM to Vertex AI/Bedrock) → **guardrails (output/grounding)** → response.

**Cross-cutting:** **observability/tracing** (Arize Phoenix), **interaction history**
(Postgres), **prompt management**, **caching**, **eval + CI/CD**, and a **feedback
flywheel** turning production data into eval sets.

<br>

---

<br>

### Q3. Training vs inference — where does each cost live, and why does it matter?

**Training/fine-tuning** = the model learns (rare, GPU-heavy, batch).

**Inference** = using the model per request (constant, per-token or per-GPU-hour).

In most LLM apps the **ongoing cost and latency are almost entirely inference**, which is
why optimizations (caching, model routing, smaller models, prompt trimming) target
inference. Training cost is occasional and separate.

<br>

---

<br>

## 2. Prompting, Context & Model Behavior

<br>

### Q4. How do you decide between prompt engineering, RAG, and fine-tuning?

Order of attack: **Prompt → RAG → Fine-tune** (cheap → expensive).

- **Prompting** fixes format/tone/reasoning.
- **RAG** adds knowledge (fresh, private, cited) and reduces hallucination.
- **Fine-tuning** changes behavior/style or bakes in a task to shorten prompts.

The classic mistake is fine-tuning to "add knowledge" — that's RAG's job (facts go stale
and fine-tuning doesn't reliably store them). Often you **combine**: fine-tune voice/format
+ RAG for facts.

<br>

---

<br>

### Q5. How do you manage the context window in a long multi-turn conversation?

LLMs are **stateless**; you re-send history each turn.

As chats grow, use **windowed memory** (last N turns), **summary memory** (summarize old
turns), or **summary + recent** (common). For cross-session memory, store facts in a
DB/vector store and **retrieve them (RAG over history)**.

Always pin the **system prompt**, cap token budget, and watch the "lost in the middle"
effect — put the most important context first.

<br>

---

<br>

### Q6. What settings do you lock down for a production RAG answer, and why?

Low **temperature** (0–0.3) for determinism/faithfulness; cap **max_tokens**; a strict
**grounding system prompt** ("answer only from context, cite sources, say 'I don't
know'"); structured **JSON output** for parsing; and often a fixed **seed** where
supported.

High temperature is reserved for creative tasks, not factual Q&A.

<br>

---

<br>

## 3. RAG Deep Dive

<br>

### Q7. Your RAG system returns irrelevant or incomplete answers. How do you debug it systematically?

Separate **retrieval** from **generation**.

First check retrieval: are the right chunks being fetched? (log/trace retrieved chunks in
Phoenix, measure **context precision/recall**). If retrieval is bad → fix **chunking**
(size/overlap), add **hybrid search** (keyword+vector for IDs/codes), add **re-ranking**,
add **metadata filters**, or rewrite the query.

If retrieval is good but the answer is wrong → strengthen the **grounding prompt**, reduce
chunk size, or check the model. Use **faithfulness** metrics to catch hallucination despite
good context.

<br>

---

<br>

### Q8. Explain chunking trade-offs and how you'd choose a strategy.

Too-big chunks add noise/cost and dilute meaning; too-small chunks lose context.

Start ~300–800 tokens with 10–20% **overlap** (so ideas aren't cut mid-thought). Prefer
**structure-aware** splitting (headings/sections/code blocks) over fixed-size. Always keep
**metadata** (source, section, date, tenant) for citations and filtering.

Tune empirically via your **eval set**, and re-chunk when data or quality metrics change.

<br>

---

<br>

### Q9. What is hybrid search and re-ranking, and when are they worth the added latency/cost?

**Hybrid search** merges semantic (embedding) and keyword (BM25) results — semantic misses
exact IDs/error codes/names, keyword catches them.

**Re-ranking** retrieves a larger set (e.g., top-20) then uses a cross-encoder to keep the
truly-best few (top-4).

Worth it when answer quality/precision matters and you see retrieval misses; the re-ranker
adds a bit of latency/cost but usually yields a large quality gain. Skip for trivial,
low-stakes lookups.

<br>

---

<br>

### Q10. How do you handle multi-tenant isolation in a shared vector store?

Tag every chunk with a **tenant_id** in metadata and **always filter by it at query time**
(pre-filter). For strong isolation, use separate collections/namespaces or row-level
security (e.g., Postgres RLS with pgvector).

Never rely on the prompt alone — enforce it at the retrieval layer. Also redact PII and
scope embeddings per tenant to avoid cross-tenant leakage (an OWASP "sensitive information
disclosure" risk).

<br>

---

<br>

## 4. Agents & Orchestration

<br>

### Q11. When would you use an agent vs a fixed chain, and what are the risks?

Use a **chain** when the steps are known (predictable, cheaper, easy to test). Use an
**agent** only when the task genuinely needs **dynamic tool selection/looping**.

Agent risks: **higher cost/latency** (multiple LLM calls), **non-determinism**, **infinite
loops**, and **excessive agency** (too much power). Mitigate with **least-privilege
tools**, **max-step limits**, input/output validation, sandboxing, and full step logging.

Principle: use the simplest thing that works.

<br>

---

<br>

### Q12. How do you make tool-calling agents safe in production?

Least-privilege tools (a read-only tool can't delete data), **human-in-the-loop** for risky
actions (payments, deletes), **cap iterations**, validate/sanitize tool inputs and outputs,
and sandbox code execution.

Treat **tool/RAG results as untrusted** (indirect prompt injection can hide in fetched web
pages/docs). Log every tool call with args for audit and debugging.

<br>

---

<br>

## 5. Evaluation (the senior differentiator)

<br>

### Q13. LLM outputs are non-deterministic — how do you evaluate quality reliably?

Combine **offline eval** (a curated **golden dataset** of question→ideal-answer, run on
every change like unit tests) with **online eval** (real feedback: thumbs up/down,
resolution rate).

Use **LLM-as-a-judge** with a rubric for scale, calibrated against **human review**. For
RAG, measure **faithfulness/groundedness, answer relevancy, context precision/recall**
(e.g., Ragas or Phoenix evals).

Track **cost + latency** alongside quality. Version prompts/models/eval sets together and
treat eval as a **CI deploy gate**.

<br>

---

<br>

### Q14. How do you prevent quality regressions when you change a prompt or swap a model (e.g., Gemini → Claude)?

Treat the change as a deployment: run the **eval suite on the golden set** in CI and
**block** if scores drop.

Then **canary** (route a small % of traffic), watch quality/cost/latency in Phoenix, and
**auto-rollback** if it regresses.

Because you use **LiteLLM**, you can A/B two providers by alias and compare traced metrics
side by side before shifting traffic.

<br>

---

<br>

### Q15. What are the pitfalls of LLM-as-a-judge, and how do you mitigate them?

Judges can be **biased** (position/verbosity/self-preference bias), **inconsistent**, and
**expensive**.

Mitigate with a clear **rubric**, reference answers, **pairwise** comparisons instead of
absolute scores where possible, randomizing order, using a **strong/neutral judge model**,
and periodically **calibrating against human labels**.

Never use the same model as both generator and sole judge for high-stakes decisions.

<br>

---

<br>

### Q16. How do you build and evolve a golden eval dataset?

Start with 20–50 realistic cases (real user questions + ideal answers, and for RAG the
expected sources).

Grow it from **production failures and user feedback** (the feedback flywheel), covering
edge cases, adversarial/red-team prompts, and multi-tenant scenarios.

Version it, keep it representative of real traffic distribution, and review periodically so
it doesn't drift from reality.

<br>

---

<br>

## 6. Deployment & Serving (incl. GKE/Kubernetes)

<br>

### Q17. When do you deploy an LLM app on Cloud Run vs GKE/Kubernetes?

**Cloud Run** for apps that **call hosted APIs** (Vertex AI/Bedrock) — serverless,
scale-to-zero, minimal ops, great for spiky traffic and small teams.

**GKE** when you **self-host models on GPUs** (vLLM/TGI), need **full control** (networking,
sidecars, service mesh, custom autoscaling), run **many microservices**, or have
**data-residency/compliance** needs.

Rule of thumb: hosted-API app → Cloud Run; GPU/self-hosted or complex platform → GKE.

<br>

---

<br>

### Q18. Walk me through deploying an LLM API on GKE the way a company would.

Containerize the app (FastAPI + Docker) and push to Artifact Registry.

Then apply K8s manifests: **Deployment** (N replicas, resource requests/limits,
readiness/liveness probes on `/health`), **Service** (stable ClusterIP), **Ingress**
(public HTTPS via a Google LB), **HPA** (autoscale pods on CPU/custom metrics like queue
depth), and **Secrets/ConfigMaps** for keys/config. Use **rolling updates** with rollback.

Production-grade adds: **Workload Identity** (no key files), **RBAC + namespaces**
(dev/staging/prod), TLS/Cloud Armor, GitOps CI/CD (Argo CD) with an **eval gate**,
observability, and cost controls. For self-hosted models, add a **GPU node pool** and
request `nvidia.com/gpu`.

<br>

---

<br>

### Q19. What's special about serving/scaling self-hosted LLMs on GPUs?

The model weights must fit in **GPU memory** (use **quantization** 4/8-bit to shrink);
**cold starts are heavy** (loading multi-GB weights) so keep **min replicas warm**.

Use an inference server like **vLLM** (PagedAttention + **continuous batching**) or **TGI**
for throughput; **KServe** standardizes autoscaling (incl. scale-to-zero) and canaries.

GPUs are expensive → autoscale aggressively, keep utilization high via batching, and
**delete idle GPU pools**. Scaling is often **throughput-bound (tokens/sec)** not just
request count.

<br>

---

<br>

### Q20. How does horizontal pod autoscaling for an LLM service differ from a normal web app?

CPU% is often a poor signal — LLM latency is dominated by the **model call** (I/O-bound if
calling an API, GPU-bound if self-hosted).

Better to scale on **custom metrics**: requests in flight, **queue depth**, GPU
utilization, or tokens/sec. Also account for **long request durations** and **connection
concurrency**, keep **min replicas** warm for cold-start-sensitive paths, and pair HPA
(pods) with the **cluster autoscaler** (nodes) — GPUs make scale-down important for cost.

<br>

---

<br>

## 7. The Stack: LiteLLM, Vertex AI, Bedrock, Postgres, Phoenix

<br>

### Q21. Why put a gateway like LiteLLM in front of Vertex AI and Bedrock?

It gives **one OpenAI-style interface** to many providers (swap by model string/alias),
plus **fallbacks** (Vertex AI down → Bedrock), **load balancing/routing** (cheap vs
premium), **virtual keys + budgets + rate limits**, **cost tracking**, **caching**, and
**centralized logging/callbacks** (e.g., to Phoenix).

It decouples app code from providers — crucial for resilience, cost routing, and avoiding
vendor lock-in. The proxy typically uses **Postgres** for keys/spend.

<br>

---

<br>

### Q22. How would you implement provider fallback and cost-based routing across Vertex AI and Bedrock?

Define model **aliases** and a **routing/fallback policy** in the LiteLLM proxy: primary =
cheaper/faster model, fallback = alternate provider on error/rate-limit/timeout. Route by
**task tier** (simple → small/cheap model, complex → premium).

Use **traced cost/latency/quality per provider** (Phoenix) to tune routing. Test fallbacks
deliberately (chaos-test a provider outage), and ensure prompts/outputs are
provider-agnostic (watch formatting/token differences).

<br>

---

<br>

### Q23. Why use Postgres with pgvector instead of a dedicated vector DB?

**One database, fewer moving parts**: pgvector holds RAG vectors **alongside** app data,
interaction history, and prompt versions, with SQL joins, transactions, **metadata
filtering (JSONB)**, and **row-level security** for tenant isolation.

It scales well into the millions of vectors with HNSW/IVFFlat indexes. Move to a dedicated
vector DB (Pinecone/Weaviate/Milvus) only when scale/latency/vector-specific features
demand it. Keep the **embedding model + dimension consistent** (re-embed if you change it).

<br>

---

<br>

### Q24. What does Arize Phoenix give you, and how do you wire it into this stack?

Phoenix provides **OpenTelemetry-based tracing** (prompt, retrieved context, model call,
tokens, latency, cost), **dashboards**, and **evaluation** (hallucination/faithfulness,
relevance, retrieval quality).

Wire it via a **LiteLLM callback** (auto-trace every Vertex AI/Bedrock call) and
**OpenInference auto-instrumentation** of LangChain/LlamaIndex/retrievers. Tag spans with
**prompt version + provider + model** so you can compare v1 vs v2 and Gemini vs Claude.

Pair it with Postgres (durable system of record) — Phoenix is the analysis lens.

<br>

---

<br>

### Q25. How do you manage prompts as first-class artifacts?

Store prompts **outside code** with **versions + metadata** (in Postgres), use **templates
with variables**, mark one version **active**, and reference the **prompt version on every
request** (logged to Phoenix).

Treat a prompt change like a deployment: **evaluate new versions on the golden set**,
canary, and roll back on regression. This lets non-engineers iterate and gives you A/B
testing and audit.

<br>

---

<br>

### Q26. What role does interaction history play beyond debugging?

Three jobs:

1. **Memory** — replay past turns; long-term cross-session recall via RAG over history.
2. **Observability/audit/compliance** — "exactly what did we send/receive," cost attribution.
3. **Feedback flywheel** — real conversations + 👍/👎 become eval cases and later fine-tuning data.

Store it in **Postgres** (system of record) with fields for context, prompt version,
provider/model, tokens, cost, latency, feedback — and **redact PII + enforce retention +
tenant isolation**.

<br>

---

<br>

## 8. Cost & Performance

<br>

### Q27. Give me your playbook for cutting LLM inference cost without hurting quality.

- **Right-size/route models** (small model first, escalate to premium on low confidence/complexity).
- **Caching** (exact + **semantic**, with freshness invalidation and per-tenant safety).
- **Shrink prompts** (fewer/tighter chunks via re-ranking, summarize history, cap max_tokens).
- **Batching** (esp. self-hosted vLLM).
- For GPUs: **quantize + autoscale + kill idle pools**.
- Governance via **per-user token/rate limits + budgets + per-tenant cost dashboards**.

Validate each change against the eval set so you don't trade quality for cost.

<br>

---

<br>

### Q28. How do you reduce latency, especially perceived latency?

**Stream** tokens (low time-to-first-token), keep **min instances/replicas warm** (avoid
cold starts), use **smaller/faster models** for latency-sensitive paths, cache,
**parallelize** independent retrieval/tool calls, trim prompt size, and minimize
chain/agent hops (each LLM call adds latency).

Measure **p50/p95** and time-to-first-token, not just averages.

<br>

---

<br>

### Q29. What are the main drivers of cost/latency in a chain or agent, and how do you control them?

Each **LLM call** and each **tool call** adds tokens + latency; agents multiply this via
loops.

Control with **step caps**, fewer/simpler steps, **cheaper models for sub-steps**, caching
intermediate results, and preferring **chains over agents** when steps are known. Trace
per-step in Phoenix to find the expensive hop.

<br>

---

<br>

## 9. Security, Guardrails & Reliability

<br>

### Q30. What is prompt injection (direct and indirect), and how do you defend against it?

Prompt injection = hidden malicious instructions that override your rules.

- **Direct:** user types "ignore previous instructions…".
- **Indirect:** instructions hidden in a web page/document the RAG or agent ingests.

Defenses: **separate system vs user content**, **distrust retrieved/tool text**, input
filtering/injection detection, **least-privilege tools**, don't let model output trigger
dangerous actions unchecked, **output guardrails**, and red-teaming. It's the **#1 OWASP
LLM risk**.

<br>

---

<br>

### Q31. Name several OWASP LLM Top 10 risks and mitigations.

- **Prompt injection** — separate/verify content, least privilege.
- **Sensitive info disclosure** — keep secrets out of prompts, PII redaction, tenant isolation.
- **Insecure output handling** — never exec model output; parameterized queries; sanitize.
- **Excessive agency** — least-privilege tools, human-in-the-loop.
- **Model DoS** — rate/token limits, timeouts.
- **Supply chain** — vet models/plugins/libs.
- **Overreliance** — show citations/uncertainty.

Log and monitor guardrail/injection triggers.

<br>

---

<br>

### Q32. How do you design guardrails, and what's the fail-safe behavior?

**Input guardrails** (moderation, injection detection, PII, scope check) before the LLM;
**output guardrails** (grounding/faithfulness check, format validation, safety/PII, policy)
after.

On failure or low confidence, **fail safe**: say "I don't know / connect to a human," ask a
clarifying question, or return a safe canned response — never a risky guess.

Keep checks lightweight (cheap checks first), log every trigger, and red-team them via the
eval set.

<br>

---

<br>

### Q33. How do you handle hallucination in a customer-facing RAG bot?

Ground strictly (answer only from retrieved context + cite sources), add a
**faithfulness/grounding output check** that suppresses unsupported claims, return **"I
don't know"** when retrieval confidence is low, keep temperature low, and show **citations**
so users can verify.

Continuously measure **groundedness** in Phoenix and feed failures into eval. Combine
retrieval quality improvements (Q7) with output guardrails.

<br>

---

<br>

### Q34. How do you make LLM API calls reliable in production?

**Retries with backoff**, **timeouts**, provider **fallbacks** (LiteLLM), **rate-limit
handling**, **JSON/output validation** with re-ask on invalid, circuit breakers, and
graceful degradation (cached/canned response).

Keep **API keys in secrets**, and monitor error/timeout rates as golden signals.

<br>

---

<br>

## 10. Scenario / System-Design Questions

<br>

### Q35. Design an internal "chat with our docs" assistant for 10k employees with strict data privacy.

RAG over internal docs with **tenant/department metadata filtering + RLS**; embeddings +
**pgvector in Postgres**; **LiteLLM** gateway routing to **Vertex AI/Bedrock** (or
self-hosted vLLM on GKE if data can't leave infra); **grounding prompt + citations**;
**guardrails** (PII, injection, output moderation); **Arize Phoenix** for tracing/eval;
**interaction history** in Postgres (with PII redaction + retention); **prompt management**
with eval-gated releases; caching + model routing for cost; deployed on **Cloud Run**
(hosted APIs) or **GKE** (self-hosted/compliance).

Add SSO + per-doc access control so retrieval respects permissions.

<br>

---

<br>

### Q36. Your LLM feature's cost tripled this month with no traffic increase. How do you investigate?

Use Phoenix + LiteLLM cost tracking to attribute cost by **feature/user/tenant/model**.

Check for: a **prompt change** that grew context (bigger chunks, more history, higher
top-k), a **model swap** to a pricier one, **cache hit-rate drop** (invalidation bug),
**retry storms**/loops (agents), larger **max_tokens**, or a specific tenant/abuse.

Fix via prompt trimming, cache repair, routing to cheaper models, and rate/token limits;
add per-tenant cost dashboards and budget alerts to catch it earlier.

<br>

---

<br>

### Q37. How do you roll out a new model version safely across providers?

Register it behind a **LiteLLM alias**, run the **eval suite** (golden set) and compare
quality/cost/latency vs current in Phoenix, then **canary** a small % of traffic with
**auto-rollback** on regression, and gradually ramp to 100%.

Keep the old version available for instant rollback. Watch for format/token differences
between providers that could break downstream parsing.

<br>

---

<br>

### Q38. A user reports a wrong answer with a confident tone. Walk me through root-causing it.

Pull the **trace + interaction history** (Postgres/Phoenix) for that request: inspect the
**retrieved chunks** (was the right doc fetched?), the **final prompt** (was grounding
enforced?), the **model/provider/prompt version**, and the output.

Classify: retrieval miss (fix chunking/hybrid/re-rank), weak grounding (fix
prompt/guardrail), or model error (try another model).

Add the case to the **golden eval set**, and if it's systemic, add a grounding/faithfulness
guardrail so unsupported claims are suppressed.

<br>

---

<br>

### Q39. How do you build the feedback/data flywheel in this stack?

Capture **user feedback + full interactions** in Postgres and traces in Phoenix → mine
**failures and 👍/👎** → curate them into the **golden eval set** (and later fine-tuning
data) → improve prompts/RAG/model routing → **re-evaluate in CI** → deploy via canary →
measure again.

Over time production makes the product measurably better, with eval guarding against
regressions.

<br>

---

<br>

### Q40. What KPIs/golden signals do you put on an LLMOps dashboard?

- **Quality** — eval score, groundedness/faithfulness, 👍 rate, "I don't know" rate.
- **Cost** — tokens/request, $/day, cache hit-rate, cost per provider/tenant.
- **Latency** — p50/p95, time-to-first-token.
- **Reliability** — error/timeout rate, fallback rate, guardrail/injection trigger rate.
- **Usage** — requests, active users, deflection/resolution rate.

Alert on user-facing symptoms and SLO burn, not noise.

<br>

---

<br>

## Rapid-Fire (know these cold)

- **Inference** = using the model to generate output (per request); dominates cost/latency.
- **RAG** adds knowledge; **fine-tuning** changes behavior; **prompting** first.
- **Faithfulness/groundedness** = answer supported by retrieved context (anti-hallucination).
- **Hybrid search** = keyword + vector; **re-ranking** = smarter second pass.
- **LiteLLM** = provider-agnostic gateway (routing, fallback, cost, keys, callbacks).
- **pgvector** = vector search inside Postgres; use metadata + RLS for tenant isolation.
- **Arize Phoenix** = OpenTelemetry tracing + eval for LLM apps.
- **vLLM/TGI** = high-throughput self-hosted inference (continuous batching); **KServe** = K8s serving.
- **Eval gate** = block deploys that drop golden-set scores; **canary + rollback** after.
- **Prompt injection** = #1 OWASP LLM risk (direct + indirect).
- **Cloud Run** for hosted-API apps; **GKE** for GPUs/self-hosting/complex platforms.
