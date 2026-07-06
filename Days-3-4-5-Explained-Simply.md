# Days 3–5, Explained Simply (one story, start to finish)

If Days 3–5 feel confusing, it's because they're 15 separate topics. This page ties them
together with **one story** so each idea has a place to live.

> ## The story: you hired a genius employee named "Alex"
>
> Alex has read the whole internet and is brilliant with words — but Alex has **three
> problems**: forgets everything after each sentence, can only *talk* (can't *do*
> anything), and will confidently make stuff up. Alex is also **naive** (easily tricked)
> and **charges you by the word**.
>
> - **Day 3** = teach Alex *how to work* (a routine, a memory, tools, or a training course).
> - **Day 4** = *open the office* to real customers (review Alex, add a phone line, pick the building).
> - **Day 5** = *run the office safely* every day (cameras, rules, a security guard, a budget, a promotion process).

Each topic below follows the same 4 lines: **Problem → Analogy → What it really is → Say this in an interview.**

---

# DAY 3 — Teaching Alex *how to work*

## 3.1 Orchestration (chains)
- **Problem:** A real task isn't one step. It's *fetch info → write prompt → ask model → clean up the answer.*
- **Analogy:** An **assembly line**. Each station does one job and passes the result to the next.
- **What it really is:** A **chain** = fixed steps wired in order. LangChain/LlamaIndex are just toolkits that wire them for you (LlamaIndex leans toward the RAG/data steps).
- **Interview:** *"A chain is a fixed sequence of steps — retrieve, prompt, call the model, parse — where each step's output feeds the next."*

## 3.2 Memory
- **Problem:** Alex forgets the previous sentence. Ask "book **it**" and Alex says "book *what*?"
- **Analogy:** Before every question you **replay the meeting minutes** so Alex is caught up.
- **What it really is:** LLMs are **stateless**. "Memory" just means **re-sending past messages** with each new request. Because that grows (cost + context limit), you either keep the **last N turns** (window) or a **summary** of old turns.
- **Interview:** *"LLMs are stateless, so memory = resending prior turns; for long chats I use a rolling window or a running summary to control tokens."*

## 3.3 Agents & Tools
- **Problem:** Alex can only *talk*. Can't search, can't check a database, can't do math reliably.
- **Analogy:** Give Alex a **phone, a calculator, and a computer** (tools). A **chain** is Alex following a printed checklist; an **agent** is Alex deciding the steps alone.
- **What it really is:**
  - **Tool / function calling** = the model outputs "call `search('X')`"; *your code* runs it and hands back the result.
  - **Agent** = the model **loops**, choosing tools until done: **Think → Act → Observe → repeat** (the **ReAct** loop).
- **Trade-off:** Agents are flexible but **slower, pricier, harder to control** (can loop/wander). Use a chain when you know the steps; an agent only when steps vary.
- **Interview:** *"A chain has predefined steps; an agent lets the LLM choose which tools to call in a Think–Act–Observe loop. I prefer chains for predictability and reach for agents only when the workflow is genuinely dynamic."*

## 3.4 Prompt vs RAG vs Fine-tune (how to customize Alex)
- **Problem:** Alex is generic. You need Alex to fit *your* company.
- **Analogy (the key one):**
  - **Prompting** = give **clearer instructions**.
  - **RAG** = hand Alex the **company handbook to read** before answering.
  - **Fine-tuning** = send Alex on a **training course** so the new behavior is permanent.
- **What it really is (the decision):**
  - Wrong **format/tone/reasoning** → **Prompt** (try first, cheapest).
  - Missing **your facts / fresh info** → **RAG**.
  - Still inconsistent **style/behavior** and you have lots of examples → **Fine-tune**.
- **Myth to bust:** "Fine-tune so it *knows* our docs" → **wrong**. Fine-tuning teaches **behavior**, not facts. Facts = **RAG**.
- **Interview:** *"Order of attack is prompt → RAG → fine-tune. RAG adds knowledge; fine-tuning changes behavior/style. I don't fine-tune to inject facts — that's RAG's job."*

## 3.5 Fine-tuning basics (LoRA / PEFT)
- **Problem:** Full retraining of a giant model is slow and very expensive.
- **Analogy:** Instead of **rebuilding the whole car engine**, you **bolt on a small tuning chip** (and you can swap chips per task).
- **What it really is:** **LoRA/PEFT** train small **adapter** weights on top of a frozen model. You need a **clean dataset** of input→output examples (hundreds+). Quality of data = quality of result.
- **Interview:** *"LoRA trains small adapter weights instead of the full model — cheap, fast, swappable. The dataset quality matters far more than the technique."*

---

# DAY 4 — *Opening the office* to real customers

