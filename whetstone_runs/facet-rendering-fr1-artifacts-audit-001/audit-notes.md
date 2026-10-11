# Change intent

Review the remaining FR-1 installer artifact-contract increment: seven separate
v2 artifact schemas, shared/embedded/readback closure, exact typed reference
slots, bounded observation preimages, command-family evidence and synthetic
execution/recovery fixtures. The manifest increment was previously reviewed;
this is a new review gate, not inherited approval or full installer qualification.

Baseline: exact Spine `57cda1c2d5589360ee8efe7155fd20b503034c2a`, runtime `0.9.1`,
schema `19`. The commit was verified available. All 17 upstream schema source
file hashes in the new inventory were independently compared to `git show` at
that exact pin. Four legacy write-response and three legacy read-response
validators reuse existing client projections, explicitly recorded in provenance;
their future package integration still requires exact-baseline qualification.

# Expected boundary

One reviewer-only Whetstone `audit-change`, profile `consistency`, through the
embedded Codex CLI after approval of the exact payload. No Editor, automatic
patching, convergence claim, unrelated file reads, web browsing, ledger access,
Spine changes, runtime implementation, deployment, commit, push or publication.
This directory is staged only; no reviewer has been invoked or authorized.

Packs are owner-neutral declarative configuration. Operator artifacts alone may
hold synthetic owner/actor/target IDs. No disclosure grants, actual facet values,
coordination items, notifications, schedules or destination facts are installed.
Real flight fields, labels/order, selected reminder templates and default-profile
policy remain operator decisions. Synthetic stable-status manifests under tests
are not curated or distributable pack releases.

# Specs and machine agreements to check

Primary authority is `specs/installer-artifacts-v2.md` together with
`specs/facet-rendering-packs.md`. V1 encoding/limits/approval/durability/exit
requirements explicitly carried forward are in `specs/installer-artifacts.md`.
The proposed runtime command map and exact source/pointer closure are in
`contracts/installer-spine-0.9.1-inventory.json`. No network schema fetch is needed.
The pure semantic oracle is test code, not an implemented installer or proof of
real public observations. It is intentionally included in this contract review.

Check especially:

1. Closure, target/owner/manifest correlation, exact environment/contract union,
   schema versions and digest domains. Unknown versions must fail before use.
2. Typed null slots and resolution ownership: only approved paths, correct
   producers/fields, earlier accepted prefix, observed IDs for retain, immutable
   revision pins and complete cascaded update approval. No guessed IDs, string
   interpolation or choosing equivalent historical revisions behind current heads.
3. Exact public request mapping and response differences. Canonical request blobs
   forbid JSON numbers; public response text preserves valid public native numbers.
   Facets have no receipt semantic hash; rendering uses `contract_version` and
   top-level evidence. No fabricated universal receipt or catalog fingerprint.
4. Forward recovery from complete bounded preimages, original selected history,
   unchanged suffix preconditions, prefix/prefix-plus-one candidates, exact replay
   and matching provisional IDs before acceptance. Partial results embed the
   checkpoint so they cannot discard a prepared request. No speculative suffix.
5. Verification is read-only and exact-pin-aware; captured responses are separate
   from fresh state, and no success grants disclosure or asserts notification
   delivery. Preserve the old archetype/v1-ordinary comparison rules.
6. Fixture quality: 36 indexed recovery boundaries across create/update flows,
   all 11 write commands, 33 named negative cases, 27 unchanged upstream wire
   vectors, independent hash preimages and post-resolution byte-limit boundary.
   Identify false-positive negative tests, unsound oracle assumptions or material
   spec/schema/test disagreement. Do not assume a passing oracle proves its own
   correctness or the later runtime gates.

# Checks and explicit remaining gates

At staging: verifier passed (143 required files); independent jsonschema 4.26.0
Draft 2020-12 meta/fixture checks and all 82 contract tests passed; 126 runtime
tests passed. Default Python lacks jsonschema and reports 17 explicit skips;
the isolated validator run, not that skipped run, supplies the schema gate.
Tracked and new-file whitespace checks are required before transmission.

No `src/spine_packs/`, v1 contract or released/draft curated pack bytes changed.
One runtime test now explicitly checks the original 12 runtime-consumed schemas,
instead of assuming every future schema is supported by the v1 subset validator.
V2 schemas remain independently standards-validated, not newly admitted at runtime.

Package qualification has NOT run in this increment: `build`/`hatchling` and the
previous isolated supported-Spine CLI builds are unavailable. New schema files
would be included by the existing packaging rule; before any release, run the
package gate on all supported old baselines plus the separately implemented
successor. Do not substitute the 0.9.1 reference CLI into the current installer.
No build, release, staging or deployment readiness is claimed.

FR-2 still requires real read-transport observation/pagination/config/capacity
adversaries, FR-3 durable filesystem fault injection, FR-4 actual continuation
and verification tests, and FR-5 exact-package disposable qualification. Those
are not implemented here. Flag missing machine-contract prerequisites for those
slices, but do not request implementation of their runtime as an audit patch.

Report actionable findings by file/section with minimal proposed correction.
Product decisions must remain open; do not invent policy to close them.
