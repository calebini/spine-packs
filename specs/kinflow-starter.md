# kinflow-starter content

This document is normative for the approved content of `kinflow-starter` under
`spine.pack-manifest.v1`. It does not extend the manifest schema or authorize
installation. General format and authority rules remain in `pack-format.md`,
`overview.md`, `architecture.md`, and `compatibility.md`.

## Draft lineage

`1.0.0-draft.6` is the current draft. It MUST contain exactly these archetypes,
their respective same-named `_standard` profiles, and one local default-binding
intent per archetype:

- `application_deadline`;
- `birthday`;
- `camp_or_program`;
- `check_in_required`;
- `community_event`;
- `dinner_reservation`;
- `document_renewal`;
- `flight`;
- `game_or_competition`;
- `insurance_renewal`;
- `lesson`;
- `license_renewal`;
- `lodging_checkin`;
- `lodging_checkout`;
- `medical_appointment`;
- `packing`;
- `parent_teacher_meeting`;
- `party`;
- `passport_renewal`;
- `payment_due`;
- `performance`;
- `playdate`;
- `registration_deadline`;
- `school_deadline`;
- `school_event`;
- `social_gathering`;
- `subscription_renewal`;
- `tax_deadline`;
- `train_or_bus_trip`;
- `travel_preparation`;
- `travel_transfer`;
- `trip_departure`;
- `visitor_arrival`.

The medical-only `1.0.0-draft.1`, medical-and-lesson `1.0.0-draft.2`, expanded
event `1.0.0-draft.3`, Education-and-Social `1.0.0-draft.4`, Travel
`1.0.0-draft.5`, and their positive fixtures MUST remain byte-for-byte
unchanged as review evidence. Every predecessor definition and binding MUST be
preserved without semantic change in draft 6. Draft 6 MUST retain the exact
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

Draft 6 archetypes, profiles, and bindings MUST use the lexicographic ordering
required by `specs/pack-format.md`. Template ordering is by key, not reminder
time. Historical draft 3 remains unchanged in its earlier canonical order.

## Late-delivery spacing policy

Draft 6 profiles MUST leave a quiet interval before the next scheduled
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

## Travel

Every definition in this section MUST use `intended_status=active`. Event
profiles and task profiles remain archetype-specific even where another
profile contains equivalent template schedules.

The archetypes MUST be exactly:

| Archetype key | Display name | Description | Compatible item types |
| --- | --- | --- | --- |
| `check_in_required` | `Check-in required` | `Required check-in actions with a specific completion deadline.` | `task` |
| `lodging_checkin` | `Lodging check-in` | `Scheduled lodging check-in times.` | `event` |
| `lodging_checkout` | `Lodging checkout` | `Scheduled lodging checkout deadlines.` | `event` |
| `packing` | `Packing` | `Packing tasks completed before a related trip starts.` | `task` |
| `train_or_bus_trip` | `Train or bus trip` | `Scheduled train and bus departures.` | `event` |
| `travel_preparation` | `Travel preparation` | `Travel preparation tasks with a specific completion deadline.` | `task` |
| `travel_transfer` | `Travel transfer` | `Scheduled transfers between travel legs or locations.` | `event` |
| `trip_departure` | `Trip departure` | `Scheduled departures for general or otherwise unspecified trips.` | `event` |

The corresponding profiles MUST be exactly:

| Profile key | Display name | Description | Compatible item types |
| --- | --- | --- | --- |
| `check_in_required_standard` | `Check-in required standard` | `Progressive reminders before a required check-in deadline.` | `task` |
| `lodging_checkin_standard` | `Lodging check-in standard` | `Preparation and arrival reminders for lodging check-in.` | `event` |
| `lodging_checkout_standard` | `Lodging checkout standard` | `Preparation and departure reminders before a lodging checkout deadline.` | `event` |
| `packing_standard` | `Packing standard` | `Advance reminders for packing before a trip starts.` | `task` |
| `train_or_bus_trip_standard` | `Train or bus trip standard` | `Preparation and boarding reminders for a scheduled train or bus trip.` | `event` |
| `travel_preparation_standard` | `Travel preparation standard` | `Progressive reminders for completing travel preparation.` | `task` |
| `travel_transfer_standard` | `Travel transfer standard` | `Preparation and arrival reminders for a scheduled travel transfer.` | `event` |
| `trip_departure_standard` | `Trip departure standard` | `Advance preparation and departure reminders for a trip.` | `event` |

