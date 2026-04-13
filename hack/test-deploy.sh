#!/usr/bin/env bash
set -euo pipefail

# test-deploy.sh - Smoke test against a running slack-qr-bot container
#
# Usage:
#   ./hack/test-deploy.sh [PORT]
#   make deploy-smoke

PORT="${1:-8080}"
BASE="http://localhost:${PORT}"

PASS=0
FAIL=0

check() {
    local desc="$1" result="$2"
    if [ "$result" = "true" ]; then
        echo "  ✓ ${desc}"
        PASS=$((PASS + 1))
    else
        echo "  ✗ ${desc}"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== Smoke Test: ${BASE} ==="
echo ""

# ---------------------------------------------------------------
# 1. Wait for server
# ---------------------------------------------------------------
echo "[1/6] Server health..."
for i in 1 2 3 4 5; do
    STATUS=$(curl -s -o /dev/null -w '%{http_code}' "${BASE}/health" 2>/dev/null) || true
    if [ "$STATUS" = "200" ]; then break; fi
    if [ "$i" = "5" ]; then
        echo "  ✗ Server not responding after 5 attempts"
        exit 1
    fi
    sleep 1
done
check "GET /health => 200" "true"

# ---------------------------------------------------------------
# 2. Health response is JSON
# ---------------------------------------------------------------
echo "[2/6] Health response structure..."
HEALTH_BODY=$(curl -s "${BASE}/health" 2>/dev/null)
check "Health returns JSON" "$(echo "$HEALTH_BODY" | python3 -c 'import sys,json; json.load(sys.stdin); print("true")' 2>/dev/null || echo 'false')"

# ---------------------------------------------------------------
# 3. QR endpoint exists
# ---------------------------------------------------------------
echo "[3/6] QR endpoint..."
QR_STATUS=$(curl -s -o /dev/null -w '%{http_code}' -X POST "${BASE}/generate-qr" 2>/dev/null) || true
check "POST /generate-qr responds" "$([ "$QR_STATUS" != "000" ] && echo true || echo false)"

# ---------------------------------------------------------------
# 4. Channels endpoint
# ---------------------------------------------------------------
echo "[4/6] Channels endpoint..."
CH_STATUS=$(curl -s -o /dev/null -w '%{http_code}' "${BASE}/channels" 2>/dev/null) || true
check "GET /channels responds" "$([ "$CH_STATUS" != "000" ] && echo true || echo false)"

# ---------------------------------------------------------------
# 5. Swagger docs
# ---------------------------------------------------------------
echo "[5/6] Swagger docs..."
SWAGGER_STATUS=$(curl -s -o /dev/null -w '%{http_code}' "${BASE}/apidocs/" 2>/dev/null) || true
check "GET /apidocs/ => 200" "$([ "$SWAGGER_STATUS" = "200" ] && echo true || echo false)"

# ---------------------------------------------------------------
# 6. Unknown route returns 404
# ---------------------------------------------------------------
echo "[6/6] Unknown route..."
UNKNOWN=$(curl -s -o /dev/null -w '%{http_code}' "${BASE}/nonexistent-route-xyz" 2>/dev/null) || true
check "GET /unknown => 404" "$([ "$UNKNOWN" = "404" ] && echo true || echo false)"

# ---------------------------------------------------------------
# Summary
# ---------------------------------------------------------------
echo ""
TOTAL=$((PASS + FAIL))
echo "=== Results: ${PASS}/${TOTAL} passed, ${FAIL} failed ==="

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
