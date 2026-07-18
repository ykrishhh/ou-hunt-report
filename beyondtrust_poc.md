# BeyondTrust Remote Support POC

**Target**: remote.ou.edu → ouedu.beyondtrustcloud.com
**Product**: BeyondTrust Remote Support / Password Safe
**Severity**: Medium-High (pending CVE verification)

## Findings

1. **SAML Endpoint Active**: /saml/sso returns 405, /saml/slo returns 401
2. **SAML Metadata Accessible**: Full SAML page with form at /saml
3. **Technician Names Leaked**: Page reveals IT staff names
4. **Known CVEs**:
   - CVE-2024-12356: Command Injection (Critical, KEV)
   - CVE-2024-12357: Authentication Bypass
   - CVE-2023-42822: Authentication Bypass

## Attack Scenario

1. Attacker discovers BeyondTrust at remote.ou.edu
2. SAML endpoint is accessible
3. If vulnerable to CVE-2024-12356: Remote code execution
4. If vulnerable to CVE-2024-12357: Authentication bypass
5. Compromise = access to remote support sessions

## Remediation

- Verify BeyondTrust version is patched for CVE-2024-12356/12357
- Restrict SAML endpoints to internal network
- Remove technician names from public page
