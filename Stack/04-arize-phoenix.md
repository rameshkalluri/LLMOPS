# Arize Phoenix — Observability & Evaluation

## What is Arize Phoenix?
**Arize Phoenix** is an **open-source observability & evaluation tool for LLM apps**. It
**traces** every step of a request (prompt, retrieved context, model call, response,
tokens, latency) and helps you **evaluate** quality — so you can see **why** an answer was
good or bad.

> **Analogy:** Phoenix is the **CCTV + quality inspector** in the restaurant. It records
> every order end-to-end (what was asked, which notes were used, what the kitchen cooked,
> how long it took) and **grades the dishes** so you can spot problems and improve.

**Where it fits:** Day 5 (observability) and Day 4 (evaluation). It's your **"how is it
doing?" layer**.

---

## What Phoenix gives you

### 1. Tracing (follow one request through every step) 🔍
Built on **OpenTelemetry / OpenInference**, Phoenix captures a **trace** across your
chain/agent: retrieve → build prompt → LLM (Vertex AI/Bedrock) → tools → response.

> **Analogy:** A **package-tracking timeline** for each request — see every stop and how
> long each took, and open any step to inspect the exact prompt/response.

### 2. Monitoring & dashboards 📊
Aggregate **latency, token usage, cost, error rates**, and quality over time — the
LLMOps golden signals (Day 5.1).

### 3. Evaluation ⚖️
Run **LLM-as-a-judge** and RAG metrics (hallucination/faithfulness, relevance, retrieval
quality) on traced data or a golden set (Day 4.1) — right where you can see the traces.

> **Analogy:** The inspector doesn't just watch — they **score each dish against a rubric**
> and flag the bad ones for retraining.

---

## How Phoenix plugs into YOUR stack

```
Your App (RAG/agent)
   │  (auto-instrumented via OpenInference / OpenTelemetry)
   ├─ LiteLLM  ──► success/failure callback ──► Phoenix   (every model call traced)
   ├─ Vector store retrieval  ──► span ──────► Phoenix     (what chunks were fetched)
   └─ Model response          ──► span ──────► Phoenix     (answer, tokens, latency, cost)
                                                   │
                                          Traces + Evals + Dashboards
```

- **Via LiteLLM callback:** set Phoenix as a callback so **every** Vertex AI/Bedrock call
  is traced automatically — no per-call code.
- **Via auto-instrumentation:** OpenInference instrumentors trace LangChain/LlamaIndex,
  retrieval, and provider SDKs.

```python
# Concept: instrument the app so traces flow to Phoenix
from phoenix.otel import register
tracer_provider = register(project_name="my-llm-app")   # points to your Phoenix instance
# LangChain/LlamaIndex/OpenAI instrumentors then auto-send spans
```
```yaml
# In LiteLLM proxy config, forward traces to Phoenix
litellm_settings:
  success_callback: ["arize_phoenix"]
  failure_callback: ["arize_phoenix"]
```

> **Phoenix + Postgres:** you store the durable **interaction history** in Postgres
> (next note); Phoenix is your **analysis/observability lens** over that activity. They
> complement each other.

---

## Phoenix vs other tools (quick context)
- **Phoenix (Arize)** — open-source, self-hostable, OpenTelemetry-native, strong on RAG
  eval; great for dev + production tracing.
- Alternatives you'll hear about: **Langfuse**, **LangSmith** (similar space). Your stack
  uses **Phoenix**.

---

## Practical tips (LLMOps)
- Trace **prompt version + model + provider** on each span → compare Vertex AI vs Bedrock,
  and prompt v1 vs v2.
- Track **cost + latency per provider/model** to drive LiteLLM routing decisions (Day 5.4).
- Turn traced failures into **eval cases** → the **feedback flywheel** (Day 5.1).
- Watch **groundedness/hallucination** metrics for your RAG answers.
- Redact **PII** before sending spans (Day 5.3).

---

## TL;DR (in plain English)
- **Arize Phoenix = CCTV + quality inspector**: it **traces** every request end-to-end and
  **evaluates** answer quality (open-source, OpenTelemetry-based).
- Plug it in via a **LiteLLM callback** (auto-trace all Vertex AI/Bedrock calls) and/or
  **OpenInference auto-instrumentation** of your RAG/agent.
- It covers the **observability + eval** layers (Days 4–5); pair it with **Postgres** for
  durable history.
- Use it to compare **providers/prompts**, watch **cost/latency/groundedness**, and feed
  failures back into your **eval set**.
