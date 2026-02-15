import json
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os

DATA_PATH = data.json
OUT = output_infographic.png

def load_data(path=DATA_PATH):
    with open(path, r) as f:
        return json.load(f)

def _draw_basic(ax, title, subtitle):
    ax.set_title(title, color=#00f2ea, fontsize=18, pad=20)
    ax.text(0.5,0.5, subtitle, ha=center, va=center, color=white)

def generate_image(data, out_path=OUT):
    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor(#0f0f1a)
    ax.set_facecolor(#0f0f1a)
    ax.axis(off)
    _draw_basic(ax, data.get(title,Infographic), data.get(subtitle,Subtitle))
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches=tight, facecolor=#0f0f1a)
    plt.close(fig)
    return out_path

def main():
    data = load_data()
    out = generate_image(data)
    print(f"Generated {out}")

if __name__ == __main__:
    main()
