# Testing Guide

<br/>

## Quick Start

```bash
make test           # Run all tests with coverage
make lint           # Run flake8 linter
make test-helm      # Helm chart lint + template render tests
```

<br/>

## Unit Tests

Run tests with pytest and coverage reporting:

```bash
make test
```

This runs:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

Test files:

| File | Description |
|------|-------------|
| `tests/conftest.py` | Pytest fixtures and configuration |
| `tests/test_config.py` | Configuration loading and validation |
| `tests/test_decorators.py` | API key authentication decorator |
| `tests/test_services.py` | Core QR/Slack service layer |
| `tests/test_routes_health.py` | Health check endpoint |
| `tests/test_routes_channels.py` | Channel listing endpoint |
| `tests/test_routes_qr.py` | QR code generation endpoints |
| `tests/test_routes_slack_events.py` | Slack event handler |
| `tests/test_utils.py` | Response utility functions |

<br/>

## Coverage Report

Generate an HTML coverage report:

```bash
make coverage
open htmlcov/index.html
```

<br/>

## Linting

Run flake8 with 120 character line length limit:

```bash
make lint
```

<br/>

## Helm Chart Tests

Lint and template render verification:

```bash
make test-helm
```

8 scenarios tested:

| Scenario | Description |
|----------|-------------|
| Lint | Chart structure and syntax validation |
| Default values | Renders with no overrides |
| Ingress enabled | Ingress resource created correctly |
| TLS ingress | Ingress with TLS configuration |
| Custom secret names | Custom Slack/API key secret references |
| Rate limit + replicas | Multiple replicas with rate limiting enabled |
| Example: ingress-tls | cert-manager TLS example |
| Example: production | Production-ready configuration |

<br/>

## Smoke Tests

After deploying to Docker, verify the server is working correctly:

```bash
# Deploy as Docker container
make deploy-docker

# Run smoke tests (6 checks)
make deploy-smoke

# Stop container
make undeploy-docker
```

Smoke test checks:

| Check | Description |
|-------|-------------|
| Health endpoint | `GET /health` returns 200 |
| JSON response | Health response is valid JSON |
| QR endpoint | `POST /generate-qr` responds |
| Channels endpoint | `GET /channels` responds |
| Swagger docs | `GET /apidocs/` returns 200 |
| Unknown route | `GET /unknown` returns 404 |

<br/>

## Running Specific Tests

```bash
# Run a specific test file
pytest tests/test_routes_qr.py -v

# Run a specific test by name
pytest tests/ -k "test_health" -v

# Run with verbose output and coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run only failing tests
pytest tests/ --lf -v
```
