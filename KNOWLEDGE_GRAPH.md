# OU.edu Hunt — Knowledge Graph

## Targets (6)

| Target | IP | Version | Role |
|--------|-----|---------|------|
| coe.ou.edu | 156.110.247.18 | Apache/2.4.37 | Web server |
| www.ou.edu | 156.110.247.18 | Apache/2.4.6 | Main website |
| exchange.ou.edu | 156.110.248.101 | Exchange 2019 CU14 | Email |
| libraries.ou.edu | Pantheon CDN | Drupal 11 | Library site |
| remote.ou.edu | BeyondTrust Cloud | Remote Support | IT support |
| sso.ou.edu | 156.110.246.34 | ADFS | Authentication |

## Findings (6)

### HIGH Severity
1. **XST (TRACE Method)** — www.ou.edu
   - TRACE method reflects cookies
   - Impact: Session hijacking
   - POC: xst_poc.html, xst_poc.sh

2. **Email Spoofing** — ou.edu
   - SPF ~all + DMARC quarantine
   - Impact: Phishing attacks
   - POC: email_spoof_poc.py

### MEDIUM Severity
3. **Exchange Hostname Disclosure** — exchange.ou.edu
   - X-FEServer leaks OUEXCHNTDC01/02
   - Impact: Infrastructure mapping
   - Note: Domain controllers exposed

4. **BeyondTrust SAML Leak** — remote.ou.edu
   - SAML federation details leaked
   - Technician names exposed
   - Impact: Social engineering

### LOW Severity
5. **Drupal Cache-Tags Leak** — libraries.ou.edu
   - Cache-tags header leaks IDs
   - Impact: Internal enumeration

### INFO
6. **Git Repository Existence** — libraries.ou.edu
   - .git directory exists (403 blocked)
   - Impact: Source code access potential

## Relationships

```
coe.ou.edu ──shares IP──> www.ou.edu
    │
    └──same Apache──> devday.zero.ou.edu

exchange.ou.edu ──ADFS SSO──> sso.ou.edu
    │
    └──X-FEServer──> OUEXCHNTDC01 (DC)

remote.ou.edu ──SAML──> sso.ou.edu
    │
    └──leaks──> technician names

libraries.ou.edu ──Drupal──> Pantheon CDN
    │
    └──.git──> exists (403)
```

## Attack Chains

### Chain 1: Session Hijacking
```
Attacker → hosts malicious page → victim visits
  → XST reflects cookies → attacker steals session
  → Account takeover
```

### Chain 2: Phishing Attack
```
Attacker → spoofs admin@ou.edu → sends email
  → SPF softfail → lands in spam
  → User checks spam → clicks link → credentials stolen
```

### Chain 3: AD Compromise
```
Attacker → discovers Exchange → reads X-FEServer header
  → identifies OUEXCHNTDC01 (domain controller)
  → targets DC → forest compromise
```

## Remediation Priority

1. **CRITICAL**: Disable TRACE method (www.ou.edu)
2. **CRITICAL**: Change SPF to -all, DMARC to p=reject
3. **HIGH**: Remove X-FEServer header (exchange.ou.edu)
4. **MEDIUM**: Patch BeyondTrust (CVE-2024-12356)
5. **LOW**: Disable Drupal cache-tags
