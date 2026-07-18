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

## Diagrams

### Attack Chain

```mermaid
graph TD
    A[Attacker] -->|1. Recon| B[Exchange Hostname Disclosure]
    A -->|2. Recon| C[BeyondTrust SAML Leak]
    A -->|3. Recon| D[Drupal Cache-Tags Leak]
    B --> E[Identify DC: OUEXCHNTDC01]
    C --> F[Map SAML Federation]
    D --> G[Enumerate Internal IDs]
    E --> H{Exploit Phase}
    F --> H
    G --> H
    H -->|XST| I[Session Hijacking]
    H -->|Email Spoof| J[Phishing Attack]
    I --> K[Account Takeover]
    J --> L[Credential Theft]
    K --> M[AD Compromise]
    L --> M
    M --> N[Forest Compromise]
```

### Infrastructure Map

```mermaid
graph LR
    subgraph "OU Infrastructure"
        A[coe.ou.edu<br/>Apache/2.4.37]
        B[www.ou.edu<br/>Apache/2.4.6]
        C[exchange.ou.edu<br/>Exchange 2019 CU14]
        D[libraries.ou.edu<br/>Drupal 11]
        E[remote.ou.edu<br/>BeyondTrust]
        F[sso.ou.edu<br/>ADFS]
    end
    
    A -->|shares IP| B
    C -->|ADFS SSO| F
    E -->|SAML| F
    D -->|Drupal| G[Pantent CDN]
    B -->|BIG-IP| H[F5 Load Balancer]
    C -->|BIG-IP| H
```

### Findings Severity

```mermaid
graph TD
    subgraph "HIGH"
        A1[XST - TRACE Method<br/>www.ou.edu]
        A2[Email Spoofing<br/>ou.edu]
    end
    
    subgraph "MEDIUM"
        B1[Exchange Hostname<br/>exchange.ou.edu]
        B2[BeyondTrust SAML<br/>remote.ou.edu]
    end
    
    subgraph "LOW"
        C1[Drupal Cache-Tags<br/>libraries.ou.edu]
    end
    
    subgraph "INFO"
        D1[Git Repo Exists<br/>libraries.ou.edu]
    end
    
    A1 -->|Session Hijacking| E[Impact]
    A2 -->|Phishing| E
    B1 -->|Infra Mapping| E
    B2 -->|Social Engineering| E
    E --> F[Account Takeover]
    E --> G[Data Theft]
    E --> H[AD Compromise]
```

## Interactive Diagrams

Open `DIAGRAMS.html` to view interactive Mermaid diagrams in browser.

## Quick Start

1. Open `DASHBOARD.html` for visual overview
2. Read `FINAL_COMBINED.md` for detailed findings
3. Review `ATTACK_MATRIX.md` for attack chains
4. Check `REMEDIATION_CHECKLIST.md` for fixes

## POCs

- `xst_poc.html` - Browser-based XST exploit
- `xst_poc.sh` - Bash exploit script
- `email_spoof_poc.py` - Email spoofing demonstration

## Tools Used

- T3MP3ST Arsenal (73 adapters)
- nuclei, nmap, curl, dig, nikto
- Shodan InternetDB

## License

MIT