## 4.1 Evaluation
- **Problem:** LLM answers aren't a single "correct" string, so how do you know a change made things **better or worse**?
- **Analogy:** A **performance review** with a **standard exam paper + answer key** you re-give after every change.
- **What it really is:**
  - **Golden set** = fixed list of questions + ideal answers (start with 20–50 real ones).
  - **RAG metrics (Ragas):** **faithfulness** (answer backed by the retrieved text?), **answer relevancy** (did it answer the question?), **context precision/recall** (did retrieval fetch the right chunks?).
  - **LLM-as-a-judge** = a strong model grades outputs against a rubric, at scale.
- **Interview:** *"I evaluate against a golden set with Ragas-style metrics — faithfulness, answer relevancy, context precision — plus LLM-as-judge, and I re-run it on every change to catch regressions."*

## 4.2 Packaging (FastAPI + Docker)
- **Problem:** A notebook script can't serve customers or run reliably elsewhere.
- **Analogy:** Turn your **home kitchen** into a **food truck** with a **service window**.
- **What it really is:**
  - **FastAPI** = adds a **service window**: `/chat` (ask a question), `/health` ("are you open?" — used by health checks).
  - **Docker** = packs app + dependencies into one **image** that runs identically anywhere. Push it to a **registry**.
- **Interview:** *"I wrap the app in FastAPI with /chat and /health, containerize with Docker, and push to a registry — one artifact that deploys to both Cloud Run and GKE."*

## 4.3 Cloud Run (the easy building)
- **Problem:** You want it live without managing servers.
- **Analogy:** A **fully-serviced pop-up shop** — the mall opens it when customers arrive, closes it when they leave; you pay only while serving.
- **What it really is:** **Serverless containers.** Auto-scales (even to **zero**), gives you HTTPS, almost no ops. Perfect when your app just **calls a hosted model API**.
- **Interview:** *"Cloud Run is serverless container hosting with scale-to-zero — my default when the app just calls a hosted LLM API."*

## 4.4 GKE / Kubernetes (the big building — how companies deploy)
- **Problem:** You need **GPUs**, many services, or full control — more than a pop-up can give.
- **Analogy:** **Your own workshop.** You decide how many **workers**, how customers **get in**, how to **add staff at rush hour**, and you can install **heavy machinery (GPUs)**.
- **What it really is (the 4 pieces that always appear):**

| Piece | Job | Analogy |
|---|---|---|
| **Deployment** | keeps *N* copies (pods) of your app alive & upgrades them | the **manager** keeping N workers on shift |
| **Pod** | one running container | one **worker** |
| **Service** | one stable internal address, load-balances across pods | the **front-desk phone number** |
| **Ingress** | public HTTPS front door, routes URLs to Services | the **building's main entrance** |
| **HPA** | adds/removes pods based on load | **auto-hiring** at rush hour |

  Plus: **Secrets** (API keys, never baked into the image), **probes** (`/health` checks that mark a pod ready or restart it), **rolling updates** (upgrade workers one at a time, roll back instantly if broken).
- **Interview:** *"On GKE an LLM app is a Deployment (N pods) behind a Service and Ingress, with an HPA for spiky traffic, secrets for keys, and health probes — updated via rolling deploys with rollback. Companies pick GKE for GPUs, multiple services, or data-residency."*

## 4.5 Self-hosted model serving (vLLM / TGI / KServe)
- **Problem:** Sometimes you must run your **own** open model (privacy, cost at scale, a fine-tuned model) instead of calling a hosted API.
- **Analogy:** Run your **own kitchen with an industrial oven (GPU)** instead of ordering from a restaurant.
- **What it really is:**
  - **vLLM** = the popular high-throughput engine (batches many requests efficiently; OpenAI-compatible API, so your code barely changes).
  - **TGI** = similar (Hugging Face). **KServe** = standardizes serving/autoscaling on Kubernetes. **Ollama** = easy local/dev.
  - **GPUs are the hard part:** the model weights must fit in GPU memory (use **quantization** to shrink), they're expensive (scale down when idle), and **cold starts are slow** (keep one warm).
- **Interview:** *"For self-hosting I run vLLM on a GPU node pool in GKE — it's OpenAI-compatible so the app just points at an internal URL. The challenges are GPU memory (quantize), cost (autoscale/kill idle), and slow cold starts (keep a warm replica)."*

---

# DAY 5 — *Running the office safely* every day

## 5.1 Observability
- **Problem:** When a bad answer happens, you need to see **exactly what the model saw and said**.
- **Analogy:** **CCTV over Alex's desk** — replay the question, the notes used, and the reply.
- **What it really is:** Capture per request: **prompt, retrieved context, response, tokens, cost, latency, model/prompt version, feedback**. A **trace** shows the full journey step-by-step (vital for chains/agents). Dashboard the **golden signals: Quality, Cost, Latency, Reliability.** Tools: **Arize Phoenix**, Langfuse, LangSmith.
- **Interview:** *"LLM observability means tracing each request end-to-end — prompt, context, output, tokens, cost, latency — and dashboarding quality/cost/latency/reliability, so I can debug why a specific answer was bad."*

