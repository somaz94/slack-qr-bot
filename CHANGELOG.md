# Changelog

All notable changes to this project will be documented in this file.

## Unreleased (2026-07-27)

### Features

- **ci:** publish Helm chart to GHCR (OCI) alongside gh-pages ([cf1ee33](https://github.com/somaz94/slack-qr-bot/commit/cf1ee3385cfffd8281a80e2272942d1e0512ed76))

### Bug Fixes

- warn when bump-version.sh finds no version to replace ([6df5d72](https://github.com/somaz94/slack-qr-bot/commit/6df5d720bfbc8a22a794b275a6b557dcf0c8cc1a))
- **ci:** use staged tarball for OCI push (gh-pages branch checkout invalidates ./helm/ path) ([ef1ad65](https://github.com/somaz94/slack-qr-bot/commit/ef1ad651370e1953f5be36533cbe3ba05cf07016))

### Continuous Integration

- adopt semantic-pr, labels, lock-threads, PR size, and auto-assign reusables ([546bc1c](https://github.com/somaz94/slack-qr-bot/commit/546bc1c8b4f9aa6bf591cefe7de082d03451538e))
- use reusable stale-issues workflow ([7edc4c3](https://github.com/somaz94/slack-qr-bot/commit/7edc4c3a9ef043efeba3d0a34e251354b589a79c))
- use reusable issue-greeting workflow ([68f8d7b](https://github.com/somaz94/slack-qr-bot/commit/68f8d7b9e2a8812f302a502f0becb0ad0157f9c0))
- use reusable dependabot-auto-merge workflow ([1ec6bb8](https://github.com/somaz94/slack-qr-bot/commit/1ec6bb8e098c83fa599ade82097bf12e1cca3403))
- use reusable contributors workflow ([cb87bc7](https://github.com/somaz94/slack-qr-bot/commit/cb87bc7136783d86bb917db3d5340c70177c077d))
- add ok-to-test workflow stub ([4f67993](https://github.com/somaz94/slack-qr-bot/commit/4f679936f8527d0f1edcdd6b3d424e46d4cb0487))
- add PR welcome workflow stub ([a30a618](https://github.com/somaz94/slack-qr-bot/commit/a30a618d878dae5677ae2d23616157fb577d4caa))
- add concurrency guards to recurring workflows ([f993c42](https://github.com/somaz94/slack-qr-bot/commit/f993c42d55f1b1aae24aa8588bb1dbcdcfe3fbd0))
- use helm-chart-release-action@v1 (replace inline release script) ([9d685b8](https://github.com/somaz94/slack-qr-bot/commit/9d685b89a652c74d9d646eee2de50510a4ac412d))

### Chores

- **deps:** bump actions/setup-python from 6 to 7 (#20) ([#20](https://github.com/somaz94/slack-qr-bot/pull/20)) ([dbe7273](https://github.com/somaz94/slack-qr-bot/commit/dbe7273b1b20e8f3544013f3f3338d5685fa148a))
- **deps:** update pillow requirement from >=12.2.0 to >=12.3.0 (#19) ([#19](https://github.com/somaz94/slack-qr-bot/pull/19)) ([8ef810a](https://github.com/somaz94/slack-qr-bot/commit/8ef810aa6883879c38d520a48f0b6abd6db3ffd7))
- **deps:** bump slack-sdk from 3.42.0 to 3.43.0 in the pip-minor group (#18) ([#18](https://github.com/somaz94/slack-qr-bot/pull/18)) ([5aed158](https://github.com/somaz94/slack-qr-bot/commit/5aed1588e7cd38888efb2f1692258abca31f4efd))
- **deps:** bump gunicorn from 25.3.0 to 26.0.0 (#15) ([#15](https://github.com/somaz94/slack-qr-bot/pull/15)) ([510d93b](https://github.com/somaz94/slack-qr-bot/commit/510d93b2e532f7659a7a0516cc6c4f81b4ef27dc))
- **deps:** bump actions/checkout from 6 to 7 (#17) ([#17](https://github.com/somaz94/slack-qr-bot/pull/17)) ([58c54dd](https://github.com/somaz94/slack-qr-bot/commit/58c54ddeeefa07b46b6f42c42c92d17e85a579b3))
- **deps:** bump slack-sdk from 3.41.0 to 3.42.0 in the pip-minor group (#16) ([#16](https://github.com/somaz94/slack-qr-bot/pull/16)) ([7bd67d0](https://github.com/somaz94/slack-qr-bot/commit/7bd67d0d9264eaa7445ba3c43baf1d262b1e24a8))
- **deps:** update pillow requirement from >=10.4.0 to >=12.2.0 (#14) ([#14](https://github.com/somaz94/slack-qr-bot/pull/14)) ([a4b857d](https://github.com/somaz94/slack-qr-bot/commit/a4b857d63749c99128b7d52f2ee29c7c2bbbfad3))
- **deps:** bump docker/login-action from 3 to 4 (#13) ([#13](https://github.com/somaz94/slack-qr-bot/pull/13)) ([8daace1](https://github.com/somaz94/slack-qr-bot/commit/8daace195756d36e10b5383d9b024c293b7ccd5c))
- **deps:** bump docker/setup-qemu-action from 3 to 4 (#12) ([#12](https://github.com/somaz94/slack-qr-bot/pull/12)) ([b55b1c2](https://github.com/somaz94/slack-qr-bot/commit/b55b1c21c4c204623a7ab2a47e478c941a7390c3))

### Contributors

- somaz

<br/>

## [v0.3.0](https://github.com/somaz94/slack-qr-bot/compare/v0.2.0...v0.3.0) (2026-04-13)

### Features

- add deploy-all target for one-step build, deploy, and smoke test ([7bb968d](https://github.com/somaz94/slack-qr-bot/commit/7bb968d22d6e50d54b10e0ab4c73da422efbb9d8))
- add CODEOWNERS ([9694a08](https://github.com/somaz94/slack-qr-bot/commit/9694a08dc02fc44030e9b4b978e171ad3fa51fcb))

### Bug Fixes

- resolve flake8 lint errors in app.py ([7667e4c](https://github.com/somaz94/slack-qr-bot/commit/7667e4c6b4011a510eb3832d13b0e32d613d15a1))
- correct swagger endpoint path in smoke test ([7e6c369](https://github.com/somaz94/slack-qr-bot/commit/7e6c369dabce1f8f5f025666dfbe8232a3f9bbba))
- use GITHUB_TOKEN for dependabot auto merge ([a2ddb39](https://github.com/somaz94/slack-qr-bot/commit/a2ddb39ee22cb1d3cd5d20baff35e2eeafbe9ac4))

### Code Refactoring

- restructure project to match static-file-server patterns ([0d8b2d2](https://github.com/somaz94/slack-qr-bot/commit/0d8b2d2151f6461a743912163ab62b193ee8d4dc))
- sync functional logic with gitlab-project version ([c237a48](https://github.com/somaz94/slack-qr-bot/commit/c237a4840172d1d9ad5bc930522bfdc0aa9e6919))

### Documentation

- add lint workflow, Helm README, test and version guides ([99f8db6](https://github.com/somaz94/slack-qr-bot/commit/99f8db6cb358a680ad5b5653595674b67320a65c))
- remove duplicate rules covered by global CLAUDE.md ([d9c0c93](https://github.com/somaz94/slack-qr-bot/commit/d9c0c93a2a8aecbd10a207b7adb44ba4b8dc85b7))
- add no-push rule to CLAUDE.md ([452c2e6](https://github.com/somaz94/slack-qr-bot/commit/452c2e67f8f2b2ecba08564b627e320c933cfae5))
- update CLAUDE.md with commit guidelines and language ([e770212](https://github.com/somaz94/slack-qr-bot/commit/e7702125bc74531cd98dadf28a1fe1f29d3d73e8))

### Continuous Integration

- add Docker build and push job to release workflow ([2e29823](https://github.com/somaz94/slack-qr-bot/commit/2e2982359d7e303d598c7899bfc6aacea5472037))
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

- bump version to v0.3.0 ([d8a45a7](https://github.com/somaz94/slack-qr-bot/commit/d8a45a774893d6683d74f33220ceda9443f08c90))
- **deps:** bump dependabot/fetch-metadata from 2 to 3 (#11) ([#11](https://github.com/somaz94/slack-qr-bot/pull/11)) ([4c1197a](https://github.com/somaz94/slack-qr-bot/commit/4c1197a38eb278561b886ec65511fef7d11409dd))
- **deps:** bump actions/github-script from 8 to 9 (#10) ([#10](https://github.com/somaz94/slack-qr-bot/pull/10)) ([1ab6ae7](https://github.com/somaz94/slack-qr-bot/commit/1ab6ae7072409af0319a5c4bb3c3052c030a5d3a))
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

