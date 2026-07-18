#!/usr/bin/env python3
"""
Email Spoofing POC for ou.edu
Demonstrates SPF softfail + DMARC quarantine = spoofable emails
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

# Target info
TARGET_DOMAIN = "ou.edu"
SPF_RECORD = "v=spf1 ... ~all"  # Softfail = spoofed emails deliver to spam
DMARC_RECORD = "v=DMARC1;p=quarantine;fo=1"  # Quarantine = not rejected

print(f"Target: {TARGET_DOMAIN}")
print(f"SPF: {SPF_RECORD}")
print(f"DMARC: {DMARC_RECORD}")
print()
print("Attack scenario:")
print("1. Attacker spoofs sender: admin@ou.edu")
print("2. Sends phishing email to faculty/student")
print("3. SPF softfail → email lands in SPAM (not rejected)")
print("4. DMARC quarantine → email quarantined (not blocked)")
print("5. If user checks spam folder, they see spoofed email")
print()
print("This is a valid phishing attack vector.")
print()
print("To exploit:")
print("  1. Use a mail server you control")
print("  2. Set From: admin@ou.edu")
print("  3. Send to target@ou.edu")
print("  4. Email will be delivered to spam folder")
print()
print("Remediation:")
print("  - Change SPF to -all (hardfail)")
print("  - Change DMARC to p=reject")