Their templates MUST be exactly:

| Profile | Template key | Basis | Offset | Local time | Grace |
| --- | --- | --- | --- | --- | --- |
| `check_in_required_standard` | `four_hours_before` | `elapsed` | `-14400` seconds | — | `3600` seconds |
| `check_in_required_standard` | `one_hour_before` | `elapsed` | `-3600` seconds | — | `1800` seconds |
| `check_in_required_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `lodging_checkin_standard` | `one_day_before_at_noon` | `calendar_days` | `-1` day | `12:00:00` | `21600` seconds |
| `lodging_checkin_standard` | `seven_days_before_at_noon` | `calendar_days` | `-7` days | `12:00:00` | `86400` seconds |
| `lodging_checkin_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |
| `lodging_checkout_standard` | `one_day_before_at_six_pm` | `calendar_days` | `-1` day | `18:00:00` | `10800` seconds |
| `lodging_checkout_standard` | `one_hour_before` | `elapsed` | `-3600` seconds | — | `1800` seconds |
| `packing_standard` | `one_day_before_at_nine` | `calendar_days` | `-1` day | `09:00:00` | `21600` seconds |
| `packing_standard` | `two_days_before_at_nine` | `calendar_days` | `-2` days | `09:00:00` | `43200` seconds |
| `train_or_bus_trip_standard` | `thirty_minutes_before` | `elapsed` | `-1800` seconds | — | `900` seconds |
| `train_or_bus_trip_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `train_or_bus_trip_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |
| `travel_preparation_standard` | `due_day_at_nine` | `calendar_days` | `0` days | `09:00:00` | `21600` seconds |
| `travel_preparation_standard` | `seven_days_before_at_nine` | `calendar_days` | `-7` days | `09:00:00` | `86400` seconds |
| `travel_preparation_standard` | `two_days_before_at_nine` | `calendar_days` | `-2` days | `09:00:00` | `43200` seconds |
| `travel_transfer_standard` | `thirty_minutes_before` | `elapsed` | `-1800` seconds | — | `900` seconds |
| `travel_transfer_standard` | `twenty_four_hours_before` | `elapsed` | `-86400` seconds | — | `21600` seconds |
| `travel_transfer_standard` | `two_hours_before` | `elapsed` | `-7200` seconds | — | `3600` seconds |
| `trip_departure_standard` | `fifteen_minutes_before` | `elapsed` | `-900` seconds | — | `600` seconds |
| `trip_departure_standard` | `one_day_before_at_noon` | `calendar_days` | `-1` day | `12:00:00` | `21600` seconds |
| `trip_departure_standard` | `seven_days_before_at_noon` | `calendar_days` | `-7` days | `12:00:00` | `86400` seconds |

`train_or_bus_trip` is anchored to its scheduled departure. `trip_departure`
is for a general or otherwise unspecified trip departure when a more specific
travel archetype does not apply; it is not an automatic runtime fallback.
Lodging definitions are anchored to the stated check-in time or checkout
deadline. `travel_transfer` is anchored to the scheduled transfer, connection,
or pickup time.

`travel_preparation` and `check_in_required` are independently scheduled tasks
whose targets are their actual completion deadlines. The check-in profile has
no target-time reminder because notification at the deadline would already be
too late.

`packing` is a task that is normally related to a trip event. When so related,
its deadline MUST equal that trip event's start time. Its profile deliberately
ends with the day-before-at-nine reminder; it has no final elapsed reminder.
Creating the relationship, copying or synchronizing the target, and handling a
changed trip start are Spine-owned item operations. The manifest does not
encode an item relationship or cause a packing task to be created.

