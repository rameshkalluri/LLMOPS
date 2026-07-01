# CI/CD & Putting It All Together

## Why CI/CD is different for LLM apps
In normal software, tests are pass/fail. For LLM apps, a change (new prompt, model, or
retrieval setting) can **silently lower quality**. So the pipeline must run **evaluation**
as a **quality gate** before deploying.

> **Analogy:** You don't promote the intern based on vibes. Before they handle real
> customers, they must **pass the standard exam** (eval on the golden set). Fail → no
> promotion (no deploy).

---

## Version everything 📌
Treat these as versioned artifacts (in Git or a registry):
- **Prompts** (a prompt change *is* a deployment).
- **Model + settings** (model name, temperature, top-p).
- **Retrieval config** (chunking, top-k, embeddings model).
- **Eval datasets** and **thresholds**.
- **App code + Dockerfile + K8s manifests**.

> **Analogy:** Keep a **paper trail** of exactly how the intern was trained and instructed
> for each release — so you can reproduce or roll back.

---

## The CI/CD pipeline (with an eval gate)
```
1. Commit change (prompt / code / model / retrieval)
2. CI: build container + unit tests
3. Run EVALUATION on the golden set (Ragas / LLM-judge)  ← quality gate
      ├─ scores hold/improve? → continue
      └─ scores drop?         → FAIL the build (block deploy)
4. Deploy to staging → smoke tests
5. Canary release (send new version a small % of traffic)
6. Watch metrics (quality, cost, latency, errors)
      ├─ healthy? → roll out to 100%
      └─ bad?     → auto-rollback
```

> **Analogy:** Let the **new intern handle 5% of calls** first; if complaints spike, pull
> them back immediately.

---

## Deploy targets (from Day 4)
- **Cloud Run** — `gcloud run deploy` (with traffic splitting for canary).
- **GKE** — `kubectl apply` / GitOps (**Argo CD**, Cloud Build); rolling updates + rollback.
- Tools: **Cloud Build**, GitHub Actions, GitLab CI, Argo CD, Jenkins.

---

## The complete LLMOps picture 🗺️
```
        ┌──────────────── Build & Customize ─────────────────┐
Day 1   │  Prompting (clear instructions)                    │
Day 2   │  RAG (open-book: retrieve your docs)               │
Day 3   │  Orchestration, Agents/Tools, Fine-tuning          │
        └───────────────────────┬────────────────────────────┘
                                 ▼
        ┌──────────────── Ship & Operate ────────────────────┐
Day 4   │  Evaluate → Package (FastAPI/Docker) →              │
        │  Deploy (Cloud Run / GKE, GPUs via vLLM/TGI)        │
Day 5   │  Observe → Guardrails → Security → Cost → CI/CD     │
        └───────────────────────┬────────────────────────────┘
                                 ▼
                    Feedback flywheel: production
                    failures → eval set → improve → repeat
```

---

## Production readiness checklist ✅
- [ ] Prompts/model/retrieval **versioned** in Git.
- [ ] **Golden eval set** + thresholds; eval runs as a **CI gate**.
- [ ] App is an **API in a container**, deployed to **Cloud Run/GKE**.
- [ ] **Secrets** in Secret Manager; least-privilege identities.
- [ ] **Observability**: tracing, golden-signal dashboards, feedback capture.
- [ ] **Guardrails** (input+output) and **security** (OWASP LLM Top 10) in place.
- [ ] **Cost controls**: caching, model routing, rate/token limits, budgets.
- [ ] **Canary + rollback** on deploy; alerts on quality/cost/latency.
- [ ] **Feedback flywheel** wired: prod failures → eval set.

---

## TL;DR (in plain English)
- LLM CI/CD adds an **evaluation gate**: no deploy unless the change **passes the exam**
  on the golden set.
- **Version everything** (prompts, model, retrieval, eval sets, manifests) for
  reproducibility and rollback.
- Ship with **canary + auto-rollback** to Cloud Run/GKE; watch quality, cost, latency.
- End-to-end LLMOps = **Build (prompt/RAG/agents/fine-tune) → Ship (eval/package/deploy) →
  Operate (observe/guard/secure/cost/CI-CD)** — looped by the **feedback flywheel.**
