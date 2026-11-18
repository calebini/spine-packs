# FR-6 flight pack content

The operator approved a separate `kinflow-flight` pack and selected
`flight_details_standard` as the departure default.
[1.0.0-draft.2](../packs/kinflow-flight/kinflow-flight.1.0.0-draft.2.json)
adds the `flight_arrival` event and its default profile. The read-only planner
can inspect both drafts. Release and installation are later gates.

The [stable 1.0.0 candidate](../packs/kinflow-flight/kinflow-flight.1.0.0.json)
preserves the definitions and compatibility of draft 2. The selected
departure and arrival defaults are therefore carried into the release.

The governing contracts are [facet-rendering-packs.md](facet-rendering-packs.md),
[spine-0.12.0-alignment.md](spine-0.12.0-alignment.md) and the existing
[flight content](kinflow-starter.md#flight). Implementation status and evidence
remain in [implementation-plan.md](implementation-plan.md).

## Draft content

The default is `flight_details_standard`. The ordinary profile
`flight_standard` is also included for explicit selection.
The details profile selects flight number and departure and arrival airport
labels on the seven-day and four-hour reminders. Its one-hour reminder selects
only departure gate as optional detail; the 24-hour reminder stays ordinary.
Arrival timestamp and destination timezone are optional informational text.
All six fields are optional.

Use whole-pack selection to include both profiles. The binding applies when
an authoring request selects the archetype's default in a matching owner
scope. Item presentation and destination disclosure are managed through the
Spine authoring workflow.

## Existing behavior to preserve

- `flight` denotes a scheduled departure and supports exactly `event`.
- The archetype display name/description remain `Flight` and `Scheduled flight
  departures.`; the ordinary `flight_standard` name, description, timing and
  grace values remain as specified in `kinflow-starter.md`.
- Departure time, timezone, primary location and recurrence stay in their
  existing Spine item/scheduling fields. Facets do not replace those authorities.
- Existing starter drafts, stable packs and published installer assets remain
  byte-for-byte unchanged. This work starts a successor artifact, not a rewrite.
- The draft targets exact Spine
  `3e65ef0de9e73b62047a0f6328731db08ca91023`, runtime `0.12.0`, ledger schema
  `20`. That exact Git object was available for this proposal. Its source
  documents were read at that commit, not at checkout HEAD. Other installer
  baselines remain supported independently; the new pack does not infer a range.

AL-3 technical qualification and the tooling-review repairs are checkpointed
in `8dd5861`. That evidence does not release the new content or qualify the
eventual committed release candidate.

## Fields

The pack declares one schema, `flight_details`, compatible with exactly `event`.
It binds the schema to the existing `flight` archetype under facet key `flight`.
The binding lets an authoring agent attach the optional facet.

| Field key | Meaning and type | Required when facet is attached | Queryable |
| --- | --- | --- | --- |
| `flight_number` | Flight designator, e.g. fictional `EX123`; `text`, maximum 32 Unicode code points | No | Yes (approved) |
| `origin` | Departure airport; `reference`, `target_kind=location` | No | No |
| `destination` | Arrival airport; `reference`, `target_kind=location` | No | Yes (approved) |
| `arrival_at` | Informational destination-local arrival timestamp including date and explicit UTC offset; `text`, maximum 64 Unicode code points | No | No |
| `arrival_timezone` | Destination IANA timezone name; `text`, maximum 128 Unicode code points | No | No |
| `departure_gate` | Recorded departure gate, e.g. fictional `B12`; `text`, maximum 32 Unicode code points | No | No |

The schema display name is `Flight details`. Its description is
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

The draft uses `queryable=false` for `departure_gate`, `origin`, `arrival_at`
and `arrival_timezone`. This prevents direct facet-query filtering on those fields,
while preserving ordinary readback and explicitly selected rendering. The flag
controls query indexing, not permissions, disclosure or notification selection.
Neither enabling both approved fields nor storing arrival text adds compound
queries or timestamp-range filtering. Changing released queryability later
would require a schema revision and explicit consumer updates.

All six fields are optional so an agent can attach a partial facet.
Absent optional values are omitted, not represented by null, placeholder data
or invented values.

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
or defaults to embed in the reusable pack.

Spine validates the supported text-field shape and bounds. It does not validate
RFC 3339 timestamp semantics, IANA timezone membership, agreement between the
offset and named zone, or chronological consistency merely because of these
field names. The authoring agent must validate supplied values: use a full
destination-local timestamp with date and explicit offset, check a supplied IANA
zone against the applicable timezone data, and check that the offset agrees at
the arrival instant when both fields are present. When departure is known, compare instants
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

## Rendering definitions

Both definitions support exactly `event`, using the existing base rendering
contract `spine.notification-rendering.v1` and profile
`spine.notification-rendering.concise-en-ca.v1`. They pin the same local
`flight_details` schema under facet key `flight`.

### Flight number and airports — seven days and four hours

The definition `flight_details` has display name `Flight details` and description
`Selected flight number and airport labels for flight reminders.`

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

The definition `flight_departure_gate` has display name `Flight departure gate`
and description `Optional recorded departure gate for a flight boarding reminder.`

| Presentation order | Selection key | Source | Literal label | Projection |
| ---: | --- | --- | --- | --- |
| 1 | `departure_gate` | `flight.departure_gate` | `Gate` | `value` |

This definition selects only the gate field. It does not select flight number
or airport fields at one hour; the ordinary reminder body remains unchanged.
When the optional gate value is missing, Spine omits that detail and retains
the eligible ordinary reminder. Missing optional
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

## Notification profiles

`flight_details_standard` is the archetype default. It has display name
`Flight details standard`
and description
`Booking, travel-document, packing, check-in, gate, and boarding reminders for a scheduled flight, with selected flight details at seven days and four hours and an optional departure gate at one hour.`

Both profiles retain exactly these existing schedules and late-delivery windows:

| Template key | Before departure, elapsed time | Late-delivery window | Rendering in the details profile |
| --- | --- | --- | --- |
| `seven_days_before` | 7 days | 24 hours | Pin `flight_details` |
| `twenty_four_hours_before` | 24 hours | 6 hours | Ordinary |
| `four_hours_before` | 4 hours | 1 hour | Pin `flight_details` |
| `one_hour_before` | 1 hour | 15 minutes | Pin `flight_departure_gate` and omit gate detail when missing |

`flight_standard` remains ordinary on all four reminders. In manifest v2 every
template states its rendering explicitly. Storage order remains canonical by
template key, not the chronological order used for review here. Preserve the
starter's 75-percent spacing rule and exact approved grace values.

These per-reminder choices are operator-approved content decisions, not
requirements imposed by Spine. They exercise scalar and location-label
projections without duplicating schedules or adding a gate-specific reminder.
Do not apply both complete profiles to the same item merely to add details;
the agent should deliberately choose the intended profile application.

## Departure draft selection

The standalone `kinflow-flight` pack starts at
[`1.0.0-draft.1`](../packs/kinflow-flight/kinflow-flight.1.0.0-draft.1.json). It uses
`spine.pack-manifest.v2`, declares the exact 0.12.0 runtime and its seven
reviewed content contracts, and has `dependencies=[]`. Installer versioning
and tag/publication approval remain separate release decisions.

Draft 1 declares one archetype, one schema, one facet binding, two
rendering definitions, two profiles and one default binding:
`flight -> flight_details_standard`. An equivalent historical v1
`flight_standard` can be retained when selected because its ordinary
presentation and timing match the draft.

Use selection `all` to include all eight configuration objects.
Archetype-only selection includes seven objects covering the default profile,
both rendering definitions and the facet configuration. The ordinary profile
is the extra object selected by `all`.

On a fresh owner catalog the plan proposes the details default. It retains an
equivalent binding. A preexisting `flight_standard` binding or any other
different flight default appears as binding drift and requires explicit
authorization for an update. The same approval boundary applies to conflicts
on shared owner-local schema, profile and definition keys.

## Disclosure, application and historical behavior

An agent can request the details default while facet values are still absent.
Once a policy uses an authorized rendering definition, Spine checks the
available values at render time. A gate supplied later can appear on the
one-hour reminder if it is available and authorized when Spine renders it.
An operator chooses the item owner, exact definition revision,
approved selection subset, profile-scoped use, destination and permitted airport
location identities through Spine's disclosure workflow. None belongs in the
reusable pack. A narrower approved subset may omit `From` or `To` without
requiring a new pack; a new definition/revision is a different approval scope.
The flight-details and gate definitions are distinct scopes; neither borrows
the other's disclosure approval. Authoring a selected definition still needs
valid presentation/disclosure configuration when its optional values are absent.

Spine's v3 authoring request requires a presentation choice for each surviving
definition-pinned template. The agent can explicitly choose ordinary
presentation or select the definition with valid disclosure configuration.
Spine's existing attempt rules omit missing or unauthorized optional details
when the reminder is otherwise eligible.

The pinned guide at this exact baseline requires fresh trusted-local items to
start with ordinary presentation, followed by explicit ownership/adoption,
facet authoring and presentation setup if details are wanted. The selected
profile supplies the schedule and template pins. The agent can enable the
authorized detail presentation with a presentation-only edit, even before
the optional values are populated. Consumer readiness for this workflow
must be verified separately.

Installed schema/rendering/profile revisions are pinned exactly. Publishing
later content does not upgrade existing profile applications or historical
notifications. Changing fields, labels, order, reminder pins or defaults needs
a new reviewed pack version and explicit installation changes. Item/facet
values remain separately authored Spine data; packs never contain travel facts.

## Flight arrival and pickup task

`1.0.0-draft.2` adds active, event-only `flight_arrival` with display name
`Flight arrival`. The authoring agent sets the event start to scheduled
landing in the destination's timezone and sets the arrival airport as
`item.primary_location`. It can create a place with a label such as
`Toronto Pearson (YYZ)` or reuse a known Spine location by ID. The time anchor
carries its own timezone. The facet adds the inbound flight number, origin
airport and terminal.

The pickup is a separate task. Its due anchor holds the agreed meetup time,
and its first-class primary location holds the specific meetup point, such as
`Terminal 2 arrivals curb, Door B`. The agent can author a fixed due time or
use Spine's event-start-to-task-due binding when creating a task with an elapsed
offset from landing. For timing that follows the event, opt into Spine's
`follow_source` behavior. Keep the meetup point and task reminders on the
task. The manifest provisions the arrival configuration. Task creation,
location selection and any temporal binding belong to item authoring.

The `flight_arrival` facet binding pins the `flight_arrival_details` schema.
All fields below are optional:

| Field | Type | Queryable |
| --- | --- | --- |
| `arrival_terminal` | Text, maximum 32 Unicode code points | No |
| `flight_number` | Text, maximum 32 Unicode code points | Yes, exact match |
| `origin` | Spine location reference for the departure airport | No |

The `flight_arrival_details` rendering definition selects these in order:
`Flight` from `flight_number` via `value`, `From` from `origin` via
`location_label`, and `Terminal` from `arrival_terminal` via `value`.
Spine can omit an unavailable detail independently at render time. Authoring
uses explicit presentation choices and disclosure for the selected fields.

The default profile `flight_arrival_standard` uses once-only elapsed
offsets from the arrival event start:

| Template key | Offset in seconds | Late window in seconds | Rendering |
| --- | ---: | ---: | --- |
| `twenty_four_hours_before` | `-86400` | `21600` | Ordinary |
| `one_hour_before` | `-3600` | `1800` | `flight_arrival_details` |
| `at_scheduled_landing` | `0` | `900` | `flight_arrival_details` |

Use a title such as `Scheduled arrival of EX123` so the ordinary message
describes the time as scheduled. The reminder at offset zero signals the event
anchor. Confirmation of actual landing comes from a separate source.

The departure configuration carries forward from draft 1. Selecting
`flight_arrival` in draft 2 includes its six configuration objects.
Selecting `flight` includes its seven default configuration objects.
Whole-pack selection includes all 14 objects and both defaults.

## Draft verification and release gates

The content tests check draft digests, field declarations, rendering
selections and profile schedules, including the exact landing offset.
Planning tests use synthetic catalog evidence to check the arrival, departure
and whole-pack selections and their rendering references.

The remaining work is tracked in the
[implementation plan](implementation-plan.md). Destination disclosure, item
authoring and consumer readiness are checked separately from pack content.

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
