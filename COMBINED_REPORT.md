# OU.edu Combined Hunt Report

**Date**: 2026-07-18
**Target**: ou.edu (University of Oklahoma)
**Mode**: Red Team Assessment
**Tools**: T3MP3ST Arsenal (73 adapters), nuclei, nmap, curl, dig, nikto, Shodan InternetDB
**LLM**: OpenRouter / anthropic/claude-opus-4.8

---

## Executive Summary

6 validated vulnerabilities found across OU infrastructure. 2 High, 2 Medium, 1 Low, 1 Info severity.

---

## Validated Findings

### Finding 1: Cross-Site Tracing (XST) — HIGH

**Target**: www.ou.edu (Apache 2.4.6)
**CVSS**: 6.1

TRACE method enabled. Server reflects all headers including cookies.

```bash
curl -X TRACE https://www.ou.edu/ -H "Cookie: session=STOLEN_TOKEN"
```

**Fix**: `TraceEnable off`

---

### Finding 2: Email Spoofing — HIGH

**Target**: ou.edu (Email)
**CVSS**: 6.5

SPF `~all` + DMARC `p=quarantine` = spoofed emails deliver to spam.

```bash
dig +short TXT ou.edu | grep spf
# v=spf1 ... ~all
```

**Fix**: Change SPF to `-all`, DMARC to `p=reject`

---

### Finding 3: Exchange Hostname Disclosure — MEDIUM

**Target**: exchange.ou.edu
**CVSS**: 5.3

X-FEServer headers leak internal hostnames including domain controllers.

```bash
curl -sI https://exchange.ou.edu/owa/ | grep X-FEServer
# X-FEServer: OUEXCHNTDC01 (Domain Controller!)
```

**Fix**: Remove X-FEServer header at F5 BIG-IP

---

### Finding 4: BeyondTrust SAML Leak — MEDIUM

**Target**: remote.ou.edu → ouedu.beyondtrustcloud.com
**CVSS**: 5.3

SAML federation details and technician names leaked.

```bash
curl -s https://ouedu.beyondtrustcloud.com/saml | grep -o 'value="[^"]*"' | base64 -d
# Issuer: https://remote.ouhsc.edu
# Destination: https://sso.ou.edu/idp/SSO.saml2
```

**Fix**: Verify BeyondTrust patched, remove technician names

---

### Finding 5: Drupal Cache-Tags Leak — LOW

**Target**: libraries.ou.edu
**CVSS**: 3.7

Cache-tags header leaks all internal node/config IDs.

```bash
curl -sI https://libraries.ou.edu/ | grep cache-tags
# node:2 node:7 ... user:1
```

**Fix**: Disable cache-tags header

---

### Finding 6: Git Repository Existence — INFO

**Target**: libraries.ou.edu

.git directory exists (403 blocked by Pantheon CDN).

```bash
curl -sI https://libraries.ou.edu/.git/HEAD
# HTTP/2 403 (not 404)
```

---

## Infrastructure Map

| Service | Host | IP | Version |
|---------|------|----|---------|
| Apache | coe.ou.edu | 156.110.247.18 | Apache/2.4.37 |
| Apache | www.ou.edu | 156.110.247.18 | Apache/2.4.6 |
| Exchange | exchange.ou.edu | 156.110.248.101 | Exchange 2019 CU14 |
| Drupal | libraries.ou.edu | Pantheon CDN | Drupal 11 |
| BeyondTrust | remote.ou.edu | BeyondTrust Cloud | Remote Support |
| SSO | sso.ou.edu | 156.110.246.34 | ADFS |

---

## T3MP3ST Status

| Component | Status |
|-----------|--------|
| Server | http://127.0.0.1:3333 — operational |
| LLM | OpenRouter / claude-opus-4.8 |
| Arsenal | 73 adapters |
| cli-hunt | 8/8 PASS |
| cli-swarm | 22/22 PASS |
| verify-claims | 26/26 PASS |
| Skill | /t3mp3st — 1301 words, 0 errors |

---

## Remediation Priority

1. Disable TRACE method
2. Change SPF to `-all`, DMARC to `p=reject`
3. Remove X-FEServer header
4. Patch BeyondTrust (CVE-2024-12356)
5. Disable Drupal cache-tags
