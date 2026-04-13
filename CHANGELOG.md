# Changelog

All notable changes to this project will be documented in this file.

## Unreleased (2026-04-13)

### Features

- add CODEOWNERS ([9694a08](https://github.com/somaz94/slack-qr-bot/commit/9694a08dc02fc44030e9b4b978e171ad3fa51fcb))

### Bug Fixes

- use GITHUB_TOKEN for dependabot auto merge ([a2ddb39](https://github.com/somaz94/slack-qr-bot/commit/a2ddb39ee22cb1d3cd5d20baff35e2eeafbe9ac4))

### Documentation

- remove duplicate rules covered by global CLAUDE.md ([d9c0c93](https://github.com/somaz94/slack-qr-bot/commit/d9c0c93a2a8aecbd10a207b7adb44ba4b8dc85b7))
- add no-push rule to CLAUDE.md ([452c2e6](https://github.com/somaz94/slack-qr-bot/commit/452c2e67f8f2b2ecba08564b627e320c933cfae5))
- update CLAUDE.md with commit guidelines and language ([e770212](https://github.com/somaz94/slack-qr-bot/commit/e7702125bc74531cd98dadf28a1fe1f29d3d73e8))

### Continuous Integration

- skip auto-generated changelog and contributors commits in release notes ([b52d635](https://github.com/somaz94/slack-qr-bot/commit/b52d6354aa815e261ea8cf6a943c81012b996f92))
- revert to body_path RELEASE.md in release workflow ([7aea35d](https://github.com/somaz94/slack-qr-bot/commit/7aea35dada20e67f7eda59b6f87b50bb2a920e35))
- use generate_release_notes instead of RELEASE.md ([1fca892](https://github.com/somaz94/slack-qr-bot/commit/1fca892bc60ba59aa8a0c2d19dc515859f8af29c))
- add PR workflow and limit push trigger to main ([f679175](https://github.com/somaz94/slack-qr-bot/commit/f679175291abd4ccae5633f0238f1b93e146a2c5))
- migrate gitlab-mirror workflow to multi-git-mirror action ([31388cd](https://github.com/somaz94/slack-qr-bot/commit/31388cd711e244906c0b7f766ab62a00d5debf82))
- use somaz94/contributors-action@v1 for contributors generation ([aef8008](https://github.com/somaz94/slack-qr-bot/commit/aef8008d6a150f11764b8bc98eb1c6c4fc574874))
- use major-tag-action for version tag updates ([063124f](https://github.com/somaz94/slack-qr-bot/commit/063124f1d121f8ae4a164049df29be26d5737021))
- migrate changelog generator to go-changelog-action ([ae171b7](https://github.com/somaz94/slack-qr-bot/commit/ae171b78ac59272e650df30adc4ad819705bb45a))
- add GitHub release notes configuration ([9864685](https://github.com/somaz94/slack-qr-bot/commit/9864685c9e411786be61aed81a45a90627b044c7))
- unify changelog-generator with flexible tag pattern ([b32c2c8](https://github.com/somaz94/slack-qr-bot/commit/b32c2c8269d43c3bbeb2377cda830ca995b7ef28))

### Chores

- **deps:** bump python-json-logger from 2.0.7 to 4.1.0 (#9) ([#9](https://github.com/somaz94/slack-qr-bot/pull/9)) ([2a84d84](https://github.com/somaz94/slack-qr-bot/commit/2a84d84156d6484c4699965d30d4c086d41bf4ca))
- **deps:** bump gunicorn from 25.1.0 to 25.3.0 in the pip-minor group (#8) ([#8](https://github.com/somaz94/slack-qr-bot/pull/8)) ([0169360](https://github.com/somaz94/slack-qr-bot/commit/016936089c4dd357d981f54d0388c978da1830ce))
- remove duplicate rules from CLAUDE.md (moved to global) ([e4b12fd](https://github.com/somaz94/slack-qr-bot/commit/e4b12fd63f6b63a0e4a80bfb6d7a2f31c2080360))
- add git config protection to CLAUDE.md ([68cc735](https://github.com/somaz94/slack-qr-bot/commit/68cc7352caad54ebf6479d2d948701f8ad930975))

### Contributors

- somaz

<br/>

## [v0.2.0](https://github.com/somaz94/slack-qr-bot/compare/v0.1.0...v0.2.0) (2026-03-13)

### Documentation

- add API reference, deployment guide, and translate Korean to English ([cc4990a](https://github.com/somaz94/slack-qr-bot/commit/cc4990a14fa971096f66e52532eb63f868a83d54))

### Contributors

- somaz

<br/>

## [v0.1.0](https://github.com/somaz94/slack-qr-bot/releases/tag/v0.1.0) (2026-03-13)

### Documentation

- CLAUDE.md ([15b8742](https://github.com/somaz94/slack-qr-bot/commit/15b87428551991abe509badabfb37369c88574f4))
- README.md ([15287ac](https://github.com/somaz94/slack-qr-bot/commit/15287acdd1f22689c3c209d00405e480c6466e25))
- README.md ([6db56dc](https://github.com/somaz94/slack-qr-bot/commit/6db56dc4dbb3f53e463ac2e8d6b8da6292ca96de))
- README.md ([ffde501](https://github.com/somaz94/slack-qr-bot/commit/ffde501f67d1556c20f3648ef77c1bb5dd67a290))

### Continuous Integration

- add workflows, tests, Makefile, and project tooling ([29fe239](https://github.com/somaz94/slack-qr-bot/commit/29fe239899abce1fd9111bd4bdabaab1b02e6ad3))

### Chores

- **deps:** bump qrcode[pil] from 7.4.2 to 8.2 (#6) ([#6](https://github.com/somaz94/slack-qr-bot/pull/6)) ([0685764](https://github.com/somaz94/slack-qr-bot/commit/068576490c13128fdf41ba06992005656bced3f6))
- **deps:** bump tenacity from 8.2.3 to 9.1.4 (#5) ([#5](https://github.com/somaz94/slack-qr-bot/pull/5)) ([edc9c4c](https://github.com/somaz94/slack-qr-bot/commit/edc9c4c313b5fa0a35d8336c3d7ec21a7cf42290))
- **deps:** bump gunicorn from 21.2.0 to 25.1.0 (#4) ([#4](https://github.com/somaz94/slack-qr-bot/pull/4)) ([a949c50](https://github.com/somaz94/slack-qr-bot/commit/a949c509e8f4eb4e052ff3b0c4fdf9139e361800))
- **deps:** bump flask-limiter from 3.5.0 to 4.1.1 (#3) ([#3](https://github.com/somaz94/slack-qr-bot/pull/3)) ([7ec0cba](https://github.com/somaz94/slack-qr-bot/commit/7ec0cbaa3f2bbad96b1ef2815f0fd1a2978e83c7))
- **deps:** bump the pip-minor group with 2 updates (#2) ([#2](https://github.com/somaz94/slack-qr-bot/pull/2)) ([990cc00](https://github.com/somaz94/slack-qr-bot/commit/990cc00eb551f76cc780eec10c85211a4327c266))
- **deps:** bump actions/setup-python from 5 to 6 (#1) ([#1](https://github.com/somaz94/slack-qr-bot/pull/1)) ([9957d4c](https://github.com/somaz94/slack-qr-bot/commit/9957d4c77da834412b0ad6399e9c5d10333d5869))
- change license from MIT to Apache 2.0 ([dbf73ec](https://github.com/somaz94/slack-qr-bot/commit/dbf73ecc08c71cec4891be3282f301d79a5966ac))
- gitlab-mirror.yml ([bacea51](https://github.com/somaz94/slack-qr-bot/commit/bacea51d891b700da011c942c264c4b1c18d9594))

### Contributors

- somaz

<br/>

