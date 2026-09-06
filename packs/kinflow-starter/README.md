# kinflow-starter

`kinflow-starter` is a draft Spine pack. Current draft version
`1.0.0-draft.5` is not installable, released, or a publication of `1.0.0`.
Drafts 1 through 4 remain byte-for-byte unchanged for review provenance.

## Current draft contents

Draft 5 contains these archetypes, each with its own same-named `_standard`
notification profile and one owner-neutral local default-binding intent:

- established slices: `medical_appointment`, `lesson`,
  `game_or_competition`, `flight`, and `birthday`;
- Education and activities: `performance`, `school_event`,
  `parent_teacher_meeting`, `camp_or_program`, and `school_deadline`; and
- Social: `social_gathering`, `party`, `playdate`, `dinner_reservation`,
  `visitor_arrival`, and `community_event`; and
- Travel: `train_or_bus_trip`, `trip_departure`, `lodging_checkin`,
  `lodging_checkout`, `travel_transfer`, `travel_preparation`, `packing`, and
  `check_in_required`.

The task archetypes are `school_deadline`, `travel_preparation`, `packing`, and
`check_in_required`; all others are events. Profiles remain archetype-specific
even when template schedules repeat. Calendar-day templates inherit local
timezone facts from each applicable Spine item; recurrence, occurrence timing,
exact item targets, relationships, and exceptions remain Spine-owned state.

The late-delivery windows follow the pack's 75% spacing rule so an earlier
opportunity expires before the final quarter of the interval leading to the
next reminder. `dinner_reservation` and `visitor_arrival` include deliberate
exact-target reminders with short delivery windows.

Exact definitions, descriptions, schedules, and boundary rules are normative
in [the pack specification](../../specs/kinflow-starter.md). The current draft
manifest is
`packs/kinflow-starter/kinflow-starter.1.0.0-draft.5.json`. It contains no
owner, subject, group, route, delivery target, generated Spine ID, timestamp,
receipt, credential, or environment-specific data.

The recorded Whetstone audit applies to the medical-only predecessor, not to
this expanded draft.

## Candidate future content

`passport_renewal` remains a candidate and has no definition in this draft.
Its semantics must not be inferred from its name. Other catalog sections will
be reviewed before they are added. The pack remains draft while those
definitions are developed and reviewed before a future `1.0.0` release.
