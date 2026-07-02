"""
Generate explanatory, interview-focused LLMOps diagrams.

Outputs (PNG, 200 DPI):
  full_architecture.png              - end-to-end system (offline + online)
  day1_llm_foundations.png
  day2_rag.png
  day3_orchestration_agents.png
  day4_eval_deploy_gke.png
  day5_monitoring_guardrails_cicd.png

Run:  python generate_diagrams.py
"""

from _helpers import (C, new_canvas, box, callout, band, arrow,
                      interview_band, legend, save)


# =========================================================================
# FULL END-TO-END ARCHITECTURE
# =========================================================================
def full_architecture():
    fig, ax = new_canvas(
        title="LLMOps - Full End-to-End Architecture",
        subtitle="OFFLINE builds the knowledge base | ONLINE answers a user question | then MONITOR & GOVERN close the loop",
    )

    # ---- OFFLINE ingestion band (upper-left) ----
    band(ax, 26, 78, 44, 24, "OFFLINE  -  Ingestion (build the knowledge base)", C["data"])
    box(ax, 11, 84, 16, 7, "Documents", "PDFs / wiki / tickets", C["data"], fs_t=9.5, fs_b=8)
    box(ax, 27, 84, 15, 7, "Chunk", "split + overlap", C["data"], fs_t=9.5, fs_b=8)
    box(ax, 42, 84, 15, 7, "Embed", "text -> vector", C["data"], fs_t=9.5, fs_b=8)
    box(ax, 27, 72, 30, 6.5, "VECTOR DB - Postgres + pgvector", "stores chunks + embeddings", C["data"], fs_t=9.5, fs_b=8)
    arrow(ax, (19, 84), (19.5, 84), color=C["data"])
    arrow(ax, (34.5, 84), (34.5, 84), color=C["data"])
    arrow(ax, (11, 80.5), (11, 75), color=C["data"])
    arrow(ax, (11, 75), (12, 72), color=C["data"], rad=0.0)
    arrow(ax, (42, 80.5), (42, 75.2), color=C["data"])
    arrow(ax, (42, 75.2), (42, 72), color=C["data"])
    # clean simple flow arrows
    arrow(ax, (19, 84), (34.5, 84), color=C["data"])

    # ---- ONLINE serving band (right/center) ----
    band(ax, 74, 66, 46, 52, "ONLINE  -  Serving a live question", C["gw"], alpha=0.05)
    user = (74, 86)
    box(ax, 74, 86, 20, 6.5, "1  USER", "asks a question", C["dark"], fs_t=10, fs_b=8)
    box(ax, 74, 74, 30, 7, "2  ORCHESTRATION", "retrieve top-k + build grounded prompt", C["orch"], fs_t=10, fs_b=8)
    box(ax, 74, 61, 30, 7, "3  GATEWAY (LiteLLM)", "auth - route - fallback - cost", C["gw"], fs_t=10, fs_b=8)
    box(ax, 74, 48, 30, 7, "4  INFERENCE", "Vertex AI / Bedrock (or vLLM on GKE)", C["inf"], fs_t=10, fs_b=8)
    box(ax, 74, 36, 24, 6, "5  RESPONSE", "answer + citations", C["slate"], fs_t=10, fs_b=8)

    arrow(ax, (74, 82.7), (74, 77.6), color=C["orch"], label="question", label_off=(-7, 0))
    arrow(ax, (74, 70.4), (74, 64.6), color=C["gw"], label="prompt", label_off=(-6, 0))
    arrow(ax, (74, 57.4), (74, 51.6), color=C["inf"])
    arrow(ax, (74, 44.4), (74, 39), color=C["slate"])
    arrow(ax, (85, 36), (84, 86), color=C["slate"], ls="--", rad=-0.5,
          label="answer", label_off=(9, 0))
    # retrieval link from vector db to orchestration
    arrow(ax, (42, 72), (59, 74), color=C["data"], rad=-0.15,
          label="retrieve context", label_off=(0, 3))

    # ---- MONITOR + GOVERN (bottom, above interview band) ----
    box(ax, 30, 22, 34, 7, "MONITOR & FEEDBACK", "Arize Phoenix traces + cost + history", C["mon"], fs_t=10, fs_b=8)
    box(ax, 70, 22, 34, 7, "GOVERN & SECURE", "versioning - guardrails - RBAC - CI/CD gate", C["gov"], fs_t=10, fs_b=8)
    arrow(ax, (66, 34), (40, 25.5), color=C["mon"], rad=0.15, label="log + trace", label_off=(4, 3))
    arrow(ax, (47, 22), (53, 22), color=C["gov"])
    arrow(ax, (70, 25.5), (78, 44.5), color=C["gov"], ls=":", rad=-0.3, label="guardrails", label_off=(9, 0))
    arrow(ax, (13, 25.5), (11, 68.5), color=C["mon"], ls="--", rad=-0.1, lw=2.2,
          label="feedback flywheel", label_off=(-1, 0))

    legend(ax, [
        ("Data & Embedding", C["data"]), ("Orchestration", C["orch"]),
        ("Gateway", C["gw"]), ("Inference", C["inf"]),
        ("Monitoring", C["mon"]), ("Governance", C["gov"]),
    ], ncol=6, y=0.02)
    save(fig, "full_architecture")


