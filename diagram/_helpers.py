"""Reusable drawing helpers for the LLMOps diagrams."""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# Shared palette (consistent across every diagram)
C = {
    "data":  "#2563eb",  # blue
    "model": "#16a34a",  # green
    "orch":  "#ea580c",  # orange
    "gw":    "#dc2626",  # red
    "inf":   "#7c3aed",  # purple
    "mon":   "#0d9488",  # teal
    "gov":   "#6b7280",  # gray
    "dark":  "#111827",
    "slate": "#334155",
    "amber": "#d97706",
    "pink":  "#db2777",
    "ink":   "#1f2937",
}


def new_canvas(w=17, h=10.5, title=None, subtitle=None):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    if title:
        ax.text(50, 97, title, ha="center", va="center",
                fontsize=22, fontweight="bold", color=C["dark"])
    if subtitle:
        ax.text(50, 93.2, subtitle, ha="center", va="center",
                fontsize=11, color="#6b7280", style="italic")
    return fig, ax


def box(ax, x, y, w, h, title, body="", fill="#2563eb", tcol="white",
        fs_t=11, fs_b=8.6, alpha=0.95, edge=None):
    """Solid colored node with bold title and optional smaller body text."""
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.3,rounding_size=1.1",
        linewidth=1.5, edgecolor=edge or fill, facecolor=fill, alpha=alpha,
        zorder=4,
    ))
    if body:
        ax.text(x, y + h * 0.20, title, ha="center", va="center",
                color=tcol, fontsize=fs_t, fontweight="bold", zorder=5)
        ax.text(x, y - h * 0.22, body, ha="center", va="center",
                color=tcol, fontsize=fs_b, zorder=5)
    else:
        ax.text(x, y, title, ha="center", va="center",
                color=tcol, fontsize=fs_t, fontweight="bold", zorder=5)


def callout(ax, x, y, w, h, title, body="", color="#2563eb",
            fs_t=9.6, fs_b=8.4):
    """Light card with colored border and dark text (for explanations)."""
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.3,rounding_size=1.0",
        linewidth=1.6, edgecolor=color, facecolor="white", alpha=0.98,
        zorder=4,
    ))
    if body:
        ax.text(x, y + h * 0.26, title, ha="center", va="center",
                color=color, fontsize=fs_t, fontweight="bold", zorder=5)
        ax.text(x, y - h * 0.16, body, ha="center", va="center",
                color=C["ink"], fontsize=fs_b, zorder=5)
    else:
        ax.text(x, y, title, ha="center", va="center",
                color=C["ink"], fontsize=fs_b, zorder=5)


def band(ax, x, y, w, h, label, color, alpha=0.08):
    """Translucent group background with a small corner label."""
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.3,rounding_size=1.4",
        linewidth=1.4, edgecolor=color, facecolor=color, alpha=alpha,
        zorder=1,
    ))
    ax.text(x - w / 2 + 3.2, y + h / 2 - 2.2, label, ha="left", va="center",
            color=color, fontsize=10.5, fontweight="bold", zorder=2)


def arrow(ax, p1, p2, color="#374151", style="-|>", lw=2.2, ls="-", rad=0.0,
          label=None, label_off=(0, 0), fs=8.6):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle=style, mutation_scale=16,
        linewidth=lw, color=color, linestyle=ls,
        connectionstyle=f"arc3,rad={rad}", zorder=3,
    ))
    if label:
        mx = (p1[0] + p2[0]) / 2 + label_off[0]
        my = (p1[1] + p2[1]) / 2 + label_off[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                color=color, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none",
                          alpha=0.9), zorder=6)


def interview_band(ax, qa, color="#0f172a", y=8.5, h=13, title="INTERVIEW ANSWERS (say this)"):
    """Bottom band with Q -> A one-liners for interview prep."""
    ax.add_patch(FancyBboxPatch(
        (3, y - h / 2), 94, h,
        boxstyle="round,pad=0.3,rounding_size=1.0",
        linewidth=1.6, edgecolor=color, facecolor="#f8fafc", alpha=1.0,
        zorder=2,
    ))
    ax.text(6, y + h / 2 - 2.0, title, ha="left", va="center",
            color=color, fontsize=10.5, fontweight="bold", zorder=3)
    n = len(qa)
    col = 2
    per = (n + 1) // col
    line_h = (h - 5) / per
    for i, (q, a) in enumerate(qa):
        c = i // per
        r = i % per
        xq = 6 + c * 47
        yq = y + h / 2 - 5 - r * line_h
        ax.text(xq, yq, f"Q: {q}", ha="left", va="center", fontsize=8.4,
                color=color, fontweight="bold", zorder=3)
        ax.text(xq + 1.5, yq - line_h * 0.42, f"A: {a}", ha="left", va="center",
                fontsize=8.0, color=C["ink"], zorder=3)


def legend(ax, items, loc="lower center", ncol=4, y=-0.03):
    handles = [Line2D([0], [0], marker="s", color="w", markerfacecolor=c,
                      markersize=12, label=t) for t, c in items]
    ax.legend(handles=handles, loc=loc, ncol=ncol, frameon=True, fontsize=9,
              bbox_to_anchor=(0.5, y), handletextpad=0.4, columnspacing=1.2)


def save(fig, name):
    fig.savefig(f"{name}.png", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved", name + ".png")
