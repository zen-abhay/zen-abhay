import json

# GitHub green color palette (0 = none, 5 = brightest neon)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap():
    print("Reading contribution data...")
    try:
        with open("data/contributions.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: data/contributions.json not found. Run Step 3 first!")
        return

    days = data["days"]
    box_size = 11
    gap = 3
    padding = 20
    
    weeks = len(days) // 7 + 1
    width = weeks * (box_size + gap) + (padding * 2)
    height = 7 * (box_size + gap) + (padding * 2)
    
    # SVG Header and Animation Styles
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '  <style>',
        '    .bg { fill: #0d1117; rx: 6px; }',
        '    .day { rx: 2px; opacity: 0; animation: slideDown 0.4s forwards; }',
        '    @keyframes slideDown {',
        '      from { opacity: 0; transform: translateY(-10px); }',
        '      to { opacity: 1; transform: translateY(0); }',
        '    }',
        '  </style>',
        f'  <rect width="{width}" height="{height}" class="bg"/>'
    ]
    
    # Generate each box on the grid
    for idx, day in enumerate(days):
        week = idx // 7
        dow = idx % 7
        x = padding + week * (box_size + gap)
        y = padding + dow * (box_size + gap)
        color = PALETTE[min(day["level"], len(PALETTE) - 1)]
        delay = (week + dow) * 0.015  # Creates a diagonal cascade animation effect
        
        svg.append(f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" class="day" style="animation-delay: {delay:.3f}s;"/>')

    svg.append('</svg>')
    
    # Save SVG file to root directory
    output_path = "contrib-heatmap.svg"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"Success! SVG rendered and saved as {output_path}")

if __name__ == "__main__":
    render_heatmap()