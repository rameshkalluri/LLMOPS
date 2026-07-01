# LiteLLM — the Gateway

## What is LiteLLM?
**LiteLLM** gives you **one unified interface to 100+ LLM providers** (Vertex AI,
Bedrock, OpenAI, Azure, Anthropic…). You write code **once** in the OpenAI format, and
LiteLLM translates it to whichever provider you point at.

> **Analogy:** LiteLLM is the **universal remote** (or a **head waiter**). Instead of
> learning a different remote for each TV (each provider's SDK), you press the same
> buttons and it talks to **any** of them. Swap Vertex AI ↔ Bedrock without rewiring your app.

**Where it fits:** Day 1 (calling APIs), Day 4 (deployment/gateway), Day 5 (cost,
routing, logging). It's the **front door to all your models**.

---

## Two ways to use it

### 1. Python SDK (in-process)
```python
from litellm import completion

# Same call shape for every provider — just change the model string
resp = completion(
    model="vertex_ai/gemini-1.5-pro",         # Vertex AI
    messages=[{"role": "user", "content": "Hello"}],
)

resp = completion(
    model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",   # Bedrock
    messages=[{"role": "user", "content": "Hello"}],
)
```

### 2. LiteLLM Proxy (a standalone gateway server) ⭐ (common in production)
Run LiteLLM as a **service** that all your apps call (OpenAI-compatible endpoint). This
centralizes keys, routing, cost, and logging in **one place**.

```yaml
# config.yaml (proxy)
model_list:
  - model_name: gemini-pro                       # a friendly alias your app uses
    litellm_params:
      model: vertex_ai/gemini-1.5-pro
  - model_name: claude                            # another alias
    litellm_params:
      model: bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0

litellm_settings:
  success_callback: ["arize_phoenix"]             # send traces to Phoenix (see Phoenix note)
```
```bash
litellm --config config.yaml     # starts the gateway; apps call it like OpenAI
```

> **Analogy:** The **proxy** is the **central switchboard** for the whole company —
> every call goes through it, so you manage keys, budgets, and logs in one room.

---

## Why LiteLLM is powerful for your stack

| Feature | What it does | LLMOps value |
|---|---|---|
| **Unified API** | One format for Vertex AI + Bedrock + others | Swap models with a string change |
| **Fallbacks** | If Vertex AI fails/rate-limits → try Bedrock | Resilience, uptime |
| **Load balancing / routing** | Spread traffic; route cheap vs premium | Cost + performance (Day 5) |
| **Virtual keys + budgets** | Per-team keys, spend limits, rate limits | Governance + cost control |
| **Cost tracking** | Logs tokens + $ per request | Observability (Day 5) |
| **Caching** | Reuse identical/similar responses (Redis) | Cost savings (Day 5.4) |
| **Callbacks/logging** | Send data to **Arize Phoenix**, Langfuse, etc. | Observability (Day 5.1) |

> This is exactly why you have **both Vertex AI and Bedrock**: LiteLLM lets you use them
> interchangeably, **fall back** between them, and **route** by cost/quality.

---

## LiteLLM + Postgres
The LiteLLM **proxy uses Postgres** to store **virtual keys, spend/usage, and config** —
so your Postgres (next note) also backs the gateway's governance features.

> **Analogy:** The switchboard keeps its **ledger of who called and how much they owe** in
> the filing cabinet (Postgres).

---

## LiteLLM + Arize Phoenix
Add Phoenix as a **success/failure callback** and every model call is **automatically
traced** (prompt, response, tokens, latency, cost) — no per-call code needed. (Details in
the Phoenix note.)

---

## Practical tips
- Use **model aliases** (`gemini-pro`, `claude`) so app code never hardcodes a provider.
- Configure **fallbacks** (Vertex AI → Bedrock) for resilience.
- Keep **provider credentials in the proxy/secrets**, not in each app (Day 5 security).
- Turn on **cost tracking + Phoenix callbacks** from day one.
- Set **per-key budgets + rate limits** to prevent runaway spend/DoS.

---

## TL;DR (in plain English)
- **LiteLLM = universal remote / head waiter**: one OpenAI-style interface to **Vertex AI,
  Bedrock, and more** — swap providers with a string.
- Run it as a **proxy/switchboard** to centralize **keys, budgets, routing, fallbacks,
  cost tracking, caching, and logging**.
- It uses **Postgres** for keys/spend and sends **traces to Arize Phoenix** — tying your
  whole stack together.
- It's the reason having **both Vertex AI + Bedrock** is easy: **fallback and route** between them.
