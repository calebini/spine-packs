# Installer planning and apply-preflight boundary audit

## Authorization state

This payload is staged only. Do not invoke the nested reviewer until the
operator explicitly approves the exact file list.

## Change intent

Assess the committed read-only installer planner and non-mutating apply
preflight before any Spine write, checkpoint, continuation, or public `apply`
command is implemented.

## Expected boundary

- Spine remains the sole authority for installed state.
- Planning and preflight use only the pinned public Spine read-command surface.
- The preflight validates complete immutable plan and approval artifacts,
  released/apply-eligible posture, manifest and request identity, exact target
  compatibility, fresh catalog state, and all planned command templates.
- Incomplete update authorization, drafts, blocked or ineligible plans,
  mismatched identities, incompatible targets, and stale observations fail
  closed before any write can be launched.
- A successful preflight returns internal execution-ready facts only. It does
  not publish an apply result, checkpoint, or public `apply` command.

## Reviewer questions

1. Can any path in the submitted implementation launch, smuggle, or replay a
   Spine write during planning or preflight?
2. Are the plan, approval, manifest, request, target, environment, catalogs,
   snapshots, classifications, actions, and update authorizations validated and
   correlated strongly enough for the stated local single-operator boundary?
3. Can a changed or stale plan pass by recomputing only an outer digest, by
   exploiting result references, or by changing unselected manifest content?
4. Does the implementation preserve the distinction between eligibility,
   approval, preflight readiness, and successful application?
5. Do the focused tests cover the material positive and negative paths needed
   before the first write-enabled slice begins?
6. Are implementation and documentation consistent, without silently claiming
   write execution, recovery, live-target qualification, or release readiness?

## Out of scope

- Phase One or Phase Two convergence
- Editor invocation or source mutation
- implementation of writes, checkpoints, continuation, verify, or packaging
- redesign of already accepted installer semantics
- cosmetic cleanup

Report verdict, boundary preservation, blocker/major/minor findings, any
out-of-scope observations, and whether Slice 3 may safely begin from this
boundary. This audit does not declare convergence or runtime qualification.