The trip-departure profile deliberately uses a fifteen-minute final reminder
instead of a two-hour reminder. Its ten-minute delivery grace remains within
the 75% cap of eleven minutes and fifteen seconds before the departure target.
The checkout evening reminder and all mixed calendar/elapsed profiles are
bounded against their shortest early-target intervals.

## Renewals and administration

Every definition in this section MUST use `intended_status=active`. All
templates use `offset_basis=calendar_days`, inherit timezone facts from the
applicable item target, and resolve at `09:00:00` local time. Profiles remain
archetype-specific even when their cadence repeats another profile.

The archetypes MUST be exactly:

| Archetype key | Display name | Description | Compatible item types |
| --- | --- | --- | --- |
| `application_deadline` | `Application deadline` | `Deadlines for completing and submitting applications.` | `task` |
| `document_renewal` | `Document renewal` | `Renewal tasks for documents without a more specific archetype.` | `task` |
| `insurance_renewal` | `Insurance renewal` | `Scheduled insurance policy renewal occurrences.` | `event` |
| `license_renewal` | `License renewal` | `Tasks to renew licenses by a selected completion deadline.` | `task` |
| `passport_renewal` | `Passport renewal` | `Tasks to renew passports by a selected completion deadline.` | `task` |
| `payment_due` | `Payment due` | `Payment obligations with a specified due date.` | `task` |
| `registration_deadline` | `Registration deadline` | `Deadlines for completing registrations.` | `task` |
| `subscription_renewal` | `Subscription renewal` | `Scheduled subscription renewal occurrences.` | `event` |
| `tax_deadline` | `Tax deadline` | `Tax filing or payment obligations with a specified due date.` | `task` |

The corresponding profiles MUST be exactly:

| Profile key | Display name | Description | Compatible item types |
| --- | --- | --- | --- |
| `application_deadline_standard` | `Application deadline standard` | `Progressive reminders leading up to and on an application deadline.` | `task` |
| `document_renewal_standard` | `Document renewal standard` | `Progressive reminders leading up to and on a document renewal deadline.` | `task` |
| `insurance_renewal_standard` | `Insurance renewal standard` | `Advance reminders before an insurance renewal.` | `event` |
| `license_renewal_standard` | `License renewal standard` | `Progressive reminders leading up to and on a license renewal deadline.` | `task` |
| `passport_renewal_standard` | `Passport renewal standard` | `Long-horizon reminders before a passport renewal deadline.` | `task` |
| `payment_due_standard` | `Payment due standard` | `Progressive reminders leading up to and on a payment due date.` | `task` |
| `registration_deadline_standard` | `Registration deadline standard` | `Progressive reminders leading up to and on a registration deadline.` | `task` |
| `subscription_renewal_standard` | `Subscription renewal standard` | `A single advance reminder before a subscription renewal.` | `event` |
| `tax_deadline_standard` | `Tax deadline standard` | `Progressive reminders leading up to and on a tax deadline.` | `task` |

Their templates MUST be exactly:

