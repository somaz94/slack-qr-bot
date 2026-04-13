# Image URL to use all building/pushing image targets
IMG ?= somaz940/slack-qr-bot:v0.2.0
APP_NAME := slack-qr-bot

GIT_COMMIT := $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_DATE := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")

# Docker build args
DOCKER_BUILD_ARGS = \
	--build-arg VERSION=$(shell echo ${IMG} | cut -d: -f2) \
	--build-arg GIT_COMMIT=$(GIT_COMMIT) \
	--build-arg BUILD_DATE=$(BUILD_DATE)

# Container tool (docker or podman)
CONTAINER_TOOL ?= docker

# Platforms for multi-arch builds
PLATFORMS ?= linux/amd64,linux/arm64

# Python
VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

# Deploy
DEPLOY_NAME ?= $(APP_NAME)
DEPLOY_PORT ?= 8080
K8S_NAMESPACE ?= slack-bots

# Setting SHELL to bash allows bash commands to be executed by recipes.
SHELL = /usr/bin/env bash -o pipefail
.SHELLFLAGS = -ec

.PHONY: all
all: venv lint

##@ General

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

##@ Development

.PHONY: venv
venv: $(VENV)/bin/activate ## Create virtualenv and install dependencies

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate

.PHONY: run
run: venv ## Run app locally (Flask dev server)
	$(PYTHON) -m src.app

.PHONY: run-gunicorn
run-gunicorn: venv ## Run app locally (Gunicorn)
	$(VENV)/bin/gunicorn --bind 0.0.0.0:$(DEPLOY_PORT) --workers 2 --timeout 60 src.app:app

##@ Linting

.PHONY: lint
lint: venv ## Run flake8 linter
	$(PIP) install flake8 2>/dev/null
	$(VENV)/bin/flake8 src/ --max-line-length=120

##@ Testing

.PHONY: test
test: venv ## Run tests with coverage
	$(PIP) install pytest pytest-cov 2>/dev/null
	$(VENV)/bin/pytest tests/ -v --cov=src --cov-report=term-missing

.PHONY: coverage
coverage: venv ## Generate HTML coverage report
	$(PIP) install pytest pytest-cov 2>/dev/null
	$(VENV)/bin/pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

.PHONY: test-helm
test-helm: ## Run Helm chart tests (lint, template render)
	@bash hack/test-helm.sh

##@ Docker

.PHONY: docker-build
docker-build: ## Build docker image
	$(CONTAINER_TOOL) build $(DOCKER_BUILD_ARGS) -t ${IMG} .

.PHONY: docker-push
docker-push: ## Push docker image
	$(CONTAINER_TOOL) push ${IMG}

.PHONY: docker-buildx-tag
docker-buildx-tag: ## Build and push multi-arch image with version tag
	sed -e '1 s/\(^FROM\)/FROM --platform=\$$\{BUILDPLATFORM\}/; t' -e ' 1,// s//FROM --platform=\$$\{BUILDPLATFORM\}/' Dockerfile > Dockerfile.cross
	- $(CONTAINER_TOOL) buildx create --name $(APP_NAME)-builder
	$(CONTAINER_TOOL) buildx use $(APP_NAME)-builder
	- $(CONTAINER_TOOL) buildx build --push --platform=$(PLATFORMS) \
		$(DOCKER_BUILD_ARGS) \
		--tag ${IMG} \
		-f Dockerfile.cross .
	- $(CONTAINER_TOOL) buildx rm $(APP_NAME)-builder
	rm Dockerfile.cross

.PHONY: docker-buildx-latest
docker-buildx-latest: ## Build and push multi-arch image with latest tag
	sed -e '1 s/\(^FROM\)/FROM --platform=\$$\{BUILDPLATFORM\}/; t' -e ' 1,// s//FROM --platform=\$$\{BUILDPLATFORM\}/' Dockerfile > Dockerfile.cross
	- $(CONTAINER_TOOL) buildx create --name $(APP_NAME)-builder
	$(CONTAINER_TOOL) buildx use $(APP_NAME)-builder
	- $(CONTAINER_TOOL) buildx build --push --platform=$(PLATFORMS) \
		$(DOCKER_BUILD_ARGS) \
		--tag $(shell echo ${IMG} | cut -f1 -d:):latest \
		-f Dockerfile.cross .
	- $(CONTAINER_TOOL) buildx rm $(APP_NAME)-builder
	rm Dockerfile.cross

.PHONY: docker-buildx
docker-buildx: ## Build and push both version and latest tags
docker-buildx: docker-buildx-tag docker-buildx-latest

##@ Version

.PHONY: version
version: ## Show current version across all files
	@./hack/bump-version.sh --current

