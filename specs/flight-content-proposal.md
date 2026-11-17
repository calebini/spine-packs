# FR-6 flight-content proposal

Status: proposed for operator review on 2026-11-17. The operator approved
capturing optional arrival timestamp/timezone text as informational data while
deferring its notification rendering, and making `flight_number` and
`destination` queryable. The operator also approved optional, non-queryable
`departure_gate`, flight-number/airport rendering at seven days and four hours,
and gate-only rendering at one hour. Remaining content choices are pending
as identified below. This document is a review draft, not a pack manifest,
release, disclosure authorization or instruction to install configuration.

The governing contracts are [facet-rendering-packs.md](facet-rendering-packs.md),
[spine-0.12.0-alignment.md](spine-0.12.0-alignment.md) and the existing
[flight content](kinflow-starter.md#flight). Implementation status and evidence
remain in [implementation-plan.md](implementation-plan.md).

## Recommendation for review

Start with a small flight-only pack containing the existing ordinary flight
profile and a new, explicitly selected details profile. Keep `flight_standard`
as the default. Offer flight number, departure-airport label and arrival-airport
label on the seven-day and four-hour reminders. The one-hour reminder selects
only departure gate as optional detail; the 24-hour reminder stays ordinary.
Also capture arrival timestamp and
destination timezone as optional informational text, without selecting them
for notification rendering. All six fields remain optional.

Install the whole flight-only pack so the opt-in profile is included. Existing
items and profile applications are not updated by installation. Details become
usable only through a separate, explicitly authorized Spine authoring and
destination-disclosure workflow.

## Existing behavior to preserve

- `flight` denotes a scheduled departure and supports exactly `event`.
- The archetype display name/description remain `Flight` and `Scheduled flight
  departures.`; the ordinary `flight_standard` name, description, timing and
  grace values remain as specified in `kinflow-starter.md`.
- Departure time, timezone, primary location and recurrence stay in their
  existing Spine item/scheduling fields. Facets do not replace those authorities.
- Existing starter drafts, stable packs and published installer assets remain
  byte-for-byte unchanged. This work starts a successor artifact, not a rewrite.
- The candidate compatibility target is only exact Spine
  `3e65ef0de9e73b62047a0f6328731db08ca91023`, runtime `0.12.0`, ledger schema
  `20`. That exact Git object was available for this proposal. Its source
  documents were read at that commit, not at checkout HEAD. Other installer
  baselines remain supported independently; the new pack does not infer a range.

AL-3 technical qualification and the tooling-review repairs are checkpointed
in `8dd5861`. That evidence does not release the new content or qualify the
eventual committed release candidate.

## Proposed fields

Use one schema, suggested key `flight_details`, compatible with exactly `event`.
Bind it to the existing `flight` archetype under facet key `flight`. A binding
makes a facet available; it does not attach values or require every flight to
have the facet.

| Field key | Meaning and type | Required when facet is attached | Queryable |
| --- | --- | --- | --- |
| `flight_number` | Flight designator, e.g. fictional `EX123`; `text`, maximum 32 Unicode code points | No | Yes (approved) |
| `origin` | Departure airport; `reference`, `target_kind=location` | No | No |
| `destination` | Arrival airport; `reference`, `target_kind=location` | No | Yes (approved) |
| `arrival_at` | Informational destination-local arrival timestamp including date and explicit UTC offset; `text`, proposed maximum 64 Unicode code points | No | No |
| `arrival_timezone` | Destination IANA timezone name; `text`, proposed maximum 128 Unicode code points | No | No |
| `departure_gate` | Recorded departure gate, e.g. fictional `B12`; `text`, proposed maximum 32 Unicode code points | No (approved) | No (approved) |

Recommended display name: `Flight details`. Recommended description:
`Optional flight number, airport references, departure gate, and informational arrival timestamp and destination timezone for a scheduled flight.`

The operator approved `queryable=true` for `flight_number` and `destination`.
This uses Spine's existing `item.facets.query` capability: one typed equality
predicate within an explicit item-owner scope and exact schema revision.
Flight-number equality is case-sensitive under the existing text rules.
Destination equality matches the referenced Spine location ID, not its display
label, a city name or an airport code supplied as text. An agent must resolve
the intended location before filtering by it; no location IDs belong in the pack.
The installer provisions these definition flags only. Item queries are separate
Spine operations and are not added to the installer's command allowlist.

The operator approved `queryable=false` for `departure_gate`.
Recommend retaining `queryable=false` for `origin`, `arrival_at` and
`arrival_timezone`. This prevents direct facet-query filtering on those fields,
while preserving ordinary readback and explicitly selected rendering. The flag
controls query indexing, not permissions, disclosure or notification selection.
Neither enabling both approved fields nor storing arrival text adds compound
queries or timestamp-range filtering. Changing released queryability later
would require a schema revision and explicit consumer updates.

Incomplete travel information should not block attaching a partial facet, so
all fields remain optional in the proposal.
Absent optional values are omitted, not represented by null, placeholder data
or invented values. Remaining required/queryable choices are identified below;
the arrival fields' optionality, gate optionality/non-queryability, and the two
approved true query flags are settled.

Exclude airline, terminal, flight status, booking references, passport
details and live external lookups from this first schema. No policy says those
facts may never be supported; adding them later requires a reviewed successor.
Airport references remain actual Spine location references supplied during
separate item authoring. The pack contains no airport IDs or airport directory.

### Approved arrival capture; rendering deferred

The operator approved these two optional data fields after deferring native
arrival-time rendering. For illustration only, an authoring agent could record
`arrival_at=2026-11-18T08:45:00+01:00` and
`arrival_timezone=Europe/Paris`. These are fictional item values, not constants
or defaults to embed in the reusable pack. Text-length bounds above remain
proposed content details for review.

Spine validates the supported text-field shape and bounds. It does not validate
RFC 3339 timestamp semantics, IANA timezone membership, agreement between the
offset and named zone, or chronological consistency merely because of these
field names. The authoring agent must validate supplied values: use a full
destination-local timestamp with date and explicit offset, check a supplied IANA
zone against the applicable timezone data, and check that the offset agrees at the arrival
instant when both fields are present. When departure is known, compare instants
to check chronology; local clock values alone are insufficient across timezones
and date-line crossings. Unknown facts remain absent rather than guessed from
airport labels or other prose. These are authoring responsibilities, not a new
runtime validator or a claim of schema-enforced cross-field constraints.

These fields are informational travel data. Departure remains the event's
scheduling anchor. They neither create nor update an event end anchor, supply
arrival-based reminders, nor replace authoritative event times. If an
authoritative event end is also present, inconsistent information must be
surfaced rather than silently overriding either value. Later synchronization
or promotion into typed temporal facts requires a separate explicit workflow.

No rendering selection below references either arrival field, including via
ordinary text projection. Capturing them grants no disclosure permission.
Native timestamp validation, destination-local date/time formatting and
selection of authoritative arrival time remain deferred capabilities; this
proposal does not require an upstream Spine change to store the two text fields.

## Proposed rendering definitions

Both definitions support exactly `event`, using the existing base rendering
contract `spine.notification-rendering.v1` and profile
`spine.notification-rendering.concise-en-ca.v1`. They pin the same local
`flight_details` schema under facet key `flight`.

### Flight number and airports — seven days and four hours

Suggested definition key/display name: `flight_details` / `Flight details`.
Suggested description: `Selected flight number and airport labels for flight reminders.`

| Presentation order | Selection key | Source | Literal label | Projection |
| ---: | --- | --- | --- | --- |
| 1 | `flight_number` | `flight.flight_number` | `Flight` | `value` |
| 2 | `origin` | `flight.origin` | `From` | `location_label` |
| 3 | `destination` | `flight.destination` | `To` | `location_label` |

The source notation in this table is explanatory, not a new manifest path
language. Actual selections use the reviewed `facet_key`, local `schema_ref`
and `field_key` members. Schema fields use canonical key order; rendering
selections retain the authored presentation order above.

For review, fictional detail values could read `Flight: EX123`,
`From: Example departure airport`, `To: Example arrival airport`. These are
illustrations of the selected labels/values, not a promised complete message or
text embedded in a pack. Spine retains its ordinary reminder body and owns the
exact suffix, separators, normalization and size/omission rules. The pack
does not supply executable or freeform message templates.

Only the canonical location label is selectable. Addresses, coordinates,
provider metadata and raw IDs are not substitutes. A location label can itself
be sensitive and still needs location-specific disclosure approval. Facet
airports do not replace the event's primary location or time authority.

### Departure gate only — one hour

Suggested definition key/display name:
`flight_departure_gate` / `Flight departure gate`.
Suggested description: `Optional recorded departure gate for a flight boarding reminder.`

| Presentation order | Selection key | Source | Literal label | Projection |
| ---: | --- | --- | --- | --- |
| 1 | `departure_gate` | `flight.departure_gate` | `Gate` | `value` |

This definition selects only the gate field. It does not select flight number
or airport fields at one hour; the ordinary reminder body remains unchanged.
When the optional gate value is missing, Spine
omits that detail and retains the eligible ordinary reminder. Missing optional
fields are omitted independently; for example, a missing airport field does
not suppress an available flight number in the other definition. Existing
disclosure, admission, normalization and size rules continue to apply; a
missing value is not a substitute for approval or a corruption fallback.

For illustration only, a recorded value could produce `Gate: B12`. Presence
means a recorded gate value is available, not that Spine queried a live source
or confirmed it recently. The operator selected presence-based gate rendering;
this proposal adds no freshness timeout, advisory activation or external fetch.
A future authorized advisory/authoring workflow may update or clear the value
through Spine. Source provenance and freshness policy for that workflow remain
separate work, not additional required fields in this first facet.

## Proposed notification profiles

Retain `flight_standard` as the ordinary default. Add a distinct, flight-specific
profile with suggested key `flight_details_standard`, display name
`Flight details standard`, and description:
`Booking, travel-document, packing, check-in, gate, and boarding reminders for a scheduled flight, with selected flight details at seven days and four hours and an optional departure gate at one hour.`

Both profiles retain exactly these existing schedules and late-delivery windows:

| Template key | Before departure, elapsed time | Late-delivery window | Rendering in the proposed details profile |
| --- | --- | --- | --- |
| `seven_days_before` | 7 days | 24 hours | Pin the proposed `flight_details` definition |
| `twenty_four_hours_before` | 24 hours | 6 hours | Ordinary |
| `four_hours_before` | 4 hours | 1 hour | Pin the proposed `flight_details` definition |
| `one_hour_before` | 1 hour | 15 minutes | Pin the proposed `flight_departure_gate` definition; omit gate detail when missing |

`flight_standard` remains ordinary on all four reminders. In manifest v2 every
template states its rendering explicitly. Storage order remains canonical by
template key, not the chronological order used for review here. Preserve the
starter's 75-percent spacing rule and exact approved grace values.

These per-reminder choices are operator-approved content decisions, not
requirements imposed by Spine. They exercise scalar and location-label
projections without duplicating schedules or adding a gate-specific reminder.
Do not apply both complete profiles to the same item merely to add details;
the agent should deliberately choose the intended profile application.

## Default, selection and distribution choices

Recommend a separate flight-only pack, suggested ID `kinflow-flight`, with an
initial proposed draft `1.0.0-draft.1` toward `1.0.0`. These are proposed names
and versions for review, not allocated or published identities. Use
`spine.pack-manifest.v2`, the exact 0.12.0 compatibility singleton and its seven
reviewed content contracts; keep `dependencies=[]`. Installer versioning and
tag/publication approval remain separate release decisions.

The proposed pack declares one archetype, one schema, one facet binding, two
rendering definitions, two profiles and one default binding:
`flight -> flight_standard`. The ordinary profile's existing semantic content
is retained; explicit v2 ordinary markers do not authorize a forced revision
of an equivalent historical v1 profile. The new details profile is nondefault.

There are two existing format/selection constraints worth making explicit:

1. Manifest v2 requires at least one default binding. An entirely binding-free
   opt-in pack would need a separately reviewed format change. Keeping the
   ordinary flight default supplies the required binding without such a change.
2. Granular selection of `flight` follows its default profile and facet binding;
   it does not pull in the unreferenced details profile/rendering definitions.
   The supported proposal therefore uses selection `all` on this small
   flight-only pack. No installer selector or dependency rule is changed.

Here `all` selects eight configuration objects. Archetype-only selection
selects five, leaving out the nondefault profile and both rendering definitions.

On a fresh owner catalog this creates the ordinary default. An equivalent
existing default is retained. If an operator has another flight default,
the plan reports binding drift and requires explicit authorization before
changing it; opting into the pack is not permission to override that choice.
Likewise, conflicting schema/profile/definition keys fail closed without exact
update approval. A separate pack is a distribution boundary, not isolated
catalog ownership or permission to overwrite shared owner-local keys.

The alternative is a successor starter release carrying the other 51
archetypes unchanged, or making the new details profile the flight default.
Those alternatives increase release scope or change future authoring behavior;
neither is selected by this proposal. Supporting nondefault-profile inclusion
under archetype-only selection would be separate installer/contract work.

## Disclosure, application and historical behavior

The proposed selections answer what this profile can request, not who may
receive it. An operator still chooses the item owner, exact definition revision,
approved selection subset, profile-scoped use, destination and permitted airport
location identities through Spine's disclosure workflow. None belongs in the
reusable pack. A narrower approved subset may omit `From` or `To` without
requiring a new pack; a new definition/revision is a different approval scope.
The flight-details and gate definitions are distinct scopes; neither borrows
the other's disclosure approval. Authoring a selected definition still needs
valid presentation/disclosure configuration when its optional values are absent.

Missing approval at authoring is not permission to downgrade silently. The
authoring agent must explicitly choose ordinary presentation or complete the
separate authorization/application workflow. At attempt time, eligible ordinary
reminders can omit missing or unauthorized optional details under Spine's
existing rules. Corruption, unsupported evidence and operational failures are
not treated as missing optional values.

The pinned guide at this exact baseline requires fresh trusted-local items to
start with ordinary presentation, followed by explicit ownership/adoption,
facet authoring and presentation setup if details are wanted. Consumer readiness
for that workflow must be checked separately. Installing this pack performs
none of those item-level operations and cannot claim delivery readiness.

Installed schema/rendering/profile revisions are pinned exactly. Publishing
later content does not upgrade existing profile applications or historical
notifications. Changing fields, labels, order, reminder pins or defaults needs
a new reviewed pack version and explicit installation changes. Item/facet
values remain separately authored Spine data; packs never contain travel facts.

## Decisions requested from the operator

Arrival capture as optional informational text, excluded from rendering, is
approved, as is queryability of `flight_number` and `destination`. Optional,
non-queryable gate capture and the per-reminder selection contents/timing in D2
are also approved. Remaining field bounds/display metadata and D3-D4 choices
remain pending. Approval of the proposal
should identify any deviations; preparing it does not approve those choices.

| Decision | Recommended choice |
| --- | --- |
| D1: fields and validation | Approved: optional informational arrival text, `queryable=true` for `flight_number`/`destination`, and optional non-queryable `departure_gate`. Remaining recommendations: all fields optional, origin/arrival fields non-queryable and proposed text bounds/metadata as described above |
| D2: visible details | Approved: flight number/airports at seven days and four hours, gate only at one hour when present, 24-hour reminder ordinary. Proposed labels/order remain `Flight`, `From`, `To` and `Gate` in their respective definitions |
| D3: profile/default | Add `flight_details_standard` for explicit use; keep `flight_standard` as the default; retain all existing timing/grace values |
| D4: distribution/identity | Separate `kinflow-flight`, proposed `1.0.0-draft.1` toward `1.0.0`; install with selection `all`; use the proposed schema/definition keys and display metadata above |

Destination-specific disclosure and item authoring remain later operator
configuration. Installer release version, consumer readiness, exact staging
baseline and publication/deployment permissions remain separate release gates.

## Next bounded implementation after content approval

1. Record the approved choices, create the one new draft manifest and content
   assertions, and leave all existing pack artifacts unchanged. Verify both
   projections, both profile schedules, selection closure and reference edges,
   including the explicitly selected nondefault profile.
   Assert both arrival fields are optional supported text declarations and are
   absent from every rendering selection. Distinguish these content assertions
   from timestamp/timezone semantic validation by future item-authoring agents.
   Assert the approved flight-number/destination query flags. Document exact
   location-reference matching rather than promising label-based queries.
   Assert optional, non-queryable gate text; two distinct rendering definitions;
   and exact seven-day/four-hour/one-hour template pins with 24-hour ordinary
   rendering. Preserve Spine's per-selection omission behavior for missing
   optional values without claiming a new pack-level rendering engine.
2. Exercise missing/retain/authorized-drift/refused-drift and read-only verify
   with new disposable configuration-only ledgers and the exact qualified public
   CLI. Check that `all` includes every proposed object while archetype-only
   selection has the narrower closure described above. No item/facet values,
   disclosure grants, materialization or sends are part of pack installation.
3. Complete the scoped content review and any required separately approved
   external audit. Finalize successor pack/installer release identities, then
   qualify the exact committed release candidate and its checksum-pinned assets.
4. Prepare the staging handoff with explicit owner/target, selected pack,
   plan approval and readback verification. Report consumer/disclosure setup
   separately. Publication and operator installation require separate approval.

## Inspected sources

Spine sources below were read through `git show` at the exact 0.12.0 pin above:

- `specs/archetype-facets.md`: optional bindings, types and optional-field rules.
- `specs/notification-rendering-definitions.md`, Sections 3.2, 5 and 6:
  supported projections, exact schema pins, profile scope and location labels.
- `docs/NOTIFICATION_RENDERING_GUIDE.md`: separate disclosure, application,
  ordinary authoring and verification workflows. Its schema-19 migration
  checklist is historical; it is not a schema-20 deployment procedure.

Local format and closure constraints were checked against
`contracts/schemas/spine-pack-manifest.v2.schema.json`, `facet_manifest.py` and
`facet_graph.py`. Synthetic fixtures are technical evidence, not approved content.
