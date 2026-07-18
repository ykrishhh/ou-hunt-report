#!/usr/bin/env python3
"""
Generate portable SVG assets for the OU hunt repo.
SVGs render on GitHub web AND the mobile app (unlike Mermaid, which the app
does not render live). Output to assets/.
Run: python3 assets/gen_assets.py
"""
import os, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

FINDINGS = [
    ("XST (TRACE Method)", "HIGH", "#ff4444", "www.ou.edu"),
    ("Email Spoofing", "HIGH", "#ff4444", "ou.edu"),
    ("Exchange Hostname Disclosure", "MEDIUM", "#ffaa00", "exchange.ou.edu"),
    ("BeyondTrust SAML Leak", "MEDIUM", "#ffaa00", "remote.ou.edu"),
    ("Drupal Cache-Tags Leak", "LOW", "#44ff44", "libraries.ou.edu"),
    ("Git Repository Existence", "INFO", "#4488ff", "libraries.ou.edu"),
]
SEV_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
sev_counts = {s: 0 for s in SEV_ORDER}
for _, sev, _, _ in FINDINGS:
    sev_counts[sev] += 1

def esc(s): return html.escape(s)

# ---------- 1. Severity donut ----------
def severity_svg():
    cx, cy, r, w = 160, 160, 110, 34
    total = sum(sev_counts.values()) or 1
    angles = []
    start = -90.0
    colors = {"CRITICAL": "#aa00ff", "HIGH": "#ff4444", "MEDIUM": "#ffaa00", "LOW": "#44ff44", "INFO": "#4488ff"}
    segs = ""
    for s in SEV_ORDER:
        n = sev_counts[s]
        if not n:
            continue
        sweep = 360.0 * n / total
        end = start + sweep
        import math
        x1 = cx + r * math.cos(math.radians(start)); y1 = cy + r * math.sin(math.radians(start))
        x2 = cx + r * math.cos(math.radians(end)); y2 = cy + r * math.sin(math.radians(end))
        large = 1 if sweep > 180 else 0
        inner_r = r - w
        xi1 = cx + inner_r * math.cos(math.radians(start)); yi1 = cy + inner_r * math.sin(math.radians(start))
        xi2 = cx + inner_r * math.cos(math.radians(end)); yi2 = cy + inner_r * math.sin(math.radians(end))
        segs += (f'<path d="M {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 1 {x2:.1f} {y2:.1f} '
                 f'L {xi2:.1f} {yi2:.1f} A {inner_r} {inner_r} 0 {large} 0 {xi1:.1f} {yi1:.1f} Z" '
                 f'fill="{colors[s]}" stroke="#0d1117" stroke-width="2"/>')
        start = end
    legend = ""
    ly = 30
    for s in SEV_ORDER:
        if not sev_counts[s]:
            continue
        legend += (f'<rect x="320" y="{ly}" width="16" height="16" fill="{colors[s]}" rx="3"/>'
                   f'<text x="344" y="{ly+13}" fill="#c9d1d9" font-family="monospace" font-size="14">{s}: {sev_counts[s]}</text>')
        ly += 26
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="320" viewBox="0 0 520 320">'
            f'<rect width="520" height="320" fill="#0d1117"/>'
            f'<text x="160" y="24" fill="#c9d1d9" font-family="monospace" font-size="16" text-anchor="middle">Findings by Severity</text>'
            f'<g transform="translate(0,0)">{segs}</g>'
            f'<text x="160" y="166" fill="#fff" font-family="monospace" font-size="22" text-anchor="middle">{total}</text>'
            f'{legend}</svg>')