| Profile | Template key | Calendar-day offset | Grace |
| --- | --- | --- | --- |
| `application_deadline_standard` | `due_day_at_nine` | `0` | `21600` seconds |
| `application_deadline_standard` | `one_day_before_at_nine` | `-1` | `43200` seconds |
| `application_deadline_standard` | `seven_days_before_at_nine` | `-7` | `86400` seconds |
| `application_deadline_standard` | `thirty_days_before_at_nine` | `-30` | `259200` seconds |
| `document_renewal_standard` | `due_day_at_nine` | `0` | `21600` seconds |
| `document_renewal_standard` | `ninety_days_before_at_nine` | `-90` | `604800` seconds |
| `document_renewal_standard` | `one_day_before_at_nine` | `-1` | `43200` seconds |
| `document_renewal_standard` | `seven_days_before_at_nine` | `-7` | `86400` seconds |
| `document_renewal_standard` | `thirty_days_before_at_nine` | `-30` | `259200` seconds |
| `insurance_renewal_standard` | `one_day_before_at_nine` | `-1` | `21600` seconds |
| `insurance_renewal_standard` | `seven_days_before_at_nine` | `-7` | `86400` seconds |
| `insurance_renewal_standard` | `thirty_days_before_at_nine` | `-30` | `259200` seconds |
| `license_renewal_standard` | `due_day_at_nine` | `0` | `21600` seconds |
| `license_renewal_standard` | `one_day_before_at_nine` | `-1` | `43200` seconds |
| `license_renewal_standard` | `seven_days_before_at_nine` | `-7` | `86400` seconds |
| `license_renewal_standard` | `sixty_days_before_at_nine` | `-60` | `259200` seconds |
| `license_renewal_standard` | `thirty_days_before_at_nine` | `-30` | `259200` seconds |
| `passport_renewal_standard` | `ninety_days_before_at_nine` | `-90` | `604800` seconds |
| `passport_renewal_standard` | `one_hundred_eighty_days_before_at_nine` | `-180` | `604800` seconds |
| `passport_renewal_standard` | `seven_days_before_at_nine` | `-7` | `86400` seconds |
| `passport_renewal_standard` | `thirty_days_before_at_nine` | `-30` | `259200` seconds |
| `passport_renewal_standard` | `three_hundred_sixty_five_days_before_at_nine` | `-365` | `1209600` seconds |
| `passport_renewal_standard` | `two_hundred_seventy_days_before_at_nine` | `-270` | `1209600` seconds |
| `payment_due_standard` | `due_day_at_nine` | `0` | `21600` seconds |
| `payment_due_standard` | `one_day_before_at_nine` | `-1` | `43200` seconds |
| `payment_due_standard` | `seven_days_before_at_nine` | `-7` | `86400` seconds |
| `payment_due_standard` | `three_days_before_at_nine` | `-3` | `43200` seconds |
| `registration_deadline_standard` | `due_day_at_nine` | `0` | `21600` seconds |
| `registration_deadline_standard` | `one_day_before_at_nine` | `-1` | `43200` seconds |
| `registration_deadline_standard` | `seven_days_before_at_nine` | `-7` | `86400` seconds |
| `registration_deadline_standard` | `thirty_days_before_at_nine` | `-30` | `259200` seconds |
| `subscription_renewal_standard` | `three_days_before_at_nine` | `-3` | `86400` seconds |
| `tax_deadline_standard` | `due_day_at_nine` | `0` | `21600` seconds |
| `tax_deadline_standard` | `ninety_days_before_at_nine` | `-90` | `604800` seconds |
| `tax_deadline_standard` | `one_day_before_at_nine` | `-1` | `43200` seconds |
| `tax_deadline_standard` | `seven_days_before_at_nine` | `-7` | `86400` seconds |
| `tax_deadline_standard` | `thirty_days_before_at_nine` | `-30` | `259200` seconds |

`document_renewal` is the general choice when neither passport nor license
semantics fit; it is not an automatic runtime fallback. A passport target is
the operator-selected date by which renewal should be completed, not
necessarily the document's printed expiration date. Issuer processing times,
travel-validity rules, document numbers, jurisdictions, and legal requirements
remain item-, operator-, or external-authority facts.

The passport profile's 365-day and 270-day offsets intentionally use exact
calendar-day counts. They approximate one year and nine months without
claiming calendar-year or calendar-month arithmetic, which v1 does not define.

Subscription renewal deliberately has one reminder, three calendar days
before the event. Insurance renewal deliberately has only the approved
30-day, 7-day, and 1-day reminders. Both are scheduled renewal events rather
than claims that an operator must perform a renewal action.

Due-day-at-nine templates are intended for date-based deadlines. When an
application, payment, registration, license, document, or tax deadline has an
earlier exact time, the operator MUST use an appropriate item-level schedule
rather than rely on a reminder that could resolve after the deadline. Amounts,
accounts, vendors, policy identifiers, tax authorities, filing details, and
payment routes MUST NOT appear in reusable pack content.

## Default bindings

Draft 6 MUST bind every included archetype to its same-named `_standard`
profile using exactly one owner-neutral `archetype_default` intent. These
bindings contain only pack-local keys. Historical drafts retain the binding
sets specified by their own content.
