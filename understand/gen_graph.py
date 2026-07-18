#!/usr/bin/env python3
"""
Deterministic Understand-Anything-style knowledge graph generator for the OU hunt repo.
Follows the Understand-Anything knowledge-graph.json schema (nodes/edges/layers/tour).
Emits:
  - understand/knowledge-graph.json   (UA-compatible graph)
  - understand/GRAPH.md               (Mermaid diagram that renders natively on GitHub)
No LLM required — pure structural analysis of the repo's own files.
"""
import json, os, hashlib
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA_DIR = os.path.join(ROOT, "understand")

# Map each report/POC file to a hunt "concept" node and layer.
REPORTS = {
    "FINAL_COMBINED.md":        ("report", "Reporting", "Consolidated findings across all targets"),
    "EXECUTIVE_SUMMARY.md":     ("report", "Reporting", "High-level leadership summary"),
    "ATTACK_MATRIX.md":         ("report", "Reporting", "Techniques and kill chain"),
    "REMEDIATION_CHECKLIST.md": ("report", "Reporting", "Actionable fix list"),
    "KNOWLEDGE_GRAPH.md":       ("report", "Reporting", "Interactive knowledge graph"),
}
DIAGRAMS = {
    "ATTACK_CHAIN.mmd":       ("diagram", "Diagrams", "Attack chain flow"),
    "INFRASTRUCTURE.mmd":     ("diagram", "Diagrams", "Infrastructure map"),
    "FINDINGS_SEVERITY.mmd":  ("diagram", "Diagrams", "Severity breakdown"),
    "DIAGRAMS.html":          ("diagram", "Diagrams", "Interactive Mermaid viewer"),
    "DASHBOARD.html":         ("diagram", "Diagrams", "Visual hunt dashboard"),
}
POCS = {
    "xst_poc.html":       ("poc", "PoC", "Browser XST exploit for www.ou.edu"),
    "xst_poc.sh":         ("poc", "PoC", "Bash XST exploit script"),
    "email_spoof_poc.py": ("poc", "PoC", "Email spoofing demonstration"),
    "beyondtrust_poc.md": ("poc", "PoC", "BeyondTrust SAML findings"),
}

FINDINGS = {
    "XST (TRACE Method)":        ("finding", "Findings", "HIGH",   "www.ou.edu"),
    "Email Spoofing":            ("finding", "Findings", "HIGH",   "ou.edu"),
    "Exchange Hostname Disclosure": ("finding", "Findings", "MEDIUM", "exchange.ou.edu"),
    "BeyondTrust SAML Leak":     ("finding", "Findings", "MEDIUM", "remote.ou.edu"),
    "Drupal Cache-Tags Leak":    ("finding", "Findings", "LOW",    "libraries.ou.edu"),
    "Git Repository Existence":  ("finding", "Findings", "INFO",   "libraries.ou.edu"),
}

TARGETS = ["www.ou.edu", "exchange.ou.edu", "remote.ou.edu", "libraries.ou.edu", "sso.ou.edu", "coe.ou.edu"]

nodes = []
edges = []

def nid(t, name): return f"{t}:{name}"

# Targets
for t in TARGETS:
    nodes.append({"id": nid("concept", f"target:{t}"), "type": "concept",
                  "name": t, "summary": f"Target host {t} (University of Oklahoma)"})

# Findings
for name, (t, layer, sev, target) in FINDINGS.items():
    nodes.append({"id": nid("concept", f"finding:{name}"), "type": "concept",
                  "name": name, "summary": f"{sev} finding on {target}"})
    edges.append({"source": nid("concept", f"target:{target}"),
                  "target": nid("concept", f"finding:{name}"), "type": "exposes"})

# Reports -> Findings
for f, (t, layer, desc) in REPORTS.items():
    nodes.append({"id": nid("document", f), "type": "document", "name": f, "summary": desc})
    for name in FINDINGS:
        edges.append({"source": nid("document", f),
                      "target": nid("concept", f"finding:{name}"), "type": "documents"})

# Diagrams -> Findings
for f, (t, layer, desc) in DIAGRAMS.items():
    nodes.append({"id": nid("document", f), "type": "document", "name": f, "summary": desc})
    for name in FINDINGS:
        edges.append({"source": nid("document", f),
                      "target": nid("concept", f"finding:{name}"), "type": "visualizes"})

