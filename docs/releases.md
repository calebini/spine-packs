# Installer releases on GitHub

The initial distribution channel is GitHub Releases in `calebini/spine-packs`,
not PyPI. The operator approved installer version `0.1.0`, MIT licensing, and
tag `installer-v0.1.0`. The numeric version does not widen the support promises
below. It is not `kinflow-starter.v1` or a change to any artifact contract.
Tag publication and GitHub release-asset publication are distinct actions;
the current authorization covers the tag, not uploading the release assets.

The package uses standard `pyproject.toml` metadata and the `spine-packs`
console entrypoint. Hatchling bundles authoritative `contracts/schemas/` bytes
as `spine_packs/_schemas/`; there is no manually maintained second schema copy.
See [PyPA metadata guidance](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
and [Hatch build configuration](https://hatch.pypa.io/latest/config/build/).

## What is distributed

Each approved installer release has three explicitly named assets:

- `spine_packs-<version>-py3-none-any.whl`: CLI, eleven validation schemas, and MIT license;
- `spine_packs-<version>.tar.gz`: rebuildable source, schemas, orientation/release
  docs, and the small disposable-integration harness and its synthetic input;
- `SHA256SUMS`: SHA-256 of those exact two files.

Both distributions carry the root `LICENSE`; package metadata declares MIT.
The wheel has no third-party runtime dependencies. Neither distribution
includes Spine, Tickerd, curated packs, operator artifacts, local ledgers,
credentials, audit payloads, or Whetstone run evidence. The sdist's reviewed
format fixture is test input only, not a curated release. Full development
tests and normative specs remain in the tagged repository.

The installer requires Python 3.11+ and local POSIX filesystem behavior. The
`any` wheel tag means pure Python, not qualified Windows or remote-filesystem
support. Qualification tooling and the external Spine baseline need Python
3.12+. A compatible Spine 0.3.0 CLI is provisioned separately; the package
does not install, deploy, upgrade, or configure Spine. Packs are separately
selected inputs; shipping an installer does not make the current drafts
apply-eligible.

## Build and qualify without publishing

Run these development commands from the repository checkout; the sdist is a
rebuild/integration input, not a complete development checkout.
First provision isolated public Spine CLIs as described in
[local-qualification.md](local-qualification.md). Use an isolated build venv;
do not install build dependencies into a shared environment:

```sh
BUILD_ROOT=$(mktemp -d /private/tmp/spine-packs-build.XXXXXX)
python3 -m venv "$BUILD_ROOT/venv"
"$BUILD_ROOT/venv/bin/python" -m pip install 'build>=1.2,<2' 'hatchling>=1.27,<2'
"$BUILD_ROOT/venv/bin/python" scripts/qualify_package.py \
  --spine-command "$QUAL_ROOT/venv/bin/spine-command" \
  --spine-ledger-migrate "$QUAL_ROOT/venv/bin/spine-ledger-migrate"
```

`QUAL_ROOT` is the isolated setup root from that document. Build tools may need
network access; qualification itself builds without dependency downloads and
installs the local wheel with `--no-index --no-deps`. The script creates a new
private evidence directory and never accepts an existing ledger. It:

1. builds the wheel from the sdist and compares it byte-for-byte with a direct
   wheel build under the same recorded tooling and fixed source timestamp;
2. checks exact archive membership and byte identity of runtime/schema sources;
3. installs into a fresh venv outside the checkout, tests the console and module
   entrypoints, and checks dependency consistency;
4. runs all four disposable-ledger scenarios from the extracted sdist with
   isolated imports, including six real-command uncertain-response recoveries;
5. records the installed module/schema paths and emits checksums only on success.

The harness rejects source-tree module/schema loading in installed mode.
Normal installed operations invoke the console script in new processes; only
fault injection uses the installed module in-process. All evidence, including
failed builds, stays local. Nothing uploads, tags, commits, or pushes.

Initial local package qualification passed on 2026-09-18 with Python 3.14.6,
build 1.6.1 and Hatchling 1.32.3 on macOS. Direct and sdist-built wheels were
byte-identical; all four installed integration tests passed, including all six
uncertain-response recoveries. Repository checks, 55 contract tests and 109
runtime tests passed. This is candidate evidence, not an all-platform/Python
version matrix or qualification of the eventual clean release commit.

## Review closeout and publication gate

The clean committed candidate `8f7e967` passed the same qualification checks.
The 22-file Slice 6 bounded review on 2026-09-18 returned `pass`, preserved
boundaries, and zero findings; see `specs/implementation-plan.md` in the source
repository. The subsequent `0.1.0`/MIT closeout changes release metadata and
license checks only, not installer runtime behavior or pack contracts.

Before publishing the approved tag, commit the version/license closeout and run
repository, contract, runtime, and package qualification checks from a clean
checkout of that exact commit. Verify that both archives carry the correct
version and license. Do not tag an unqualified commit or move an existing tag.

Before creating a GitHub Release, record the Python/platform and build-tool
versions, tested Spine/Tickerd commits, limitations, and checksum results in
release notes, and obtain explicit approval to publish the exact three assets.
That step is separate from the approved tag and has not run yet.
The GitHub prerelease marker is independent of the numeric version and can be
chosen when publishing; a numeric version alone asserts no broader maturity.

Attach only the three qualified assets to the authorized GitHub Release.
Use GitHub's release UI or `gh release create`; do not use a wildcard that could
upload logs, manifests, or operator evidence. Publish the qualified wheel, not
a new untested rebuild. Do not move a published tag or replace published asset
bytes; fixes require another installer version. This is release policy, not a
claim that GitHub immutability settings have been configured.

Checksums detect accidental byte changes; they are not signatures or an
independent publisher-trust mechanism. Signing and automatic release workflows
remain separate decisions. No PyPI credentials or publication are needed.

## Operator installation after publication

Download the wheel and `SHA256SUMS` from the approved GitHub release, verify
the wheel's SHA-256 against its named entry, then install the local wheel in
an isolated tool environment, for example:

```sh
pipx install ./spine_packs-0.1.0-py3-none-any.whl
spine-packs --help
```

Alternatively, use a dedicated venv and `python -m pip install --no-index
--no-deps ./spine_packs-0.1.0-py3-none-any.whl`. No repository checkout or
`PYTHONPATH` is needed. Obtain a separately released compatible pack and explicit
target inputs before planning; applying still needs the exact plan approval.
Do not overwrite or discard existing execution/checkpoint evidence on upgrade.