# =========================================================================
# DAY 1 - LLM FOUNDATIONS & PROMPT ENGINEERING
# =========================================================================
def day1():
    fig, ax = new_canvas(
        title="Day 1 - LLM Foundations & Prompt Engineering",
        subtitle="How an LLM turns your prompt into text, one token at a time - and how to control cost & quality",
    )

    # core pipeline
    box(ax, 16, 74, 22, 9, "PROMPT", "system + user roles\n(instructions + question)", C["orch"], fs_t=11, fs_b=8)
    box(ax, 40, 74, 16, 9, "TOKENS", "text split into\nsub-word pieces", C["data"], fs_t=11, fs_b=8)
    box(ax, 64, 74, 20, 9, "LLM", "predicts the NEXT\ntoken, again & again", C["inf"], fs_t=11, fs_b=8)
    box(ax, 88, 74, 18, 9, "RESPONSE", "generated\ntext", C["slate"], fs_t=11, fs_b=8)
    arrow(ax, (27, 74), (32, 74), color=C["ink"])
    arrow(ax, (48, 74), (54, 74), color=C["ink"])
    arrow(ax, (74, 74), (79, 74), color=C["ink"])

    # context window wrapper note
    callout(ax, 52, 62, 78, 6, "CONTEXT WINDOW",
            "the max tokens (input + output) the model can 'see' at once - overflow = truncation / forgetting", C["gw"])

    # concept callouts
    callout(ax, 18, 48, 28, 11, "Temperature / Top-p",
            "randomness knobs. Low = focused/deterministic\n(facts, JSON). High = creative/varied.", C["inf"])
    callout(ax, 50, 48, 28, 11, "Embeddings",
            "text -> vector of numbers capturing meaning.\nFoundation for RAG search (Day 2).", C["data"])
    callout(ax, 82, 48, 28, 11, "Cost & Latency",
            "you pay per token (in + out). Longer prompt\n= more $ and slower. Cap max_tokens.", C["amber"])

    # prompt engineering strip
    callout(ax, 18, 33, 28, 9, "Prompt Engineering",
            "zero-shot -> few-shot (examples)\n-> chain-of-thought -> force JSON output", C["orch"])
    callout(ax, 50, 33, 28, 9, "Hallucination",
            "model predicts likely text, not truth.\nFix: grounding (RAG), low temp, ask for 'I don't know'.", C["pink"])
    callout(ax, 82, 33, 28, 9, "Roles",
            "system = rules/persona | user = question |\nassistant = model reply. Keep them separate.", C["gov"])

    interview_band(ax, [
        ("What is a token?", "sub-word unit (~4 chars / 0.75 words); billing & limits are per token."),
        ("What is the context window?", "max tokens (input+output) the model sees at once; overflow gets cut."),
        ("Why do LLMs hallucinate?", "they predict probable text, not verified facts; ground with RAG + low temp."),
        ("temperature vs top-p?", "both control randomness; low = deterministic (use for facts/JSON)."),
    ])
    save(fig, "day1_llm_foundations")


