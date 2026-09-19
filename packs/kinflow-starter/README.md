# kinflow-starter

`kinflow-starter 1.0.0` is the approved stable Spine pack, promoted from draft 10
without definition or compatibility changes. Drafts 1 through 10 remain
byte-for-byte unchanged and are not installable. Released bytes are immutable;
future changes require a new version. Installation still requires an explicit
owner, target, selection, and exact plan approval.

Stable `1.0.1` is prepared from compatibility-only `1.0.1-draft.1`, adding
Spine `0.6.0` without changing any definition or reminder. Publication remains
pending exact-commit qualification and approval. The draft is preserved and
is not apply-eligible. `1.0.0` still supports only `0.3.0` and `0.5.0` and MUST
NOT be edited to bypass that allowlist. Installer `0.3.0` is required for the
new runtime; it is also awaiting publication approval.

## Release contents

Versions 1.0.0 and 1.0.1 contain these 52 archetypes, each with its own same-named `_standard`
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
in [the pack specification](../../specs/kinflow-starter.md). The stable
manifests are
`packs/kinflow-starter/kinflow-starter.1.0.0.json` and
`packs/kinflow-starter/kinflow-starter.1.0.1.json`. They contain no
owner, subject, group, route, delivery target, generated Spine ID, timestamp,
receipt, credential, or environment-specific data.

The recorded Whetstone audit applies to the medical-only predecessor, not to
the entire expanded pack; release validation must not be described as a new
full-content Whetstone audit.

## Distribution and compatibility

The pack is distributed separately from the installer under GitHub tag
`pack-kinflow-starter-v1.0.0`, with the manifest and `SHA256SUMS` as assets.
It declares exactly Spine `0.3.0` and `0.5.0`; use installer `0.2.0` for `0.5.0`
/ schema 15. See [release finalization](../../docs/release-finalization.md) for
checksums, qualification limits, and staging prerequisites. A release does not
create items, recurrence, owners, delivery routes, or an installation.

The prepared successor proposes separate tag `pack-kinflow-starter-v1.0.1`
with its JSON manifest and its own `SHA256SUMS`. Its exact runtime allowlist is
`0.3.0`, `0.5.0`, `0.6.0`. See
[0.6.0 release finalization](../../docs/spine-0.6.0-release-finalization.md).
