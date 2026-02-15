#!/usr/bin/env python3
"""
InfoGen — Data-driven infographic generator
Generates a teen-aesthetic infographic from data.json
"""

import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

# ── Style: Dark + Neon (teen aesthetic) ──────────────────────────
BG       = "#0d0d1a"
WHITE    = "#ffffff"
CYAN     = "#00f2ea"
PINK     = "#ff0050"
LIME     = "#ccff00"
PURPLE   = "#b14eff"
GREY     = "#888888"

def load_data(path="data.json"):
    with open(path) as f:
        return json.load(f)

def draw_infographic(data):
    fig = plt.figure(figsize=(12, 22), facecolor=BG)
    gs = GridSpec(20, 6, figure=fig, hspace=0.6, wspace=0.4)

    # ── 1. TITLE ─────────────────────────────────────────────────
    ax = fig.add_subplot(gs[0:2, :])
    ax.set_facecolor(BG); ax.axis("off")
    ax.text(0.5, 0.75, data["title"], ha="center", va="center",
            fontsize=48, fontweight="bold", color=CYAN, fontfamily="sans-serif")
    ax.text(0.5, 0.35, data["subtitle"], ha="center", va="center",
            fontsize=16, color=WHITE, alpha=0.85)
    ax.text(0.5, 0.10, f'{data["meta"]["region"]}  •  {data["meta"]["year"]}',
            ha="center", va="center", fontsize=12, color=GREY)

    # ── 2. DEFINITION ────────────────────────────────────────────
    ax = fig.add_subplot(gs[2:3, :])
    ax.set_facecolor(BG); ax.axis("off")
    ax.text(0.5, 0.7, "WHAT IS 67?", ha="center", fontsize=14,
            fontweight="bold", color=PINK)
    ax.text(0.5, 0.25, data.get("definition", ""), ha="center", va="center",
            fontsize=11, color=WHITE, wrap=True, style="italic",
            fontfamily="sans-serif")

    # ── 3. BIG STATS ─────────────────────────────────────────────
    ax = fig.add_subplot(gs[3:5, :])
    ax.set_facecolor(BG); ax.axis("off")
    ax.text(0.5, 0.95, "BY THE NUMBERS", ha="center", fontsize=14,
            fontweight="bold", color=PINK)
    stats = data["stats"]
    labels = list(stats.keys())
    vals   = list(stats.values())
    for i, (k, v) in enumerate(zip(labels, vals)):
        x = (i + 1) / (len(labels) + 1)
        ax.text(x, 0.55, v, ha="center", fontsize=36, fontweight="bold", color=LIME)
        ax.text(x, 0.20, k.replace("_", " ").upper(), ha="center",
                fontsize=10, color=WHITE, alpha=0.7)

    # ── 4. PLATFORM DONUT ────────────────────────────────────────
    ax = fig.add_subplot(gs[5:9, 0:3])
    ax.set_facecolor(BG)
    platforms = data["platforms"]
    sizes  = [p["percent"] for p in platforms]
    labels = [f'{p["name"]}' for p in platforms]
    colors = [p.get("color", CYAN) for p in platforms]
    wedges, texts, autos = ax.pie(
        sizes, labels=labels, autopct="%1.0f%%", startangle=90,
        colors=colors, textprops=dict(color=WHITE, fontsize=10),
        pctdistance=0.8, labeldistance=1.12)
    for a in autos:
        a.set_fontsize(9); a.set_color(WHITE)
    centre = plt.Circle((0, 0), 0.60, fc=BG)
    ax.add_artist(centre)
    ax.set_title("PLATFORM DOMINANCE", color=PINK, fontsize=13, pad=18,
                 fontweight="bold")

    # ── 5. DEMOGRAPHICS BAR ──────────────────────────────────────
    ax = fig.add_subplot(gs[5:9, 3:6])
    ax.set_facecolor(BG)
    demos = data["demographics"]
    ages = list(demos.keys())
    vals = list(demos.values())
    bar_colors = [CYAN, PINK, LIME, PURPLE][:len(ages)]
    bars = ax.barh(ages, vals, color=bar_colors, height=0.55)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{v}%", va="center", color=WHITE, fontsize=11)
    ax.set_title("WHO'S INTO IT? (AGE %)", color=PINK, fontsize=13,
                 pad=18, fontweight="bold")
    ax.tick_params(axis="y", colors=WHITE, labelsize=11)
    ax.tick_params(axis="x", colors=BG)
    ax.set_xlim(0, max(vals) + 12)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # ── 6. TIMELINE ──────────────────────────────────────────────
    ax = fig.add_subplot(gs[9:15, :])
    ax.set_facecolor(BG); ax.axis("off")
    ax.set_title("TIMELINE", color=PINK, fontsize=14, pad=20, fontweight="bold")

    timeline = data["timeline"]
    n = len(timeline)
    # vertical line
    ax.plot([0.5, 0.5], [0.02, 0.92], color=CYAN, linewidth=2, alpha=0.5)
    for i, item in enumerate(timeline):
        y = 0.88 - i * (0.85 / (n - 1)) if n > 1 else 0.5
        ax.plot(0.5, y, "o", color=PINK, markersize=10, zorder=5)
        if i % 2 == 0:
            ax.text(0.46, y, f'{item["period"]}', ha="right", va="center",
                    fontsize=10, fontweight="bold", color=CYAN)
            ax.text(0.46, y - 0.035, item["event"], ha="right", va="center",
                    fontsize=9, color=WHITE, alpha=0.85)
        else:
            ax.text(0.54, y, f'{item["period"]}', ha="left", va="center",
                    fontsize=10, fontweight="bold", color=CYAN)
            ax.text(0.54, y - 0.035, item["event"], ha="left", va="center",
                    fontsize=9, color=WHITE, alpha=0.85)

    # ── 7. NOTABLE IMPACTS ───────────────────────────────────────
    ax = fig.add_subplot(gs[15:17, 0:3])
    ax.set_facecolor(BG); ax.axis("off")
    ax.set_title("NOTABLE IMPACTS", color=PINK, fontsize=13, pad=14,
                 fontweight="bold")
    impacts = data.get("impacts", [])
    for i, imp in enumerate(impacts):
        y = 0.85 - i * 0.18
        ax.text(0.08, y, f"▸ {imp}", va="center", fontsize=10, color=WHITE)

    # ── 8. CULTURE SIGNALS ───────────────────────────────────────
    ax = fig.add_subplot(gs[15:17, 3:6])
    ax.set_facecolor(BG); ax.axis("off")
    ax.set_title("CULTURE SIGNALS", color=PINK, fontsize=13, pad=14,
                 fontweight="bold")
    signals = data.get("culture_signals", [])
    for i, sig in enumerate(signals):
        y = 0.85 - i * 0.18
        ax.text(0.08, y, f"✦ {sig}", va="center", fontsize=10, color=LIME)

    # ── 9. BUZZWORDS ─────────────────────────────────────────────
    ax = fig.add_subplot(gs[17:18, :])
    ax.set_facecolor(BG); ax.axis("off")
    bw = data.get("buzzwords", [])
    bw_str = "   •   ".join(bw)
    ax.text(0.5, 0.6, "BUZZWORDS", ha="center", fontsize=12,
            fontweight="bold", color=PINK)
    ax.text(0.5, 0.15, bw_str, ha="center", fontsize=13,
            color=CYAN, fontfamily="sans-serif")

    # ── 10. SOURCES ──────────────────────────────────────────────
    ax = fig.add_subplot(gs[18:19, :])
    ax.set_facecolor(BG); ax.axis("off")
    sources = data.get("sources_placeholder", [])
    src_str = "  |  ".join(sources)
    ax.text(0.5, 0.5, src_str, ha="center", fontsize=7, color=GREY, alpha=0.6)

    # ── FOOTER ───────────────────────────────────────────────────
    ax = fig.add_subplot(gs[19:20, :])
    ax.set_facecolor(BG); ax.axis("off")
    ax.text(0.5, 0.5, f'Generated by {data["meta"]["generated_by"]}  •  {data["meta"]["region"]}  •  {data["meta"]["year"]}',
            ha="center", fontsize=9, color=GREY, alpha=0.5)

    # ── SAVE ─────────────────────────────────────────────────────
    out = "output_infographic.png"
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Infographic saved to {out}")
    return out


if __name__ == "__main__":
    data = load_data()
    draw_infographic(data)
