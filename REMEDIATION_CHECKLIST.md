# OU.edu Remediation Checklist

## Critical (Fix Immediately)

- [ ] Disable TRACE method on www.ou.edu
  - Add `TraceEnable off` to Apache config
  - Or filter at F5 BIG-IP

- [ ] Change SPF record to hardfail
  - Current: `v=spf1 ... ~all`
  - Change to: `v=spf1 ... -all`

- [ ] Change DMARC policy to reject
  - Current: `v=DMARC1;p=quarantine`
  - Change to: `v=DMARC1;p=reject`

## High (Fix Within 1 Week)

- [ ] Remove X-FEServer header from Exchange
  - Add F5 iRule to strip header
  - Or configure Exchange to not send it

- [ ] Patch BeyondTrust for CVE-2024-12356
  - Check current version
  - Apply latest security patch

## Medium (Fix Within 1 Month)

- [ ] Disable Drupal cache-tags header
  - Edit settings.php
  - Or configure Varnish to strip it

- [ ] Remove technician names from BeyondTrust page
  - Edit public-facing page
  - Remove PII exposure

## Low (Fix When Possible)

- [ ] Verify .git directory is not accessible
  - Current: 403 (blocked by Pantheon)
  - Confirm no bypass possible

- [ ] Update Apache to latest version
  - Current: 2.4.37 / 2.4.6
  - Target: Latest stable
