# kinflow-starter

`kinflow-starter` is a draft Spine pack. Current draft version
`1.0.0-draft.9` is not installable, released, or a publication of `1.0.0`.
Drafts 1 through 8 remain byte-for-byte unchanged for review provenance.

## Current draft contents

Draft 9 contains these archetypes, each with its own same-named `_standard`
notification profile and one owner-neutral local default-binding intent:

- established slices: `medical_appointment`, `lesson`,
  `game_or_competition`, `flight`, and `birthday`;
- Education and activities: `performance`, `school_event`,
  `parent_teacher_meeting`, `camp_or_program`, and `school_deadline`; and
- Social: `social_gathering`, `party`, `playdate`, `dinner_reservation`,
  `visitor_arrival`, and `community_event`; and
- Travel: `train_or_bus_trip`, `trip_departure`, `lodging_checkin`,
  `lodging_checkout`, `travel_transfer`, `travel_preparation`, `packing`, and
  `check_in_required`; and
- Renewals and administration: `document_renewal`, `passport_renewal`,
  `license_renewal`, `registration_deadline`, `application_deadline`,
  `payment_due`, `subscription_renewal`, `insurance_renewal`, and
  `tax_deadline`; and
- Health: `medication_refill`, `prescription_pickup`, and `vaccination_due`;
  and
- Home, vehicle, and logistics: `home_service_appointment`,
  `home_maintenance`, `vehicle_service`, `delivery_window`, `pickup`,
  `dropoff`, and `pet_appointment`; and
- General commitments: `reservation`, `ticketed_event`, `meeting`,
  `interview`, `work_deadline`, `personal_deadline`, `follow_up`, `errand`,
  and `purchase_required`.

The task archetypes are `school_deadline`, `travel_preparation`, `packing`,
`check_in_required`, `home_maintenance`, every Health archetype, every General
commitments archetype except `reservation`, `ticketed_event`, `meeting`, and
`interview`, plus every Renewals and administration archetype except
`subscription_renewal` and `insurance_renewal`; all others are events. Profiles
remain archetype-specific even when template schedules repeat. Calendar-day
templates inherit local timezone facts from each applicable Spine item;
recurrence, occurrence timing, exact item targets, relationships, and
exceptions remain Spine-owned state.

The late-delivery windows follow the pack's 75% spacing rule so an earlier
opportunity expires before the final quarter of the interval leading to the
next reminder. `dinner_reservation` and `visitor_arrival` include deliberate
exact-target reminders with short delivery windows.

Exact definitions, descriptions, schedules, and boundary rules are normative
in [the pack specification](../../specs/kinflow-starter.md). The current draft
manifest is
`packs/kinflow-starter/kinflow-starter.1.0.0-draft.9.json`. It contains no
owner, subject, group, route, delivery target, generated Spine ID, timestamp,
receipt, credential, or environment-specific data.

The recorded Whetstone audit applies to the medical-only predecessor, not to
this expanded draft.

## Candidate future content

The planned archetype sections are now represented. The pack remains draft
while the complete content and contract are reviewed before a future immutable
`1.0.0` release.