# =========================================================================
# DAY 2 - RAG
# =========================================================================
def day2():
    fig, ax = new_canvas(
        title="Day 2 - RAG (Retrieval-Augmented Generation)",
        subtitle="Give the model an 'open book': retrieve relevant chunks, then answer ONLY from them (grounded + cited)",
    )

    # OFFLINE row
    band(ax, 50, 80, 92, 15, "OFFLINE  -  Indexing (done once, ahead of time)", C["data"])
    box(ax, 14, 80, 18, 7.5, "Documents", "your private data", C["data"], fs_t=10, fs_b=8)
    box(ax, 34, 80, 16, 7.5, "Chunk", "split + overlap", C["data"], fs_t=10, fs_b=8)
    box(ax, 53, 80, 16, 7.5, "Embed", "chunk -> vector", C["data"], fs_t=10, fs_b=8)
    box(ax, 76, 80, 22, 7.5, "VECTOR DB", "pgvector: chunks+vectors", C["data"], fs_t=10, fs_b=8)
    arrow(ax, (23, 80), (26, 80), color=C["data"])
    arrow(ax, (42, 80), (45, 80), color=C["data"])
    arrow(ax, (61, 80), (65, 80), color=C["data"])

    # ONLINE row
    band(ax, 50, 55, 92, 22, "ONLINE  -  Query (every question)", C["orch"], alpha=0.05)
    box(ax, 13, 58, 18, 7.5, "Question", "user asks", C["dark"], fs_t=10, fs_b=8)
    box(ax, 33, 58, 16, 7.5, "Embed query", "-> vector", C["inf"], fs_t=10, fs_b=8)
    box(ax, 54, 58, 20, 7.5, "Similarity search", "top-k nearest chunks", C["inf"], fs_t=10, fs_b=8)
    box(ax, 80, 58, 20, 7.5, "Augment prompt", "question + chunks", C["orch"], fs_t=10, fs_b=8)
    box(ax, 66, 46, 26, 7, "LLM -> grounded answer + citations", "", C["slate"], fs_t=10)
    arrow(ax, (22, 58), (25, 58), color=C["ink"])
    arrow(ax, (41, 58), (44, 58), color=C["ink"])
    arrow(ax, (64, 58), (70, 58), color=C["ink"])
    arrow(ax, (76, 76), (57, 62), color=C["data"], rad=-0.2, label="match", label_off=(3, 2))
    arrow(ax, (80, 54), (72, 49.5), color=C["orch"], rad=-0.2)

    # advanced RAG callout
    callout(ax, 27, 33, 44, 8, "Advanced RAG (boost accuracy)",
            "metadata filters (by source/date) - hybrid search (keyword+vector) - re-ranking top results", C["amber"])
    callout(ax, 73, 33, 44, 8, "Why RAG > fine-tuning for knowledge",
            "cheaper, always fresh, uses private data, gives citations, no model retraining", C["model"])

    interview_band(ax, [
        ("What is RAG?", "retrieve relevant chunks from a vector DB, put them in the prompt, answer from them."),
        ("How does retrieval work?", "embed the query, cosine-similarity vs stored vectors, take top-k."),
        ("How do you pick chunk size?", "balance context vs noise/cost; use overlap so meaning isn't cut."),
        ("RAG vs fine-tuning?", "RAG = knowledge/freshness/citations; fine-tune = behavior/format/style."),
    ])
    save(fig, "day2_rag")


