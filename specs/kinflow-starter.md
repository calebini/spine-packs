# kinflow-starter content

This document is normative for the approved content of `kinflow-starter` under
`spine.pack-manifest.v1`. It does not extend the manifest schema or authorize
installation. General format and authority rules remain in `pack-format.md`,
`overview.md`, `architecture.md`, and `compatibility.md`.

## Draft lineage

`1.0.0-draft.3` is the current draft. It MUST contain exactly the `birthday`,
`flight`, `game_or_competition`, `lesson`, and `medical_appointment`
archetypes, their respective standard profiles, and one local default-binding
intent per archetype.

The medical-only `1.0.0-draft.1`, medical-and-lesson `1.0.0-draft.2`, and their
positive fixtures MUST remain unchanged as review evidence. Every predecessor
definition and binding MUST be preserved without semantic change in draft 3.
Draft 3 MUST retain the exact compatibility declarations and empty dependencies
and MUST have a newly computed content digest. All artifacts remain drafts, not
releases or evidence of installation.

## Lesson meaning and display text

`lesson` denotes a scheduled instructional session, including swimming and
piano lessons, classes, tutoring, coaching, and other private instruction.
Preparation, practice assignments, and homework are not lesson occurrences.

The lesson archetype MUST use:

- `archetype_key`: `lesson`;
- `intended_status`: `active`;
- `revision.display_name`: `Lesson`;
- `revision.description`: `Scheduled instructional sessions such as classes, tutoring, coaching, or private lessons.`; and
- `revision.compatible_item_types`: exactly `["event"]`.

Display text is English only. V1 supports a single unlocalized display string
and a required nullable description, not locale maps or localization fields.

## Lesson notification profile

The profile MUST use:

- `profile_key`: `lesson_standard`;
- `display_name`: `Lesson standard`;
- `description`: `Default reminders for an upcoming lesson.`;
- `intended_status`: `active`; and
- `revision.compatible_item_types`: exactly `["event"]`.

It MUST contain exactly these templates, in the listed lexicographic order:

| Template key | Elapsed offset in seconds | Positive delivery grace in seconds |
| --- | --- | --- |
| `one_hour_before` | `-3600` | `1800` |
| `twenty_four_hours_before` | `-86400` | `21600` |

Each schedule MUST use `kind=once` and `at.kind=target_offset` with
`offset_basis=elapsed`. Each late-handling object MUST use
`kind=deliver_within`. Offset and grace values MUST be decimal strings, not
JSON numbers. A 24-hour elapsed offset is not a calendar-day or local-time rule.

The grace values represent 30 minutes and 6 hours after the respective nominal
reminder times; both windows end before the item target. Delivery behavior and
authoritative timing remain Spine's responsibility.

## Binding and ordering

The lesson binding intent MUST contain exactly
`binding_kind=archetype_default`, `archetype_key=lesson`, and
`notification_profile_key=lesson_standard`. It references definitions in this
pack, not installed Spine IDs or an owner.

In draft 3, archetypes and bindings MUST be ordered `birthday`, `flight`,
`game_or_competition`, `lesson`, then `medical_appointment`. Profiles MUST use
the corresponding lexicographic order. Template ordering is by key, not
reminder time.

## Recurrence and authority

A lesson may be a single session or an occurrence in a recurring series.
Cadence, series membership, occurrence generation, target anchors, rescheduling,
and exceptions MUST remain Spine-owned item state. The pack and its profiles
MUST NOT encode those facts, recurrence scope, recipients, or routes.

`kind=once` describes one template schedule relative to an applicable item
target; it does not declare that the lesson itself can occur only once. The
pack does not generate recurring occurrences or claim that recurrence support
is available in a deployment. Any missing public item-level capability must be
addressed separately in Spine, never with profile fields or runtime code here.

## Game or competition

`game_or_competition` denotes scheduled sports games, tournaments, and
competitions. It and `game_or_competition_standard` MUST be active, compatible
with exactly `["event"]`, and use display names `Game or competition` and
`Game or competition standard`. Their descriptions MUST be `Scheduled sports
games, tournaments, and competitions.` and `Preparation and arrival reminders
for a scheduled game or competition.` respectively.

The profile MUST contain exactly:

| Template key | Basis | Offset | Grace |
| --- | --- | --- | --- |
| `twenty_four_hours_before` | `elapsed` | `-86400` seconds | `21600` seconds |
| `two_hours_before` | `elapsed` | `-7200` seconds | `3600` seconds |

The profile does not calculate travel time, venue arrival time, or check-in
deadlines. Those are item or operator facts.

## Flight

`flight` denotes a scheduled flight departure. It and `flight_standard` MUST be
active, compatible with exactly `["event"]`, and use display names `Flight` and
`Flight standard`. Their descriptions MUST be `Scheduled flight departures.`
and `Booking, travel-document, packing, check-in, gate, and boarding reminders
for a scheduled flight.` respectively.

The profile MUST contain exactly:

| Template key | Basis | Offset | Grace |
| --- | --- | --- | --- |
| `four_hours_before` | `elapsed` | `-14400` seconds | `3600` seconds |
| `one_hour_before` | `elapsed` | `-3600` seconds | `900` seconds |
| `seven_days_before` | `elapsed` | `-604800` seconds | `86400` seconds |
| `twenty_four_hours_before` | `elapsed` | `-86400` seconds | `21600` seconds |

Airline, booking, terminal, gate, flight-status, airport-transportation, and
boarding facts remain item-, operator-, or external-system-owned facts. They
MUST NOT be embedded in the reusable profile.

## Birthday

`birthday` denotes an annual birthday occasion. It and `birthday_standard`
MUST be active, compatible with exactly `["event"]`, and use display names
`Birthday` and `Birthday standard`. Their descriptions MUST be `Annual birthday
occasions for advance planning and day-of recognition.` and `Advance planning
and day-of reminders for a birthday.` respectively.

The profile MUST contain exactly:

| Template key | Calendar-day offset | Local time | Grace |
| --- | --- | --- | --- |
| `birthday_day_at_nine` | `0` | `09:00:00` | `43200` seconds |
| `one_day_before_at_nine` | `-1` | `09:00:00` | `43200` seconds |
| `seven_days_before_at_nine` | `-7` | `09:00:00` | `86400` seconds |
| `thirty_days_before_at_nine` | `-30` | `09:00:00` | `259200` seconds |

Each boundary MUST use `offset_basis=calendar_days` and omit timezone fields.
The timezone and timezone-database version MUST be inherited from the birthday
item's local target. Profile application MUST fail closed when the target
cannot supply them. Annual recurrence, occurrence generation, exceptions, and
the target date remain Spine-owned item facts and MUST NOT appear in the pack.

## Default bindings

Draft 3 MUST bind each of `birthday`, `flight`, and `game_or_competition` to
its same-named `_standard` profile using one owner-neutral
`archetype_default` intent. These bindings contain only pack-local keys.
