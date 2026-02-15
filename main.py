import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from PIL import Image, ImageDraw, ImageFont
import io

# Visual Config (Teen Style: Dark Mode + Neon)
STYLE = {
    "bg_color": "#0f0f1a",        # Deep dark blue/black
    "text_main": "#ffffff",       # White
    "accent_1": "#00f2ea",        # Cyan / Neon Blue
    "accent_2": "#ff0050",        # TikTok Red/Pink
    "accent_3": "#ccff00",        # Lime Green
    "font_family": "sans-serif"
}

def load_data(path):
    with open(path, 'r') as f:
        return json.load(f)

def create_infographic(data):
    # Setup Figure
    fig = plt.figure(figsize=(10, 16), facecolor=STYLE['bg_color'])
    gs = GridSpec(12, 6, figure=fig)
    fig.patch.set_facecolor(STYLE['bg_color'])

    # Title Section
    ax_header = fig.add_subplot(gs[0:2, :])
    ax_header.set_facecolor(STYLE['bg_color'])
    ax_header.axis('off')
    
    ax_header.text(0.5, 0.7, data['title'], 
                   ha='center', va='center', 
                   fontsize=40, fontweight='bold', 
                   color=STYLE['accent_1'], fontfamily=STYLE['font_family'])
    
    ax_header.text(0.5, 0.45, f"{data['subtitle']} | {data['meta']['region']} | {data['meta']['year']}", 
                   ha='center', va='center', 
                   fontsize=14, color=STYLE['text_main'], alpha=0.8)

    # Big Stats Row
    ax_stats = fig.add_subplot(gs[2:4, :])
    ax_stats.set_facecolor(STYLE['bg_color'])
    ax_stats.axis('off')
    
    stats = list(data['stats'].items())
    for i, (key, val) in enumerate(stats):
        x_pos = (i + 1) / (len(stats) + 1)
        ax_stats.text(x_pos, 0.6, val, ha='center', fontsize=32, fontweight='bold', color=STYLE['accent_3'])
        ax_stats.text(x_pos, 0.4, key.replace('_', ' ').upper(), ha='center', fontsize=10, color=STYLE['text_main'])

    # Platform Donut Chart
    ax_pie = fig.add_subplot(gs[4:7, 0:3])
    ax_pie.set_facecolor(STYLE['bg_color'])
    
    platforms = data['platforms']
    sizes = [p['percent'] for p in platforms]
    labels = [p['name'] for p in platforms]
    colors = [p.get('color', 'gray') for p in platforms]
    
    wedges, texts, autotexts = ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                          startangle=90, colors=colors, 
                                          textprops=dict(color="white"), pctdistance=0.85)
    
    # Draw circle for donut
    centre_circle = plt.Circle((0,0),0.70,fc=STYLE['bg_color'])
    ax_pie.add_artist(centre_circle)
    ax_pie.set_title("PLATFORM DOMINANCE", color=STYLE['text_main'], fontsize=12, pad=20)

    # Demographics Bar Chart
    ax_bar = fig.add_subplot(gs[4:7, 3:6])
    ax_bar.set_facecolor(STYLE['bg_color'])
    
    demos = data['demographics']
    ages = list(demos.keys())
    values = list(demos.values())
    
    bars = ax_bar.bar(ages, values, color=STYLE['accent_1'])
    ax_bar.set_title("AGE DISTRIBUTION", color=STYLE['text_main'], fontsize=12, pad=20)
    ax_bar.tick_params(axis='x', colors='white')
    ax_bar.tick_params(axis='y', colors='white')
    for spine in ax_bar.spines.values():
        spine.set_edgecolor(STYLE['bg_color']) # Hide borders
    
    # Timeline
    ax_time = fig.add_subplot(gs[7:12, :])
    ax_time.set_facecolor(STYLE['bg_color'])
    ax_time.axis('off')
    
    timeline = data['timeline']
    ax_time.text(0.5, 0.95, "2025 TIMELINE", ha='center', fontsize=14, color=STYLE['text_main'], fontweight='bold')
    
    # Draw vertical line
    ax_time.plot([0.5, 0.5], [0.1, 0.85], color=STYLE['accent_1'], linewidth=2)
    
    for i, item in enumerate(timeline):
        y_pos = 0.8 - (i * 0.2)
        # Dot
        ax_time.plot(0.5, y_pos, 'o', color=STYLE['accent_2'], markersize=10)
        
        # Text alternating sides
        if i % 2 == 0:
            ax_time.text(0.45, y_pos, f"{item['month']}: {item['event']}", ha='right', va='center', color='white', fontsize=11)
        else:
            ax_time.text(0.55, y_pos, f"{item['month']}: {item['event']}", ha='left', va='center', color='white', fontsize=11)

    plt.tight_layout()
    output_path = "output_infographic.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor=STYLE['bg_color'])
    print(f"Infographic saved to {output_path}")

if __name__ == "__main__":
    data = load_data('data.json')
    create_infographic(data)