# =========================================================================
# DAY 3 - ORCHESTRATION, AGENTS, FINE-TUNING
# =========================================================================
def day3():
    fig, ax = new_canvas(
        title="Day 3 - Orchestration, Agents & Fine-Tuning",
        subtitle="Give the model a workflow (chains), a way to remember (memory), tools (agents), or new skills (fine-tune)",
    )

    # Chains
    band(ax, 25, 76, 44, 16, "Chain (fixed steps)", C["orch"])
    box(ax, 12, 76, 14, 6.5, "Step 1", "retrieve", C["orch"], fs_t=9.5, fs_b=8)
    box(ax, 26, 76, 14, 6.5, "Step 2", "prompt", C["orch"], fs_t=9.5, fs_b=8)
    box(ax, 40, 76, 14, 6.5, "Step 3", "parse", C["orch"], fs_t=9.5, fs_b=8)
    arrow(ax, (19, 76), (19, 76), color=C["orch"])
    arrow(ax, (19, 76), (33, 76), color=C["orch"])
    arrow(ax, (33, 76), (33, 76), color=C["orch"])

    # Agent loop
    band(ax, 74, 74, 46, 22, "Agent = LLM decides (ReAct loop)", C["inf"], alpha=0.05)
    box(ax, 74, 80, 22, 6.5, "LLM (reasoner)", "Thought -> Action", C["inf"], fs_t=9.5, fs_b=8)
    box(ax, 62, 68, 18, 6, "Tools", "search / API / DB", C["model"], fs_t=9.5, fs_b=8)
    box(ax, 86, 68, 18, 6, "Memory", "past turns", C["gw"], fs_t=9.5, fs_b=8)
    arrow(ax, (68, 77), (63, 71), color=C["ink"], label="call", label_off=(-3, 1))
    arrow(ax, (66, 71), (71, 77), color=C["ink"], ls="--", label="observe", label_off=(4, -1))
    arrow(ax, (83, 71), (80, 77), color=C["gw"], ls="--")

    # Decision: prompt vs rag vs finetune
    callout(ax, 27, 50, 44, 10, "Prompt vs RAG vs Fine-tune (how to choose)",
            "Need KNOWLEDGE/freshness -> RAG   |   Need BEHAVIOR/format/tone -> Fine-tune\nJust need a quick tweak -> better Prompt. Combine when needed.", C["amber"])
    callout(ax, 73, 50, 44, 10, "Fine-tuning basics (LoRA / PEFT)",
            "train small 'adapter' weights on examples instead of the whole model:\ncheap, fast, portable. Needs a clean labeled dataset.", C["model"])

    callout(ax, 50, 36, 90, 6, "Memory types",
            "buffer (last N turns) - summary (compress old turns) - vector (retrieve relevant past) - keep it small to save tokens", C["gw"])

    interview_band(ax, [
        ("Chain vs agent?", "chain = fixed predefined steps; agent = LLM chooses which tools to call (ReAct)."),
        ("What is the ReAct loop?", "Thought -> Action (tool) -> Observation, repeat until it can answer."),
        ("Prompt vs RAG vs fine-tune?", "knowledge->RAG; behavior/format->fine-tune; quick fix->prompt."),
        ("What is LoRA/PEFT?", "train small adapter weights, not the full model: cheap & fast to swap."),
    ])
    save(fig, "day3_orchestration_agents")


# =========================================================================
# DAY 4 - EVALUATION, DEPLOYMENT, GKE
# =========================================================================
def day4():
    fig, ax = new_canvas(
        title="Day 4 - Evaluation, Deployment & Serving on GKE",
        subtitle="Measure quality -> package as an API in a container -> ship to Cloud Run (easy) or GKE (scale + GPUs)",
    )

    # eval gate
    box(ax, 14, 78, 22, 9, "EVALUATION", "golden set + Ragas\n(faithfulness, relevancy)", C["gov"], fs_t=10, fs_b=8)
    box(ax, 40, 78, 20, 9, "FastAPI", "wrap app\nas /chat API", C["orch"], fs_t=10, fs_b=8)
    box(ax, 64, 78, 20, 9, "Docker", "build one\nportable image", C["data"], fs_t=10, fs_b=8)
    arrow(ax, (25, 78), (30, 78), color=C["ink"], label="gate", label_off=(0, 2.5))
    arrow(ax, (50, 78), (54, 78), color=C["ink"])
    arrow(ax, (74, 78), (80, 78), color=C["ink"])
    box(ax, 90, 78, 16, 9, "Registry", "store image", C["slate"], fs_t=10, fs_b=8)

    # two deploy targets
    band(ax, 26, 50, 44, 20, "Option A - Cloud Run (serverless, easy)", C["model"])
    callout(ax, 26, 50, 40, 12, "Cloud Run",
            "give it the image -> URL. Autoscales (even to 0),\nno servers to manage. Great default for CPU apps.", C["model"], fs_t=10)

    band(ax, 74, 48, 46, 30, "Option B - GKE / Kubernetes (control, scale, GPUs)", C["inf"], alpha=0.05)
    box(ax, 60, 58, 18, 5.5, "Ingress", "public entry", C["inf"], fs_t=9, fs_b=7.5)
    box(ax, 80, 58, 18, 5.5, "Service", "load-balance", C["inf"], fs_t=9, fs_b=7.5)
    box(ax, 70, 48, 26, 6, "Deployment -> Pods (replicas)", "", C["inf"], fs_t=9.5)
    box(ax, 60, 39, 18, 5.5, "HPA", "autoscale pods", C["gw"], fs_t=9, fs_b=7.5)
    box(ax, 84, 39, 22, 6, "GPU node pool", "vLLM / TGI / KServe", C["model"], fs_t=9, fs_b=7.5)
    arrow(ax, (69, 58), (71, 58), color=C["inf"])
    arrow(ax, (74, 55), (72, 51), color=C["inf"])
    arrow(ax, (64, 45), (66, 42), color=C["gw"], ls="--")
    arrow(ax, (80, 45), (84, 42), color=C["model"], ls="--")
    arrow(ax, (90, 73.5), (78, 60.8), color=C["slate"], ls=":", rad=-0.2, label="deploy", label_off=(6, 1))

    interview_band(ax, [
        ("How do you eval non-deterministic output?", "golden set + LLM-as-judge + Ragas (faithfulness/context/answer relevancy)."),
        ("Cloud Run vs GKE?", "Cloud Run = serverless, scale-to-zero, easy; GKE = control, GPUs, big scale."),
        ("What does HPA do?", "auto-adds/removes pods based on CPU / QPS / custom metrics."),
        ("Why self-host with vLLM?", "cost at scale, privacy, open models, high-throughput batched inference."),
    ])
    save(fig, "day4_eval_deploy_gke")


