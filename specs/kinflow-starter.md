# kinflow-starter content

This document is normative for the approved content of `kinflow-starter` under
`spine.pack-manifest.v1`. It does not extend the manifest schema or authorize
installation. General format and authority rules remain in `pack-format.md`,
`overview.md`, `architecture.md`, and `compatibility.md`.

## Draft lineage

`1.0.0-draft.4` is the current draft. It MUST contain exactly these archetypes,
their respective same-named `_standard` profiles, and one local default-binding
intent per archetype:

- `birthday`;
- `camp_or_program`;
- `community_event`;
- `dinner_reservation`;
- `flight`;
- `game_or_competition`;
- `lesson`;
- `medical_appointment`;
- `parent_teacher_meeting`;
- `party`;
- `performance`;
- `playdate`;
- `school_deadline`;
- `school_event`;
- `social_gathering`; and
- `visitor_arrival`.

The medical-only `1.0.0-draft.1`, medical-and-lesson `1.0.0-draft.2`, expanded
event `1.0.0-draft.3`, and their positive fixtures MUST remain byte-for-byte
unchanged as review evidence. Every predecessor definition and binding MUST be
preserved without semantic change in draft 4. Draft 4 MUST retain the exact
compatibility declarations and empty dependencies and MUST have a newly
computed content digest. All artifacts remain drafts, not releases or evidence
of installation.

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

Draft 4 archetypes, profiles, and bindings MUST use the lexicographic ordering
required by `specs/pack-format.md`. Template ordering is by key, not reminder
time. Historical draft 3 remains unchanged in its earlier canonical order.

## Late-delivery spacing policy

Draft 4 profiles MUST leave a quiet interval before the next scheduled
notification. For two templates whose resolved nominal notification instants
are `A` and `B`, where `A` occurs before `B`, the positive delivery grace for
`A` MUST be no greater than the smaller of:

- the domain-specific grace selected for `A`; and
- `floor(0.75 * (B - A))` seconds.

For the final pre-target reminder, the item target is the next boundary. A
template nominally scheduled at the target has no later target boundary and
MUST instead declare a short, explicit domain-specific grace. Calendar-day and
mixed-basis profiles MUST satisfy the rule against the shortest possible gap
between their resolved instants, including an early target time and local
clock changes. If the ordering or gap cannot be established, validation or
application MUST fail closed rather than assume a longer interval.

The rule constrains pack authorship; it does not merge notification
opportunities or add scheduling behavior to this repository. The JSON arrays
remain ordered lexicographically by template key, so chronological ordering
for this calculation is derived from the schedules rather than array position.

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

## Education and activities

Every definition in this section MUST use `intended_status=active`. Profiles
MUST be archetype-specific even where their template schedules repeat another
profile. Repeated templates do not create a shared profile identity.

The archetypes MUST be exactly:

| Archetype key | Display name | Description | Compatible item types |
| --- | --- | --- | --- |
| `camp_or_program` | `Camp or program` | `Scheduled camps and bounded programs represented by their overall start.` | `event` |
| `parent_teacher_meeting` | `Parent-teacher meeting` | `Scheduled meetings between parents or guardians and teachers.` | `event` |
| `performance` | `Performance` | `Scheduled recitals, concerts, plays, and similar events in which the participant is performing.` | `event` |
| `school_deadline` | `School deadline` | `School-related completion and submission deadlines.` | `task` |
| `school_event` | `School event` | `Scheduled school carnivals, fairs, concerts, open houses, and similar events.` | `event` |

The corresponding profiles MUST be exactly:

| Profile key | Display name | Description | Compatible item types |
| --- | --- | --- | --- |
| `camp_or_program_standard` | `Camp or program standard` | `Preparation and start reminders for an upcoming camp or program.` | `event` |
| `parent_teacher_meeting_standard` | `Parent-teacher meeting standard` | `Preparation and attendance reminders for a parent-teacher meeting.` | `event` |
| `performance_standard` | `Performance standard` | `Preparation and arrival reminders for a scheduled performance.` | `event` |
| `school_deadline_standard` | `School deadline standard` | `Progressive reminders leading up to and on a school deadline.` | `task` |
| `school_event_standard` | `School event standard` | `Preparation and arrival reminders for a school event.` | `event` |

Their templates MUST be exactly:

| Profile | Template key | Basis | Offset | Local time | Grace |
| --- | --- | --- | --- | --- | --- |
| `camp_or_program_standard` | `one_day_before_at_noon` | `calendar_days` | `-1` day | `12:00:00` | `21600` seconds |
| `camp_or_program_standard` | `seven_days_before_at_noon` | `calendar_days` | `-7` days | `12:00:00` | `86400` seconds |
| `camp_or_program_standard` | `thirty_days_before_at_noon` | `calendar_days` | `-30` days | `12:00:00` | `259200` seconds |
| `camp_or_program_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |
| `parent_teacher_meeting_standard` | `one_hour_before` | `elapsed` | `-3600` seconds | — | `1800` seconds |
| `parent_teacher_meeting_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `performance_standard` | `seven_days_before` | `elapsed` | `-604800` seconds | — | `86400` seconds |
| `performance_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `performance_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |
| `school_deadline_standard` | `due_day_at_nine` | `calendar_days` | `0` days | `09:00:00` | `21600` seconds |
| `school_deadline_standard` | `one_day_before_at_nine` | `calendar_days` | `-1` day | `09:00:00` | `43200` seconds |
| `school_deadline_standard` | `seven_days_before_at_nine` | `calendar_days` | `-7` days | `09:00:00` | `86400` seconds |
| `school_deadline_standard` | `two_days_before_at_nine` | `calendar_days` | `-2` days | `09:00:00` | `43200` seconds |
| `school_event_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `school_event_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |

`performance` is for a participant or performer, not merely an attendee; a
generic attended performance may use another event archetype. A
`camp_or_program` target is the overall program start, not each session in a
recurring program. Session recurrence and occurrence creation remain
Spine-owned. A `school_deadline` target represents the due date for completion
or submission. Operators SHOULD use an exact item target when a deadline has a
specific time; the reusable day-based profile does not embed that local fact.

The one-day camp reminder uses a six-hour grace rather than twelve hours. This
keeps it within the 75% spacing cap even when the program starts at midnight:
the next two-hour reminder is only ten elapsed hours after the preceding noon
reminder.

## Social

Every definition in this section MUST use `intended_status=active` and be
compatible with exactly `event`. The archetypes MUST be exactly:

| Archetype key | Display name | Description |
| --- | --- | --- |
| `community_event` | `Community event` | `Scheduled community, neighborhood, civic, and local public events.` |
| `dinner_reservation` | `Dinner reservation` | `Scheduled restaurant dinner reservations.` |
| `party` | `Party` | `Scheduled parties and celebrations.` |
| `playdate` | `Playdate` | `Scheduled playdates for children and their caregivers.` |
| `social_gathering` | `Social gathering` | `Scheduled informal social gatherings.` |
| `visitor_arrival` | `Visitor arrival` | `Expected arrivals of visitors at a scheduled time.` |

The corresponding profiles MUST be exactly:

| Profile key | Display name | Description |
| --- | --- | --- |
| `community_event_standard` | `Community event standard` | `Preparation and arrival reminders for a community event.` |
| `dinner_reservation_standard` | `Dinner reservation standard` | `Arrival reminders for a dinner reservation, including a time-now reminder.` |
| `party_standard` | `Party standard` | `Planning, preparation, and arrival reminders for a party.` |
| `playdate_standard` | `Playdate standard` | `Coordination and arrival reminders for a playdate.` |
| `social_gathering_standard` | `Social gathering standard` | `Preparation and arrival reminders for a social gathering.` |
| `visitor_arrival_standard` | `Visitor arrival standard` | `Preparation and arrival-time reminders for an expected visitor.` |

Their templates MUST be exactly:

| Profile | Template key | Basis | Offset | Local time | Grace |
| --- | --- | --- | --- | --- | --- |
| `community_event_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `community_event_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |
| `dinner_reservation_standard` | `at_reservation_time` | `elapsed` | `0` seconds | — | `900` seconds |
| `dinner_reservation_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |
| `party_standard` | `seven_days_before` | `elapsed` | `-604800` seconds | — | `86400` seconds |
| `party_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `party_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |
| `playdate_standard` | `one_hour_before` | `elapsed` | `-3600` seconds | — | `1800` seconds |
| `playdate_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `social_gathering_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `social_gathering_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |
| `visitor_arrival_standard` | `at_arrival_time` | `elapsed` | `0` seconds | — | `900` seconds |
| `visitor_arrival_standard` | `one_day_before_at_noon` | `calendar_days` | `-1` day | `12:00:00` | `21600` seconds |
| `visitor_arrival_standard` | `one_hour_before` | `elapsed` | `-3600` seconds | — | `1800` seconds |

The `0` offsets are intentional time-now reminders anchored to the dinner
reservation time and expected visitor arrival. They do not assert that the
person or reservation actually arrived. The visitor's one-day reminder uses
the target's local date at noon and inherits timezone facts from the item.
Specific venues, invitees, addresses, reservation details, hosts, and visitor
identities remain item- or operator-owned facts.

## Default bindings

Draft 4 MUST bind every included archetype to its same-named `_standard`
profile using exactly one owner-neutral `archetype_default` intent. These
bindings contain only pack-local keys. Historical drafts retain the binding
sets specified by their own content.
