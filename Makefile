APP_NAME := slack-qr-bot
IMG ?= somaz940/slack-qr-bot:latest
CONTAINER_TOOL ?= docker
PLATFORMS ?= linux/arm64,linux/amd64

VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

.PHONY: all run test clean help venv docker-build docker-push docker-buildx deploy logs

all: venv lint

## Virtual Environment
venv: $(VENV)/bin/activate

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate

## Run
run: venv
	$(PYTHON) -m src.app

run-gunicorn: venv
	$(VENV)/bin/gunicorn --bind 0.0.0.0:8080 --workers 2 --timeout 60 src.app:app

## Test
test: venv
	$(PIP) install pytest pytest-cov 2>/dev/null
	$(VENV)/bin/pytest tests/ -v --cov=src --cov-report=term-missing

coverage: venv
	$(PIP) install pytest pytest-cov 2>/dev/null
	$(VENV)/bin/pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
	@echo "Open htmlcov/index.html in your browser"

## Code Quality
lint: venv
	$(PIP) install flake8 2>/dev/null
	$(VENV)/bin/flake8 src/ --max-line-length=120

## Docker
docker-build:
	$(CONTAINER_TOOL) build -t ${IMG} .

docker-push:
	$(CONTAINER_TOOL) push ${IMG}

docker-buildx-tag:
	- $(CONTAINER_TOOL) buildx create --name $(APP_NAME)-builder
	$(CONTAINER_TOOL) buildx use $(APP_NAME)-builder
	- $(CONTAINER_TOOL) buildx build --push --platform=$(PLATFORMS) \
		--tag ${IMG} \
		-f Dockerfile .
	- $(CONTAINER_TOOL) buildx rm $(APP_NAME)-builder

docker-buildx-latest:
	- $(CONTAINER_TOOL) buildx create --name $(APP_NAME)-builder
	$(CONTAINER_TOOL) buildx use $(APP_NAME)-builder
	- $(CONTAINER_TOOL) buildx build --push --platform=$(PLATFORMS) \
		--tag $(shell echo ${IMG} | cut -f1 -d:):latest \
		-f Dockerfile .
	- $(CONTAINER_TOOL) buildx rm $(APP_NAME)-builder

docker-buildx: docker-buildx-tag docker-buildx-latest

## K8s Deploy
deploy:
	kubectl apply -f k8s/

restart:
	kubectl rollout restart deployment/$(APP_NAME)

logs:
	kubectl logs -l app=$(APP_NAME) -f

## Cleanup
clean:
	rm -rf $(VENV) .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

## Help
help:
	@echo "Usage:"
	@echo "  make venv                - Create virtualenv and install dependencies"
	@echo "  make run                 - Run app locally (Flask dev server)"
	@echo "  make run-gunicorn        - Run app locally (Gunicorn)"
	@echo "  make test                - Run tests with coverage"
	@echo "  make coverage            - Generate HTML coverage report"
	@echo "  make lint                - Run flake8 linter"
	@echo "  make docker-build        - Build Docker image"
	@echo "  make docker-push         - Push Docker image"
	@echo "  make docker-buildx-tag   - Build and push multi-arch image (version tag)"
	@echo "  make docker-buildx-latest - Build and push multi-arch image (latest tag)"
	@echo "  make docker-buildx       - Build and push multi-arch image (both tags)"
	@echo "  make deploy              - Deploy to Kubernetes"
	@echo "  make restart             - Restart deployment"
	@echo "  make logs                - Tail pod logs"
	@echo "  make clean               - Remove venv and cache files"