# =========================================================================
# DAY 5 - MONITORING, GUARDRAILS, SECURITY, COST, CI/CD
# =========================================================================
def day5():
    fig, ax = new_canvas(
        title="Day 5 - Monitoring, Guardrails, Security, Cost & CI/CD",
        subtitle="Run the 'office' around the model: watch it, keep it safe, defend it, cap its cost, and ship changes safely",
    )

    # request path with guardrails wrapping
    box(ax, 12, 76, 16, 8, "User input", "", C["dark"], fs_t=10)
    box(ax, 33, 76, 18, 8, "INPUT GUARD", "injection / PII\nchecks", C["gw"], fs_t=9.5, fs_b=8)
    box(ax, 55, 76, 16, 8, "App + LLM", "RAG answer", C["inf"], fs_t=9.5, fs_b=8)
    box(ax, 77, 76, 18, 8, "OUTPUT GUARD", "grounding / PII /\nmoderation", C["gw"], fs_t=9.5, fs_b=8)
    box(ax, 95, 76, 10, 8, "User", "", C["dark"], fs_t=9.5)
    arrow(ax, (20, 76), (24, 76), color=C["ink"])
    arrow(ax, (42, 76), (47, 76), color=C["ink"])
    arrow(ax, (63, 76), (68, 76), color=C["ink"])
    arrow(ax, (86, 76), (90, 76), color=C["ink"])

    # threats
    callout(ax, 20, 60, 34, 9, "Security - OWASP LLM Top 10",
            "prompt injection - data leakage - insecure output -\nexcessive agency. Defend at the input guard + least privilege.", C["pink"])
    # observability
    callout(ax, 58, 60, 34, 9, "Observability",
            "trace every call (prompt->context->output),\nmetrics (latency, tokens, cost), capture user feedback.", C["mon"])
    # arrow app -> observability
    arrow(ax, (55, 72), (58, 65), color=C["mon"], ls="--")

    # cost levers
    callout(ax, 27, 44, 48, 9, "Cost optimization (levers)",
            "cache repeats - route easy queries to a smaller model - trim prompt/context -\nbatch requests - cap max_tokens", C["amber"])
    # CI/CD
    callout(ax, 75, 44, 44, 9, "CI/CD with an eval gate",
            "PR -> run eval set -> BLOCK if quality drops ->\ncanary release -> auto-rollback on regression.", C["model"])

    interview_band(ax, [
        ("What is prompt injection?", "user text overrides your instructions; mitigate w/ role separation, guards, least privilege."),
        ("What are guardrails?", "input checks (injection/PII) + output checks (grounding/PII/moderation) with safe fallback."),
        ("How do you cut LLM cost?", "cache, route to smaller model, trim prompt, batch, cap max_tokens."),
        ("Why an eval gate in CI/CD?", "run eval set on each change; block deploy on quality drop; canary + rollback."),
    ])
    save(fig, "day5_monitoring_guardrails_cicd")


if __name__ == "__main__":
    full_architecture()
    day1()
    day2()
    day3()
    day4()
    day5()
    print("All diagrams generated.")
