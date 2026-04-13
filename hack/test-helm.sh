#!/usr/bin/env bash
set -euo pipefail

# test-helm.sh - Lint and template-test the Helm chart
#
# Usage:
#   ./hack/test-helm.sh
#   make test-helm

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
CHART_DIR="${ROOT_DIR}/helm/slack-qr-bot"

echo "==> Helm chart tests"
echo ""

# 1. Lint
echo "--- Lint ---"
helm lint "${CHART_DIR}"
echo ""

# 2. Template render (default values)
echo "--- Template (default values) ---"
helm template test-release "${CHART_DIR}" > /dev/null
echo "  [OK] Default values render successfully"
echo ""

# 3. Template render (with ingress)
echo "--- Template (ingress enabled) ---"
helm template test-release "${CHART_DIR}" \
    --set ingress.enabled=true \
    --set "ingress.hosts[0].host=test.example.com" \
    --set "ingress.hosts[0].paths[0].path=/" \
    --set "ingress.hosts[0].paths[0].pathType=Prefix" > /dev/null
echo "  [OK] Ingress values render successfully"
echo ""

# 4. Template render (TLS ingress)
echo "--- Template (TLS ingress) ---"
helm template test-release "${CHART_DIR}" \
    --set ingress.enabled=true \
    --set "ingress.hosts[0].host=test.example.com" \
    --set "ingress.hosts[0].paths[0].path=/" \
    --set "ingress.hosts[0].paths[0].pathType=Prefix" \
    --set "ingress.tls[0].secretName=tls-secret" \
    --set "ingress.tls[0].hosts[0]=test.example.com" > /dev/null
echo "  [OK] TLS ingress render successfully"
echo ""

# 5. Template render (custom secret names)
echo "--- Template (custom secret names) ---"
helm template test-release "${CHART_DIR}" \
    --set secrets.slackTokenSecretName=custom-slack-secret \
    --set secrets.apiKeySecretName=custom-api-secret > /dev/null
echo "  [OK] Custom secret names render successfully"
echo ""

# 6. Template render (rate limit + replicas)
echo "--- Template (rate limit + replicas) ---"
helm template test-release "${CHART_DIR}" \
    --set config.rateLimitEnabled=true \
    --set replicaCount=3 \
    --set service.type=NodePort \
    --set "extraEnv[0].name=CUSTOM" \
    --set "extraEnv[0].value=test" > /dev/null
echo "  [OK] Rate limit + replicas render successfully"
echo ""

# 7. Template render (all example files)
echo "--- Template (example values) ---"
for f in "${CHART_DIR}"/examples/*.yaml; do
    name=$(basename "$f" .yaml)
    helm template test-release "${CHART_DIR}" -f "$f" > /dev/null
    echo "  [OK] ${name}"
done
echo ""

TOTAL=$((6 + $(ls "${CHART_DIR}"/examples/*.yaml 2>/dev/null | wc -l | tr -d ' ')))
echo "==> All Helm chart tests passed! (${TOTAL} scenarios)"
