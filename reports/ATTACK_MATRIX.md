# OU.edu Attack Matrix

## Reconnaissance → Exploitation → Impact

| Phase | Finding | Technique | Impact |
|-------|---------|-----------|--------|
| Recon | Exchange Hostname Disclosure | X-FEServer header leak | Internal mapping |
| Recon | BeyondTrust SAML Leak | SAML metadata exposure | Federation mapping |
| Recon | Drupal Cache-Tags Leak | HTTP header leak | Internal IDs |
| Recon | Git Repository Existence | .git directory probe | Source access |
| Exploit | XST (TRACE Method) | Cookie reflection | Session hijacking |
| Exploit | Email Spoofing | SPF softfail | Phishing |
| Impact | Session Hijacking | Cookie theft | Account takeover |
| Impact | Phishing | Spoofed emails | Credential theft |
| Impact | AD Compromise | DC identification | Forest compromise |

## Kill Chain

```
1. Recon: Map infrastructure (Exchange, SSO, Drupal)
2. Enumerate: Find weak points (TRACE, SPF, SAML)
3. Exploit: XST for cookies, spoof emails
4. Pivot: Use stolen sessions for deeper access
5. Impact: Account takeover, data theft, AD compromise
```
