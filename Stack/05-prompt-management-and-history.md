# Prompt Management & Interaction History

Two disciplines that turn a demo into real LLMOps: **managing prompts like code** and
**recording every interaction**.

> **Analogy:** In the restaurant, **prompt management = the versioned recipe book** (every
> recipe has a version, and you can revert to last week's). **Interaction history = the
> guest logbook** (who ordered what, and what you served) — the raw material for improving
> recipes and remembering regulars.

---

## Part A — Prompt Management 📖

### What it is
Storing your prompts **outside the code**, with **versions, metadata, and history**, so
you can edit, test, roll back, and compare them — without redeploying the app.

**Where it fits:** Day 1 (prompt engineering) + Day 5 (versioning / CI-CD).

### Why it matters
- A **prompt change is a deployment** — it can change quality, cost, and safety.
- You need to **A/B test** and **roll back** prompts like code.
- Non-engineers (PMs, domain experts) can **iterate on prompts** without touching code.

> **Analogy:** You wouldn't change a **signature recipe** with no version history and no
> taste test. Same for prompts.

### What to store per prompt
```
prompt_id, name, version, template_text, variables,
model/settings hints, created_by, created_at, status (draft/active), notes
```
- Use **templates with variables** (Day 1.4): `"{context}"`, `"{question}"`.
- Mark one version **active**; keep old ones for rollback/comparison.

### In your stack
- Store prompt versions in **Postgres** (a `prompts` table) — same DB as history/vectors.
- Reference the **prompt version on each request** and log it to **Arize Phoenix** so you
  can compare **v1 vs v2** quality/cost.
- (Optional) LiteLLM and some platforms offer prompt features, but a simple **Postgres
  table + your app** is enough and keeps control in your hands.

```sql
CREATE TABLE prompts (
    id           BIGSERIAL PRIMARY KEY,
    name         TEXT,
    version      INT,
    template     TEXT,
    is_active    BOOLEAN DEFAULT FALSE,
    metadata     JSONB,
    created_at   TIMESTAMPTZ DEFAULT now()
);
```

### LLMOps flow (ties to Day 5 CI/CD)
```
Edit prompt → new version (draft) → evaluate on golden set (Day 4) via Phoenix
→ pass? mark active → serve → monitor → roll back if quality/cost regresses
```

---

## Part B — Interaction History 📝

### What it is
A durable record of **every conversation**: user input, retrieved context, final prompt,
model response, provider/model used, prompt version, tokens, cost, latency, and user
feedback.

**Where it fits:** Day 3 (memory) + Day 5 (observability + feedback flywheel).

### Why it matters (three big jobs)
1. **Memory (Day 3)** — replay past turns so multi-turn chat works; power long-term,
   cross-session memory.
2. **Observability/audit (Day 5)** — "what exactly did we send and get?" for debugging,
   compliance, and cost attribution.
3. **Feedback flywheel (Day 5)** — real conversations + thumbs-up/down become your **eval
   set** and (later) **fine-tuning data**.

> **Analogy:** The **guest logbook**: it lets the intern remember returning customers
> (memory), lets managers review what happened (audit), and turns real complaints into
> **new training flashcards** (flywheel).

### What to store per interaction
```
session_id, user_id, timestamp,
user_message, retrieved_chunks, final_prompt, prompt_version,
provider/model (vertex_ai/bedrock), response,
tokens_in/out, cost, latency, tool_calls,
guardrail_flags, user_feedback (👍/👎, correction)
```
- Store in **Postgres** (a `conversations`/`messages` table).
- Mirror key events to **Arize Phoenix** for tracing/eval dashboards.

```sql
CREATE TABLE interactions (
    id             BIGSERIAL PRIMARY KEY,
    session_id     UUID,
    user_id        TEXT,
    user_message   TEXT,
    context        JSONB,        -- retrieved chunks + sources
    prompt_version INT,
    provider       TEXT,         -- 'vertex_ai' | 'bedrock'
    model          TEXT,
    response       TEXT,
    tokens_in      INT,
    tokens_out     INT,
    cost_usd       NUMERIC,
    latency_ms     INT,
    feedback       TEXT,         -- 'up' | 'down' | correction
    created_at     TIMESTAMPTZ DEFAULT now()
);
```

### Postgres vs Phoenix for history (they pair up)
- **Postgres** = the **durable, queryable system of record** (your data, retention, joins,
  memory lookups, tenant isolation).
- **Arize Phoenix** = the **observability/eval lens** (traces, dashboards, scoring).
- Use **both**: write history to Postgres, send traces/evals to Phoenix.

### Privacy note (Day 5.3)
- **Redact PII** before storing/tracing; set **retention** policies; enforce **tenant
  isolation** (user A can't see user B's history).

---

## TL;DR (in plain English)
- **Prompt management = a versioned recipe book**: store prompts (with versions) in
  **Postgres**, evaluate new versions (Phoenix) before making them active, and **roll back**
  like code.
- **Interaction history = the guest logbook**: record input, context, prompt version,
  provider/model, response, tokens, cost, latency, and feedback in **Postgres**.
- History powers **memory (Day 3)**, **audit/observability (Day 5)**, and the **feedback
  flywheel** (turn real chats into eval/fine-tuning data).
- **Postgres = system of record; Arize Phoenix = observability lens** — use them together,
  and **redact PII + isolate tenants**.