VERSION ?=
.PHONY: bump-version
bump-version: ## Bump version across all files. Usage: make bump-version VERSION=v0.3.0
	@if [ -z "$(VERSION)" ]; then echo "Usage: make bump-version VERSION=vX.Y.Z"; exit 1; fi
	@./hack/bump-version.sh $(VERSION)

##@ Workflow

.PHONY: check-gh
check-gh: ## Check if gh CLI is installed and authenticated
	@command -v gh >/dev/null 2>&1 || { echo "\033[31m✗ gh CLI not installed. Run: brew install gh\033[0m"; exit 1; }
	@gh auth status >/dev/null 2>&1 || { echo "\033[31m✗ gh CLI not authenticated. Run: gh auth login\033[0m"; exit 1; }
	@echo "\033[32m✓ gh CLI ready\033[0m"

.PHONY: branch
branch: ## Create feature branch (usage: make branch name=feature-name)
	@if [ -z "$(name)" ]; then echo "Usage: make branch name=<feature-name>"; exit 1; fi
	git checkout main
	git pull origin main
	git checkout -b feat/$(name)
	@echo "\033[32m✓ Branch feat/$(name) created\033[0m"

.PHONY: pr
pr: check-gh ## Run tests, push, and create PR (usage: make pr title="Add feature")
	@if [ -z "$(title)" ]; then echo "Usage: make pr title=\"PR title\""; exit 1; fi
	$(VENV)/bin/pytest tests/ -v --cov=src
	$(VENV)/bin/flake8 src/ --max-line-length=120
	git push -u origin $$(git branch --show-current)
	@./scripts/create-pr.sh "$(title)"
	@echo "\033[32m✓ PR created\033[0m"

##@ Deploy

.PHONY: deploy-docker
deploy-docker: ## Deploy as Docker container (pulls image if not local)
	@if ! $(CONTAINER_TOOL) image inspect ${IMG} >/dev/null 2>&1; then \
		echo "\033[33m⚠ Image ${IMG} not found locally. Pulling from registry...\033[0m"; \
		$(CONTAINER_TOOL) pull ${IMG} || { echo "\033[31m✗ Pull failed. Run 'make docker-build' to build locally.\033[0m"; exit 1; }; \
	fi
	@echo "Stopping existing container (if any)..."
	-@$(CONTAINER_TOOL) rm -f $(DEPLOY_NAME) 2>/dev/null
	@echo "Starting $(DEPLOY_NAME) on port $(DEPLOY_PORT)..."
	$(CONTAINER_TOOL) run -d \
		--name $(DEPLOY_NAME) \
		-p $(DEPLOY_PORT):8080 \
		-e SLACK_BOT_TOKEN=$${SLACK_BOT_TOKEN:-dummy} \
		-e RATE_LIMIT_ENABLED=false \
		${IMG}
	@echo "Container $(DEPLOY_NAME) running at http://localhost:$(DEPLOY_PORT)"

.PHONY: undeploy-docker
undeploy-docker: ## Stop and remove Docker container
	@echo "Stopping $(DEPLOY_NAME)..."
	-$(CONTAINER_TOOL) rm -f $(DEPLOY_NAME) 2>/dev/null
	@echo "Container $(DEPLOY_NAME) removed."

.PHONY: deploy-smoke
deploy-smoke: ## Smoke test against running server
	@bash hack/test-deploy.sh $(DEPLOY_PORT)

.PHONY: deploy-all
deploy-all: docker-build deploy-docker deploy-smoke ## Build + deploy + smoke test (all-in-one)

.PHONY: deploy-k8s
deploy-k8s: ## Deploy to Kubernetes cluster
	@echo "Deploying to namespace $(K8S_NAMESPACE)..."
	kubectl apply -f deploy/deployment.yaml -n $(K8S_NAMESPACE)
	kubectl rollout status deployment/$(DEPLOY_NAME) -n $(K8S_NAMESPACE) --timeout=60s
	@echo "Deployed. Service: kubectl get svc $(DEPLOY_NAME) -n $(K8S_NAMESPACE)"

.PHONY: undeploy-k8s
undeploy-k8s: ## Remove from Kubernetes cluster
	@echo "Removing from namespace $(K8S_NAMESPACE)..."
	kubectl delete -f deploy/deployment.yaml -n $(K8S_NAMESPACE) --ignore-not-found
	@echo "Removed."

.PHONY: restart
restart: ## Restart Kubernetes deployment
	kubectl rollout restart deployment/$(APP_NAME) -n $(K8S_NAMESPACE)

.PHONY: logs
logs: ## Tail Kubernetes pod logs
	kubectl logs -l app=$(APP_NAME) -f -n $(K8S_NAMESPACE)

##@ Cleanup

.PHONY: clean
clean: ## Remove build artifacts and caches
	rm -rf $(VENV) .pytest_cache .coverage htmlcov Dockerfile.cross
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
