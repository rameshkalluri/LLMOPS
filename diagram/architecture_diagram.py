"""
Generate an end-to-end LLMOps architecture diagram (PNG).

Draws the 7 layers from LLMOps-Architecture.md and connects every dot:
User -> Orchestration -> Gateway -> Inference -> Response, with the
Data/Embedding pipeline feeding retrieval, the Model layer feeding inference,
and the Monitoring + Governance layers closing the feedback flywheel.

Run:  python architecture_diagram.py
Out:  llmops_architecture.png  (and .svg)
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# ----- palette (one color per layer) ---------------------------------------
C = {
    "data":  "#2563eb",  # L1 Data & Embedding      (blue)
    "model": "#16a34a",  # L2 Model                 (green)
    "orch":  "#ea580c",  # L3 Prompt & Orchestration(orange)
    "gw":    "#dc2626",  # L4 Gateway               (red)
    "inf":   "#7c3aed",  # L5 Inference & Serving   (purple)
    "mon":   "#0d9488",  # L6 Monitoring & Feedback (teal)
    "gov":   "#6b7280",  # L7 Governance & Security (gray)
    "user":  "#111827",  # user
}

fig, ax = plt.subplots(figsize=(17, 11), dpi=200)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")


def box(x, y, w, h, text, color, text_color="white", fs=11, bold=True):
    """Draw a rounded box centered at (x, y)."""
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.3,rounding_size=1.2",
        linewidth=1.5, edgecolor=color, facecolor=color, alpha=0.92,
        mutation_aspect=1,
    )
    ax.add_patch(patch)
    ax.text(
        x, y, text, ha="center", va="center", color=text_color,
        fontsize=fs, fontweight="bold" if bold else "normal", zorder=5,
        wrap=True,
    )
    return (x, y, w, h)


def arrow(p1, p2, color="#374151", style="-|>", lw=2.2, ls="-", rad=0.0,
          label=None, label_off=(0, 0), label_color=None, fs=9):
    a = FancyArrowPatch(
        p1, p2, arrowstyle=style, mutation_scale=18,
        linewidth=lw, color=color, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}", zorder=3,
    )
    ax.add_patch(a)
    if label:
        mx = (p1[0] + p2[0]) / 2 + label_off[0]
        my = (p1[1] + p2[1]) / 2 + label_off[1]
        ax.text(mx, my, label, ha="center", va="center",
                fontsize=fs, color=label_color or color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none",
                          alpha=0.85), zorder=6)


# ===== TITLE =================================================================
ax.text(50, 97.5, "End-to-End LLMOps Architecture",
        ha="center", va="center", fontsize=22, fontweight="bold",
        color="#111827")
ax.text(50, 94.2,
        "Data -> Embeddings -> Retrieve -> Prompt -> Gateway -> Inference -> Response -> Monitor -> Govern -> Feedback",
        ha="center", va="center", fontsize=10.5, color="#6b7280", style="italic")

# ===== CENTER REQUEST FLOW ===================================================
user   = box(50, 87, 20, 6, "USER\n(web / mobile client)", C["user"], fs=11)
orch   = box(50, 74, 30, 7,
             "L3  PROMPT & ORCHESTRATION\nretrieve top-k  +  build grounded prompt\n(versioned template  +  memory)",
             C["orch"], fs=10)
gw     = box(50, 60, 30, 7,
             "L4  GATEWAY  (LiteLLM)\nunified API - auth - routing - rate limit\nfallback / A-B - cost & latency metrics",
             C["gw"], fs=10)
inf    = box(50, 46, 30, 7,
             "L5  INFERENCE & SERVING\nVertex AI / Bedrock  (hosted)\nor vLLM / TGI on GKE  + cache + stream",
             C["inf"], fs=10)
resp   = box(50, 33, 22, 6, "RESPONSE\nanswer + citations", "#334155", fs=10)

# center vertical arrows (request path)
arrow((50, 84), (50, 77.6), color=C["orch"], label="prompt", label_off=(-6, 0))
arrow((50, 70.4), (50, 63.6), color=C["gw"])
arrow((50, 56.4), (50, 49.6), color=C["inf"])
arrow((50, 42.4), (50, 36), color="#334155")
# response back up to user (curved, on the right)
arrow((61, 33), (60, 87), color="#334155", ls="--", rad=-0.45,
      label="answer", label_off=(9, 0), label_color="#334155")

# ===== LEFT: DATA & EMBEDDING PIPELINE (L1) ==================================
src    = box(16, 84, 22, 6.5, "Data sources\ndocs / wiki / CRM / tickets", C["data"], fs=9.5)
proc   = box(16, 73, 22, 6.5, "Processing\nclean - normalize - CHUNK", C["data"], fs=9.5)
emb    = box(16, 62, 22, 6.5, "Embeddings\n(LiteLLM embed model)", C["data"], fs=9.5)
vdb    = box(16, 51, 22, 7, "VECTOR DB\nPostgres + pgvector", C["data"], fs=10)

arrow((16, 80.75), (16, 76.25), color=C["data"])
arrow((16, 69.75), (16, 65.25), color=C["data"])
arrow((16, 58.75), (16, 54.5), color=C["data"])
# vector db feeds retrieval in orchestration
arrow((27, 51), (36, 72), color=C["data"], rad=-0.25,
      label="retrieve", label_off=(0, 3), label_color=C["data"])

# ===== RIGHT: MODEL LAYER (L2) ===============================================
base   = box(84, 73, 22, 6.5, "L2  Base model\nGemini / Claude / Llama", C["model"], fs=9.5)
adapt  = box(84, 62, 22, 6.5, "Adapt\nprompt / RAG / fine-tune\n(LoRA / PEFT)", C["model"], fs=9)
arrow((84, 69.75), (84, 65.25), color=C["model"])
# model layer selects the served model
arrow((73, 60), (65, 47), color=C["model"], rad=-0.25,
      label="selects", label_off=(3, 3), label_color=C["model"])

# ===== BOTTOM: MONITORING (L6) & GOVERNANCE (L7) =============================
mon    = box(28, 18, 30, 8,
             "L6  MONITORING & FEEDBACK\nArize Phoenix - traces / cost / hallucination\n+ interaction history (Postgres)",
             C["mon"], fs=9.5)
gov    = box(72, 18, 30, 8,
             "L7  GOVERNANCE & SECURITY\nversioning - RBAC - PII - audit\nguardrails - CI/CD eval gate",
             C["gov"], fs=9.5)

# response + user feedback into monitoring
arrow((45, 31), (33, 22), color=C["mon"], rad=0.2,
      label="log + trace", label_off=(-3, 3), label_color=C["mon"])
arrow((43, 33), (28, 22.5), color=C["mon"], ls="--", rad=0.15)
# monitoring -> governance
arrow((43, 18), (57, 18), color=C["gov"], label="policies", fs=9)
# governance guards the gateway
arrow((72, 22), (63, 57), color=C["gov"], ls=":", rad=-0.3, lw=1.8,
      label="guardrails", label_off=(10, 0), label_color=C["gov"])
# feedback flywheel: monitoring back up to data pipeline
arrow((16, 22), (16, 47.5), color=C["mon"], ls="--", rad=0.0, lw=2.4,
      label="feedback\nflywheel", label_off=(-6.5, 0), label_color=C["mon"], fs=9)
arrow((21, 18), (16, 21.5), color=C["mon"], ls="--", rad=0.2)

# ===== LEGEND ================================================================
legend_items = [
    ("L1  Data & Embedding", C["data"]),
    ("L2  Model", C["model"]),
    ("L3  Prompt & Orchestration", C["orch"]),
    ("L4  Gateway (LiteLLM)", C["gw"]),
    ("L5  Inference & Serving", C["inf"]),
    ("L6  Monitoring & Feedback", C["mon"]),
    ("L7  Governance & Security", C["gov"]),
]
handles = [Line2D([0], [0], marker="s", color="w", markerfacecolor=c,
                  markersize=12, label=t) for t, c in legend_items]
ax.legend(handles=handles, loc="lower center", ncol=4, frameon=True,
          fontsize=9, bbox_to_anchor=(0.5, -0.02), handletextpad=0.4,
          columnspacing=1.2)

plt.tight_layout()
fig.savefig("llmops_architecture.png", dpi=200, bbox_inches="tight",
            facecolor="white")
fig.savefig("llmops_architecture.svg", bbox_inches="tight", facecolor="white")
print("Saved llmops_architecture.png and .svg")
