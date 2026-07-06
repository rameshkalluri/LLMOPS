# Days 1–5, Explained Simply (one story, start to finish)

If the 5 days feel confusing, it's because they're ~25 separate topics. This page ties
them together with **one story** so each idea has a place to live.

> ## The story: you hired a genius employee named "Alex"
>
> Alex has read the whole internet and is brilliant with words — but Alex has **three
> problems**: forgets everything after each sentence, can only *talk* (can't *do*
> anything), and will confidently make stuff up. Alex is also **naive** (easily tricked)
> and **charges you by the word**.
>
> - **Day 1** = learn *how to talk to Alex* (words, knobs, clear briefs) — and how Alex thinks.
> - **Day 2** = give Alex the *company handbook to read* before answering (RAG).
> - **Day 3** = teach Alex *how to work* (a routine, a memory, tools, or a training course).
> - **Day 4** = *open the office* to real customers (review Alex, add a phone line, pick the building).
> - **Day 5** = *run the office safely* every day (cameras, rules, a security guard, a budget, a promotion process).

Each topic below follows the same 4 lines: **Problem → Analogy → What it really is → Say this in an interview.**

---

# DAY 1 — Learning *how to talk to Alex*

## 1.1 What is an LLM?
- **Problem:** What even *is* this thing, and why does it sometimes lie?
- **Analogy:** A **super-powered autocomplete**. Your phone guesses the next word; Alex guesses so well (having read the internet) it can write essays and code.
- **What it really is:** A model that **predicts the next token** over and over. It **predicts**, it doesn't *look up* — that's why it's fluent but can be **wrong** (hallucination). Use **instruct/chat** models (GPT-4o, Claude, Gemini), not raw "base" models.
- **Interview:** *"An LLM predicts the next token repeatedly; it's pattern prediction, not fact lookup, which is why it hallucinates — and why we add RAG and guardrails."*

