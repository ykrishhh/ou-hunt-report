# OU.edu Red Team Hunt

A comprehensive security assessment of the University of Oklahoma's infrastructure, identifying 6 validated vulnerabilities with working proof-of-concept exploits.

## Findings

| # | Finding | Severity | Target |
|---|---------|----------|--------|
| 1 | XST (TRACE Method) | HIGH | www.ou.edu |
| 2 | Email Spoofing | HIGH | ou.edu |
| 3 | Exchange Hostname Disclosure | MEDIUM | exchange.ou.edu |
| 4 | BeyondTrust SAML Leak | MEDIUM | remote.ou.edu |
| 5 | Drupal Cache-Tags Leak | LOW | libraries.ou.edu |
| 6 | Git Repository Existence | INFO | libraries.ou.edu |

## Attack Chain

```mermaid
graph TD
    A[Attacker] --> B[Exchange Hostname Disclosure]
    A --> C[BeyondTrust SAML Leak]
    A --> D[Drupal Cache-Tags Leak]
    B --> E[Identify Domain Controller]
    C --> F[Map SAML Federation]
    D --> G[Enumerate Internal IDs]
    E --> H[Exploit Phase]
    F --> H
    G --> H
    H --> I[Session Hijacking via XST]
    H --> J[Email Spoofing Attack]
    I --> K[Account Takeover]
    J --> L[Credential Theft]
    K --> M[AD Compromise]
    L --> M
    M --> N[Forest Compromise]
```

## Infrastructure Map

```mermaid
graph LR
    A[coe.ou.edu] -->|shares IP| B[www.ou.edu]
    C[exchange.ou.edu] --> D[sso.ou.edu]
    E[remote.ou.edu] --> D
    F[libraries.ou.edu] --> G[Pantent CDN]
    B --> H[F5 BIG-IP]
    C --> H
```

## Findings Severity

```mermaid
graph TD
    A1[XST - TRACE Method] --> E[Impact]
    A2[Email Spoofing] --> E
    B1[Exchange Hostname] --> E
    B2[BeyondTrust SAML] --> E
    E --> F[Account Takeover]
    E --> G[Data Theft]
    E --> H[AD Compromise]

    style A1 fill:#ff4444
    style A2 fill:#ff4444
    style B1 fill:#ffaa00
    style B2 fill:#ffaa00
    style C1 fill:#44ff44
    style D1 fill:#4444ff
```

## Dashboard

Open `DASHBOARD.html` for an interactive visual overview of all findings.

## Diagrams

Open `DIAGRAMS.html` to view interactive Mermaid diagrams in your browser.

### Mermaid Source Files

| File | Description |
|------|-------------|
| `ATTACK_CHAIN.mmd` | Attack chain flow |
| `INFRASTRUCTURE.mmd` | Infrastructure map |
| `FINDINGS_SEVERITY.mmd` | Severity breakdown |

## POCs

| File | Description |
|------|-------------|
| `xst_poc.html` | Browser-based XST exploit |
| `xst_poc.sh` | Bash exploit script |
| `email_spoof_poc.py` | Email spoofing demonstration |
| `beyondtrust_poc.md` | BeyondTrust findings |

## Reports

| File | Description |
|------|-------------|
| `FINAL_COMBINED.md` | Complete findings report |
| `EXECUTIVE_SUMMARY.md` | High-level summary |
| `ATTACK_MATRIX.md` | Attack techniques and kill chain |
| `REMEDIATION_CHECKLIST.md` | Actionable fix checklist |
| `KNOWLEDGE_GRAPH.md` | Interactive knowledge graph |

## Tools Used

- T3MP3ST Arsenal (73 adapters)
- nuclei, nmap, curl, dig, nikto
- Shodan InternetDB

## License

MIT
