# Version Management & Release Process

<br/>

## Version Locations

Version is tracked in the following files:

| File | Field | Format |
|------|-------|--------|
| `Makefile` | `IMG` | `somaz940/slack-qr-bot:v0.2.0` |
| `helm/slack-qr-bot/Chart.yaml` | `version` | `0.2.0` (without `v`) |
| `helm/slack-qr-bot/Chart.yaml` | `appVersion` | `v0.2.0` |
| `helm/slack-qr-bot/values.yaml` | `image.tag` | `v0.2.0` |
| `deploy/deployment.yaml` | `image` | `somaz940/slack-qr-bot:v0.2.0` |
| `deploy/helmfile/helmfile.yaml` | `version` | `0.2.0` (without `v`) |
| `deploy/helmfile/values/mgmt.yaml` | `image.tag` | `v0.2.0` |

<br/>

## Check Current Version

```bash
make version
```

Output:
```
Current version: v0.2.0

Version in each file:
  Makefile:                           v0.2.0
  Chart.yaml (version):               0.2.0
  Chart.yaml (appVersion):            v0.2.0
  values.yaml (image.tag):            v0.2.0
  deployment.yaml (image):            v0.2.0
  helmfile.yaml (version):            0.2.0
  helmfile mgmt.yaml (image.tag):     v0.2.0
```

<br/>

## Bump Version

Update all files at once:

```bash
make bump-version VERSION=v0.3.0
```

This updates:
- `Makefile` IMG tag
- `Chart.yaml` version + appVersion
- `values.yaml` image.tag
- `deploy/deployment.yaml` image tag
- `deploy/helmfile/helmfile.yaml` version
- `deploy/helmfile/values/mgmt.yaml` image.tag
- `README.md` version references

<br/>

## Release Process

### 1. Bump version and commit

```bash
make bump-version VERSION=v0.3.0
git diff                                    # review changes
git commit -am "chore: bump version to v0.3.0"
git push origin main
```

### 2. Build and push Docker image

```bash
make docker-buildx                          # builds + pushes versioned + latest tags
```

### 3. Create git tag

```bash
git tag v0.3.0
git push origin v0.3.0
```

This triggers the following CI workflows:
- **release.yml**: Docker multi-arch build+push → GitHub Release with changelog
- **helm-release.yml**: Package Helm chart → publish to gh-pages

### 4. Verify

```bash
# Docker image
docker pull somaz940/slack-qr-bot:v0.3.0

# Helm chart
helm repo update
helm search repo slack-qr-bot
```

<br/>

## Development Workflow

### Feature branch

```bash
make branch name=custom-qr-colors          # creates feat/custom-qr-colors
# ... develop ...
make pr title="Add custom QR colors"       # test + lint + push + create PR
```

### Pre-flight checks

```bash
make test                                   # all tests pass
make lint                                   # flake8 lint
make test-helm                              # Helm chart lint + render
make version                                # versions consistent
```