## 1.2 Tokens & context window
- **Problem:** Why do I get charged weirdly, and why does Alex "forget" long chats?
- **Analogy:** A **token = a pizza slice** (text is cut into slices; you're billed per slice). The **context window = Alex's desk** — only so many papers fit; extras fall off the edge.
- **What it really is:** A token ≈ 4 characters ≈ ¾ of a word. You pay for **input + output** tokens. The **context window** is the max tokens (prompt + answer) the model can see at once. LLMs are **stateless** — nothing is remembered unless you put it back on the desk.
- **Interview:** *"A token is a sub-word unit billed in and out; the context window is the max tokens the model can see at once, and models are stateless so history must be resent."*

## 1.3 Model settings (the knobs)
- **Problem:** Same question, wildly different answers — how do I control it?
- **Analogy:** **Knobs on a stove.** Temperature is the **spice dial**: low = plain/repeatable, high = experimental.
- **What it really is:** **Temperature/top-p** control randomness (keep **low, 0–0.3**, for production/RAG accuracy). **Max tokens** caps answer length (saves money). The **system message** = Alex's **job description taped to the desk** (rules/persona for the whole chat).
- **Interview:** *"Temperature and top-p control randomness — I keep them low for factual/RAG tasks; the system message sets persona and rules; max_tokens caps cost."*

## 1.4 Embeddings
- **Problem:** How can a computer tell that "car" and "automobile" mean the same thing?
- **Analogy:** A giant **map of meaning** where every sentence gets a GPS coordinate. "Dog" and "puppy" land close; "dog" and "bank loan" land far apart.
- **What it really is:** An **embedding** turns text into a **vector of numbers** capturing meaning; similar meaning → nearby vectors (measured by **cosine similarity**). This powers **semantic search** and is the **foundation of RAG** (Day 2).
- **Interview:** *"Embeddings map text to vectors so similar meanings are nearby; we compare with cosine similarity — it's the basis for semantic search and RAG retrieval."*

## 1.5 Prompt engineering
- **Problem:** Vague instructions → random results.
- **Analogy:** **Briefing an intern** with a **recipe card**: ingredients (context), steps (task), and a **photo of the finished dish** (an example of the output you want).
- **What it really is:** Writing clear instructions: **role, task, context, rules, output format, examples.** Key techniques: **few-shot** (show examples), **chain-of-thought** (ask it to reason step by step), **JSON output** (so your code can parse it). Use **templates** and **version prompts** in Git.
- **Interview:** *"Prompt engineering is the cheapest quality lever — I give role/task/context/rules/format, use few-shot and structured JSON output, and version prompts because a prompt change is a deployment."*

## 1.6 Calling APIs & cost
- **Problem:** How do I actually use it, and how do I keep the bill sane?
- **Analogy:** **Texting the intern** — send the job + rules, get an answer, and a **taxi meter** counts the tokens in and out.
- **What it really is:** Send **messages + settings**, get **text + token usage**. **Tokens = money** (input + output). Cut cost with smaller models, shorter prompts, `max_tokens`, and caching. Production basics: **retries, timeouts, JSON validation, secret-managed API keys**, and **streaming** for snappier UX.
- **Interview:** *"You send messages plus settings and get text plus token usage; cost is input+output tokens, so I trim prompts, cap max_tokens, cache, and keep keys in a secret manager with retries and timeouts."*

---

# DAY 2 — Giving Alex the *handbook to read* (RAG)

## 2.1 Why RAG?
- **Problem:** Alex graduated last year (stale), has never seen your private files, and won't admit when unsure.
- **Analogy:** An **open-book exam** — instead of answering from memory, Alex is handed the **exact relevant pages** and told "answer using only these, and cite them."
- **What it really is:** **RAG = Retrieval-Augmented Generation:** retrieve the most relevant pieces of *your* docs and put them in the prompt so the model answers from **facts you supplied**. Benefits: uses **private data**, **always fresh** (edit docs, not the model), **fewer hallucinations**, **citations**, cheaper than fine-tuning for knowledge.
- **Interview:** *"RAG retrieves relevant chunks of my own data into the prompt so answers are grounded and cited — it's how you add fresh, private knowledge without retraining."*

## 2.2 Vector databases
- **Problem:** With millions of chunks, how do you find the right ones *instantly*?
- **Analogy:** A **super-organized librarian** who arranged every paragraph on the map of meaning and instantly points to the closest shelves.
- **What it really is:** A **vector DB** stores embeddings and finds the **top-k nearest** to your query vector (nearest-neighbor search, sped up by indexes like **HNSW**). Each entry stores **vector + original text + metadata**. Options: **pgvector** (your stack), Chroma, Pinecone, Weaviate, Vertex AI Vector Search.
- **Interview:** *"A vector DB does fast nearest-neighbor search over embeddings; retrieval is embed-query → find top-k nearest chunks → return their text. We store vector, text, and metadata per chunk."*

## 2.3 Chunking
- **Problem:** You can't dump a 300-page manual into the prompt.
- **Analogy:** Don't photocopy the **whole book** for one question — tear out the **few relevant pages.** Chunking decides how big each "page" is.
- **What it really is:** Cut docs into pieces (~300–800 tokens), embed each, retrieve only the relevant few. It's a **Goldilocks** choice: too big = noisy/costly, too small = loses meaning. Add **overlap (10–20%)** so ideas aren't cut mid-thought; prefer **structure-aware** splitting (by headings/sections). Keep **metadata** per chunk.
- **Interview:** *"Chunking balances context vs noise; I use ~300–800 tokens with 10–20% overlap and structure-aware splitting, and keep metadata for citations and filtering."*

## 2.4 The RAG pipeline
- **Problem:** How do all the pieces fit into a working system?
- **Analogy:** First **organize the library** (once); then, per question, the **librarian grabs the relevant pages** and Alex **answers from them.**
- **What it really is:** Two phases:
  - **Ingestion (offline):** Load → Chunk → Embed → Store in vector DB (+metadata).
  - **Query (live):** Embed question → Retrieve top-k → **Augment** prompt with context → **Generate** answer + citations.
  - The **grounding prompt** ("answer ONLY from the context; if it's not there say 'I don't know'; cite sources") is what stops made-up answers.
- **Interview:** *"RAG is ingestion (load/chunk/embed/store) plus query (embed/retrieve/augment/generate); the grounding prompt — 'use only the context, cite, else say I don't know' — is what prevents hallucination."*

## 2.5 Advanced RAG
- **Problem:** Basic retrieval returns "okay" chunks; you need **accurate** ones.
- **Analogy:** A **first-round sort** grabs 20 maybe-relevant pages, then a **senior expert reads them** and keeps the 4 truly best.
- **What it really is:** Boosters — **metadata filtering** (only search the right shelves: date/dept/tenant), **hybrid search** (meaning + exact keywords, so you don't miss IDs/codes), **re-ranking** (retrieve top-20 cheaply, re-order, keep top-4), **query rewriting**, and **best-first ordering** (models get "lost in the middle").
- **Interview:** *"To improve RAG I add metadata filters, hybrid search for exact terms, and a re-ranker over a larger candidate set — plus query rewriting and putting the best chunk first."*

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
LEARN TO TALK        ADD KNOWLEDGE         BUILD (teach Alex)          SHIP (open office)          OPERATE (run it safely)
Day 1                Day 2                 Day 3                       Day 4                        Day 5
├─ LLM: autocomplete ├─ Why RAG: open book ├─ Chains: assembly line    ├─ Eval: exam + key         ├─ Observability: CCTV
├─ Tokens: pizza     ├─ Vector DB:         ├─ Memory: replay minutes   ├─ FastAPI+Docker:          ├─ Guardrails: bouncer +
│    slices; desk    │    librarian on map ├─ Agents/Tools:            │    food truck             │    supervisor
├─ Knobs: spice dial ├─ Chunking: tear     │    phone + calculator     ├─ Cloud Run: pop-up shop   ├─ Security: anti-
├─ Embeddings: map   │    the right pages   ├─ Prompt/RAG/Fine-tune:   ├─ GKE: your own workshop   │    social-engineering
│    of meaning      ├─ Pipeline: ingest   │    brief/handbook/course  └─ vLLM/GPU: own kitchen    ├─ Cost: budget + portions
├─ Prompts: recipe   │    + query          └─ LoRA: bolt-on chip                                    └─ CI/CD: pass exam before
└─ APIs: taxi meter  └─ Advanced: re-rank                                                               promotion + canary
                         ▲                                                                                     │
                         └──────────────── feedback flywheel: prod failures → eval set → improve ─────────────┘
```

- **Day 1** = *how to talk to Alex* (words, knobs, briefs) and how Alex thinks.
- **Day 2** = give Alex *the handbook to read* (RAG) so answers are grounded + cited.
- **Day 3** = *how Alex works* (routine, memory, tools, or a training course).
- **Day 4** = *open the doors* and pick *where Alex works.*
- **Day 5** = keep the office *honest, safe, cheap, and improving.*

For diagrams of each day, see [`diagram/`](diagram/) (day1–day5 PNGs). For the full
system view, see [`LLMOps-Architecture.md`](LLMOps-Architecture.md).