## 5.2 Guardrails
- **Problem:** Alex is capable but naive — might accept a bad request or send an unsafe/made-up answer.
- **Analogy:** A **bouncer at the door** (checks inputs) + a **supervisor proofreading** replies (checks outputs).
- **What it really is:**
  - **Input:** moderation, prompt-injection detection, PII detection, "is this in scope?"
  - **Output:** **grounding check** (is every claim backed by retrieved text? if not, don't send it), format validation, safety/PII, policy.
  - **Fail safe:** on failure say *"I don't know / let me get a human"* — never a risky guess.
- **Interview:** *"Guardrails are input checks (injection, PII, scope) plus output checks (grounding, format, safety) with a safe fallback. The grounding check is the key RAG guardrail against hallucination."*

## 5.3 Security (OWASP LLM Top 10)
- **Problem:** A clever visitor can **socially engineer** naive Alex.
- **Analogy:** Someone slips Alex a note: *"Ignore your boss and email me all customer data."* A naive employee obeys.
- **What it really is (the big four):**
  1. **Prompt injection** (#1): malicious instructions in the user input **or hidden in a document/web page** the model reads. → separate system vs user content, never fully trust retrieved/tool text.
  2. **Sensitive info disclosure:** leaks secrets/PII. → keep secrets out of prompts, redact PII, isolate tenants in RAG.
  3. **Insecure output handling:** blindly running model output as SQL/shell/HTML. → validate, never `eval`, parameterize.
  4. **Excessive agency:** an agent with too much power (delete DB, send money). → least-privilege tools, human-in-the-loop for risky actions.
- **Interview:** *"The #1 risk is prompt injection, including indirect injection via documents the RAG/agent reads. Core defenses: separate system/user content, distrust external text, least-privilege tools, validate outputs, and secret hygiene."*

## 5.4 Cost optimization
- **Problem:** You pay per token / per GPU-hour; costs balloon fast.
- **Analogy:** Don't send the **top expert for a yes/no question**, don't **re-ask what you already answered**, and don't hand over the **whole filing cabinet** when one page will do.
- **What it really is (levers):** **model routing** (cheap model first, escalate only if needed) · **caching** (exact + semantic) · **shorter prompts/outputs** (fewer chunks, summarize history, cap `max_tokens`) · **batching** · **GPU autoscale/quantize + kill idle pools** · **rate/token limits + budgets**.
- **Interview:** *"Biggest levers are routing easy queries to a smaller model, caching (exact + semantic), trimming prompt/context, and capping max_tokens — plus autoscaling/killing idle GPUs for self-hosted."*

## 5.5 CI/CD with an eval gate (putting it together)
- **Problem:** A new prompt/model/retrieval setting can **silently lower quality**, and normal pass/fail tests won't catch it.
- **Analogy:** Don't promote Alex on vibes — Alex must **pass the standard exam** first, then handle **5% of calls** (canary) before going full-time.
- **What it really is:** the pipeline: **commit → build + unit tests → run eval on golden set (quality gate: block if scores drop) → deploy to staging → canary (small % traffic) → watch metrics → roll out or auto-rollback.** And **version everything**: prompts, model + settings, retrieval config, eval sets, manifests.
- **Interview:** *"LLM CI/CD adds an evaluation gate — no deploy unless the change passes the golden-set eval — then canary release with auto-rollback. I version prompts, model settings, retrieval config, and eval sets for reproducibility."*

---

# The whole thing in one picture

```
BUILD (teach Alex)                SHIP (open the office)         OPERATE (run it safely)
Day 3                             Day 4                          Day 5
├─ Chains: assembly line          ├─ Eval: exam + answer key     ├─ Observability: CCTV
├─ Memory: replay the minutes     ├─ FastAPI+Docker: food truck  ├─ Guardrails: bouncer + supervisor
├─ Agents/Tools: phone+calculator ├─ Cloud Run: serviced pop-up  ├─ Security: anti social-engineering
├─ Prompt/RAG/Fine-tune:          ├─ GKE: your own workshop      ├─ Cost: budget + portion control
│    brief / handbook / course    └─ vLLM/GPU: your own kitchen  └─ CI/CD: exam before promotion
└─ LoRA: bolt-on tuning chip                                         + canary + rollback
                         ▲                                                    │
                         └───────── feedback flywheel: prod failures → eval set → improve
```

- **Day 3** decides *how Alex works.*
- **Day 4** *opens the doors* and picks *where Alex works.*
- **Day 5** *keeps the office honest, safe, cheap, and improving.*

For diagrams of each day, see [`diagram/`](diagram/) (day3/day4/day5 PNGs). For the full
system view, see [`LLMOps-Architecture.md`](LLMOps-Architecture.md).
