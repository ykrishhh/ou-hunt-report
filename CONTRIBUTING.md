# Contributing

Contributions to improve the reports, add diagrams, or extend the asset
generators are welcome.

## Asset generation

- `assets/gen_assets.py` — regenerates portable SVG/PNG diagrams from `FINDINGS`
- `understand/gen_graph.py` — regenerates the knowledge graph and Mermaid output

Run after editing findings:

```bash
python3 assets/gen_assets.py
python3 understand/gen_graph.py
```

## Structure

```
reports/   written reports
pocs/      proof-of-concept exploits
diagrams/  mermaid source + interactive viewer
dashboard/ interactive HTML dashboard
assets/    portable SVG/PNG (render on GitHub app + web)
understand/ knowledge graph (Understand-Anything schema)
```

## License

By contributing, you agree your contributions are licensed under the MIT License.