# ---------- 2. Attack chain (horizontal flow) ----------
def attackchain_svg():
    stages = [
        ("Targets", "#4488ff", ["www.ou.edu", "exchange.ou.edu", "remote.ou.edu", "libraries.ou.edu"]),
        ("Recon / Leak", "#ffaa00", ["Hostname Disclosure", "SAML Leak", "Cache-Tags Leak"]),
        ("Exploit", "#ff4444", ["XST TRACE", "Email Spoofing"]),
        ("Impact", "#aa00ff", ["Account Takeover", "AD Compromise"]),
    ]
    col_w, x0, y0, gap = 170, 20, 50, 20
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="740" height="300" viewBox="0 0 740 300">',
           f'<rect width="740" height="300" fill="#0d1117"/>']
    for ci, (title, color, items) in enumerate(stages):
        x = x0 + ci * col_w
        svg.append(f'<rect x="{x}" y="{y0}" width="{col_w-20}" height="220" fill="#161b22" stroke="{color}" stroke-width="2" rx="8"/>')
        svg.append(f'<text x="{x+(col_w-20)/2}" y="{y0+24}" fill="{color}" font-family="monospace" font-size="14" text-anchor="middle" font-weight="bold">{esc(title)}</text>')
        for ii, it in enumerate(items):
            yy = y0 + 50 + ii * 34
            svg.append(f'<rect x="{x+12}" y="{yy}" width="{col_w-44}" height="26" fill="#21262d" rx="4"/>')
            svg.append(f'<text x="{x+(col_w-20)/2}" y="{yy+18}" fill="#c9d1d9" font-family="monospace" font-size="11" text-anchor="middle">{esc(it)}</text>')
        if ci < len(stages) - 1:
            ax = x + col_w - 20
            svg.append(f'<path d="M {ax} 160 L {ax+gap} 160" stroke="{color}" stroke-width="2" marker-end="url(#ar)"/>')
    svg.append('<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#8b949e"/></marker></defs>')
    svg.append('</svg>')
    return "".join(svg)

# ---------- 3. Knowledge graph (simple force-ish layout, fixed) ----------
def knowledgegraph_svg():
    targets = ["www.ou.edu", "exchange.ou.edu", "remote.ou.edu", "libraries.ou.edu"]
    nodes = []
    # positions: targets left, findings mid, reports right
    ty = 40
    for i, t in enumerate(targets):
        nodes.append((f"T{i}", t, 60, 40 + i * 60, "#4488ff"))
    fnames = [f[0] for f in FINDINGS]
    for i, fname in enumerate(fnames):
        sev = FINDINGS[i][1]
        color = "#ff4444" if sev=="HIGH" else "#ffaa00" if sev=="MEDIUM" else "#44ff44" if sev=="LOW" else "#4488ff"
        nodes.append((f"F{i}", fname, 300, 40 + i * 55, color))
    edges = [(f"T{0}", f"F{0}"), (f"T{1}", f"F{2}"), (f"T{2}", f"F{3}"), (f"T{3}", f"F{4}"), (f"T{3}", f"F{5}")]
    edges += [(f"T{0}", f"F{1}")]  # email spoofing -> ou.edu (approx)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="360" viewBox="0 0 520 360">',
           f'<rect width="520" height="360" fill="#0d1117"/>']
    for a, b in edges:
        na = next(n for n in nodes if n[0] == a)
        nb = next(n for n in nodes if n[0] == b)
        svg.append(f'<line x1="{na[2]}" y1="{na[3]}" x2="{nb[2]}" y2="{nb[3]}" stroke="#30363d" stroke-width="1.5"/>')
    for nid, label, x, y, color in nodes:
        svg.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}"/>')
        svg.append(f'<text x="{x+12}" y="{y+4}" fill="#c9d1d9" font-family="monospace" font-size="11">{esc(label)}</text>')
    svg.append('</svg>')
    return "".join(svg)

for name, fn in [("severity.svg", severity_svg), ("attack-chain.svg", attackchain_svg), ("knowledge-graph.svg", knowledgegraph_svg)]:
    with open(os.path.join(ASSETS, name), "w") as f:
        f.write(fn())
    print("wrote assets/" + name)
