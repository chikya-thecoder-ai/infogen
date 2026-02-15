#!/usr/bin/env python3
"""
InfoGen — Phone-friendly infographic (1080x1920 portrait)
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

BG    = "#0f0f1a"
WHITE = "#ffffff"
CYAN  = "#00f2ea"
PINK  = "#ff0050"
LIME  = "#ccff00"
PURPLE = "#b14eff"


def load(path="data.json"):
    with open(path) as f:
        return json.load(f)


def render(data, out="output_infographic_phone.png"):
    # 1080x1920 at 150 dpi -> 7.2 x 12.8 inches
    fig = plt.figure(figsize=(7.2, 12.8), dpi=150)
    fig.patch.set_facecolor(BG)
    gs = GridSpec(24, 6, figure=fig, wspace=0.3, hspace=0.7)

    # ── TITLE ────────────────────────────────────────────────────
    ax = fig.add_subplot(gs[0:2, :])
    ax.axis("off"); ax.set_facecolor(BG)
    ax.text(0.5, 0.78, data["title"],
            ha="center", va="center", color=CYAN,
            fontsize=38, fontweight="bold", fontfamily="sans-serif")
    ax.text(0.5, 0.42, data["subtitle"],
            ha="center", va="center", color=WHITE, fontsize=11)
    ax.text(0.5, 0.15,
            f"{data['meta']['region']}  \u2022  {data['meta']['year']}",
            ha="center", va="center", color=WHITE, fontsize=9, alpha=0.6)

    # ── DEFINITION ───────────────────────────────────────────────
    ax = fig.add_subplot(gs[2:3, :])
    ax.axis("off"); ax.set_facecolor(BG)
    ax.text(0.5, 0.75, "WHAT IS 67?",
            ha="center", fontsize=12, fontweight="bold", color=PINK)
    ax.text(0.5, 0.25, data.get("definition", ""),
            ha="center", va="center", color=WHITE, fontsize=9,
            style="italic", wrap=True)

    # ── BIG STATS ────────────────────────────────────────────────
    ax = fig.add_subplot(gs[3:5, :])
    ax.axis("off"); ax.set_facecolor(BG)
    ax.text(0.5, 0.95, "BY THE NUMBERS",
            ha="center", fontsize=12, fontweight="bold", color=PINK)
    stats = data["stats"]
    for i, (k, v) in enumerate(stats.items()):
        x = (i + 1) / (len(stats) + 1)
        ax.text(x, 0.55, v, ha="center", fontsize=26,
                fontweight="bold", color=LIME)
        ax.text(x, 0.22, k.replace("_", " ").upper(),
                ha="center", fontsize=8, color=WHITE, alpha=0.7)

    # ── PLATFORM DONUT ───────────────────────────────────────────
    ax = fig.add_subplot(gs[5:9, 0:3])
    ax.set_facecolor(BG)
    plat = data["platforms"]
    sizes = [p["percent"] for p in plat]
    labels = [p["name"] for p in plat]
    colors = [p.get("color", CYAN) for p in plat]
    wedges, texts, autos = ax.pie(
        sizes, labels=labels, autopct="%1.0f%%", startangle=90,
        colors=colors,
        textprops=dict(color=WHITE, fontsize=8),
        pctdistance=0.8, labeldistance=1.12)
    for a in autos:
        a.set_fontsize(8); a.set_color(WHITE)
    ax.add_artist(plt.Circle((0, 0), 0.60, fc=BG))
    ax.set_title("PLATFORM DOMINANCE", color=PINK, fontsize=10,
                 pad=10, fontweight="bold")

    # ── DEMOGRAPHICS BAR ─────────────────────────────────────────
    ax = fig.add_subplot(gs[5:9, 3:6])
    ax.set_facecolor(BG)
    demos = data["demographics"]
    ages = list(demos.keys())
    vals = list(demos.values())
    bar_colors = [CYAN, PINK, LIME, PURPLE][:len(ages)]
    bars = ax.barh(ages, vals, color=bar_colors, height=0.55)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{v}%", va="center", color=WHITE, fontsize=9)
    ax.set_title("WHO'S INTO IT? (AGE %)", color=PINK, fontsize=10,
                 pad=10, fontweight="bold")
    ax.tick_params(axis="y", colors=WHITE, labelsize=9)
    ax.tick_params(axis="x", colors=BG)
    ax.set_xlim(0, max(vals) + 12)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # ── TIMELINE ─────────────────────────────────────────────────
    ax = fig.add_subplot(gs[9:16, :])
    ax.axis("off"); ax.set_facecolor(BG)
    ax.set_title("TIMELINE", color=PINK, fontsize=11,
                 pad=12, fontweight="bold")
    timeline = data["timeline"]
    n = len(timeline)
    ax.plot([0.5, 0.5], [0.02, 0.92], color=CYAN, linewidth=2, alpha=0.4)
    for i, item in enumerate(timeline):
        y = 0.88 - i * (0.82 / (n - 1)) if n > 1 else 0.5
        ax.plot(0.5, y, "o", color=PINK, markersize=8, zorder=5)
        period = item.get("period", item.get("month", ""))
        event  = item.get("event", "")
        if i % 2 == 0:
            ax.text(0.46, y, period, ha="right", va="center",
                    fontsize=9, fontweight="bold", color=CYAN)
            ax.text(0.46, y - 0.04, event, ha="right", va="center",
                    fontsize=8, color=WHITE, alpha=0.85)
        else:
            ax.text(0.54, y, period, ha="left", va="center",
                    fontsize=9, fontweight="bold", color=CYAN)
            ax.text(0.54, y - 0.04, event, ha="left", va="center",
                    fontsize=8, color=WHITE, alpha=0.85)

    # ── IMPACTS ──────────────────────────────────────────────────
    ax = fig.add_subplot(gs[16:19, 0:3])
    ax.axis("off"); ax.set_facecolor(BG)
    ax.set_title("NOTABLE IMPACTS", color=PINK, fontsize=10,
                 pad=8, fontweight="bold")
    for idx, it in enumerate(data.get("impacts", [])):
        ax.text(0.04, 0.85 - idx * 0.18, f"\u25b8 {it}",
                transform=ax.transAxes, color=WHITE, fontsize=8)

    # ── CULTURE SIGNALS ──────────────────────────────────────────
    ax = fig.add_subplot(gs[16:19, 3:6])
    ax.axis("off"); ax.set_facecolor(BG)
    ax.set_title("CULTURE SIGNALS", color=PINK, fontsize=10,
                 pad=8, fontweight="bold")
    for idx, sig in enumerate(data.get("culture_signals", [])):
        ax.text(0.04, 0.85 - idx * 0.18, f"\u2726 {sig}",
                transform=ax.transAxes, color=LIME, fontsize=8)

    # ── BUZZWORDS ────────────────────────────────────────────────
    ax = fig.add_subplot(gs[19:20, :])
    ax.axis("off"); ax.set_facecolor(BG)
    bw = data.get("buzzwords", [])
    ax.text(0.5, 0.7, "BUZZWORDS", ha="center", fontsize=10,
            fontweight="bold", color=PINK)
    ax.text(0.5, 0.20, "   \u2022   ".join(bw), ha="center",
            fontsize=10, color=CYAN)

    # ── SOURCES ──────────────────────────────────────────────────
    ax = fig.add_subplot(gs[20:21, :])
    ax.axis("off"); ax.set_facecolor(BG)
    sources = data.get("sources_placeholder", [])
    ax.text(0.5, 0.5, "  |  ".join(sources), ha="center",
            fontsize=6, color=WHITE, alpha=0.4)

    # ── FOOTER ───────────────────────────────────────────────────
    ax = fig.add_subplot(gs[21:22, :])
    ax.axis("off"); ax.set_facecolor(BG)
    ax.text(0.5, 0.5,
            f"Generated by {data['meta']['generated_by']}  \u2022  "
            f"{data['meta']['region']}  \u2022  {data['meta']['year']}",
            ha="center", fontsize=7, color=WHITE, alpha=0.35)

    # ── SAVE ─────────────────────────────────────────────────────
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"Phone infographic saved to {out}")
    return out


if __name__ == "__main__":
    render(load())