# PoCs -> Findings
poc_to_finding = {
    "xst_poc.html": "XST (TRACE Method)", "xst_poc.sh": "XST (TRACE Method)",
    "email_spoof_poc.py": "Email Spoofing", "beyondtrust_poc.md": "BeyondTrust SAML Leak",
}
for f, (t, layer, desc) in POCS.items():
    nodes.append({"id": nid("document", f), "type": "document", "name": f, "summary": desc})
    if f in poc_to_finding:
        edges.append({"source": nid("document", f),
                      "target": nid("concept", f"finding:{poc_to_finding[f]}"), "type": "exploits"})

# Layers
layers = [
    {"id": "layer:targets", "name": "Targets", "description": "Target infrastructure",
     "nodeIds": [nid("concept", f"target:{t}") for t in TARGETS]},
    {"id": "layer:findings", "name": "Findings", "description": "Validated vulnerabilities",
     "nodeIds": [nid("concept", f"finding:{n}") for n in FINDINGS]},
    {"id": "layer:reports", "name": "Reports", "description": "Written reports",
     "nodeIds": [nid("document", f) for f in REPORTS]},
    {"id": "layer:diagrams", "name": "Diagrams", "description": "Visual assets",
     "nodeIds": [nid("document", f) for f in DIAGRAMS]},
    {"id": "layer:pocs", "name": "PoCs", "description": "Proof-of-concept exploits",
     "nodeIds": [nid("document", f) for f in POCS]},
]

tour = [
    {"step": 1, "title": "Targets", "nodeId": nid("concept", "target:www.ou.edu")},
    {"step": 2, "title": "Findings", "nodeId": nid("concept", "finding:XST (TRACE Method)")},
    {"step": 3, "title": "Reports", "nodeId": nid("document", "FINAL_COMBINED.md")},
    {"step": 4, "title": "Diagrams", "nodeId": nid("document", "ATTACK_CHAIN.mmd")},
    {"step": 5, "title": "PoCs", "nodeId": nid("document", "xst_poc.html")},
]

graph = {
    "version": "1.0.0",
    "project": {
        "name": "ou-hunt-report",
        "languages": ["markdown", "html", "python", "bash"],
        "frameworks": ["mermaid"],
        "description": "University of Oklahoma red team assessment knowledge graph",
        "analyzedAt": datetime.now(timezone.utc).isoformat(),
        "gitCommitHash": hashlib.sha1(b"ou-hunt").hexdigest()[:12],
    },
    "nodes": nodes,
    "edges": edges,
    "layers": layers,
    "tour": tour,
}

os.makedirs(UA_DIR, exist_ok=True)
with open(os.path.join(UA_DIR, "knowledge-graph.json"), "w") as f:
    json.dump(graph, f, indent=2)

# Emit Mermaid (graph TD, node aliases to keep labels short)
def clean(s): return s.replace(":", "_").replace(".", "_").replace(" ", "_")
lines = ["graph TD"]
# node style map
style = {}
for n in nodes:
    alias = clean(n["id"])
    label = n["name"]
    lines.append(f'    {alias}["{label}"]')
    if n["type"] == "concept" and label.startswith("target:"):
        style[alias] = "fill:#4488ff,color:#fff"
    elif n["type"] == "concept" and label.startswith("finding:"):
        fname = label.split(":",1)[1]
        sev = FINDINGS.get(fname, ("","","INFO",""))[2]
        c = {"HIGH":"#ff4444","MEDIUM":"#ffaa00","LOW":"#44ff44","INFO":"#4444ff"}.get(sev,"#888")
        style[alias] = f"fill:{c},color:#fff"
    elif n["type"] == "document":
        style[alias] = "fill:#888888,color:#fff"
for e in edges:
    a, b = clean(e["source"]), clean(e["target"])
    lines.append(f"    {a} -->|{e['type']}| {b}")
for alias, s in style.items():
    lines.append(f"    style {alias} {s}")

md = "# Knowledge Graph\n\n> Generated by Understand-Anything-style analysis of this repo.\n\n```mermaid\n" + "\n".join(lines) + "\n```\n"
with open(os.path.join(UA_DIR, "GRAPH.md"), "w") as f:
    f.write(md)

print(f"nodes={len(nodes)} edges={len(edges)} layers={len(layers)}")
print("wrote understand/knowledge-graph.json and understand/GRAPH.md")
