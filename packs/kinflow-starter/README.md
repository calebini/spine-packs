# kinflow-starter

`kinflow-starter` is a draft Spine pack. Current draft version
`1.0.0-draft.2` is not installable, released, or a publication of `1.0.0`.
The medical-only `1.0.0-draft.1` remains unchanged for review provenance.

## Exact draft contents

The medical slice remains unchanged:

- archetype `medical_appointment`, compatible with `event`;
- notification profile `medical_appointment_standard`, compatible with
  `event`;
- templates `seven_days_before`, `twenty_four_hours_before`,
  `two_hours_before`, and `thirty_minutes_before`, using negative elapsed
  target offsets and positive `deliver_within` grace windows; and
- one owner-neutral `archetype_default` binding intent from
  `medical_appointment` to `medical_appointment_standard`.

The approved lesson slice adds:

- archetype `lesson` for scheduled instruction such as swimming and piano
  lessons, compatible only with `event`;
- profile `lesson_standard`, also compatible only with `event`;
- a 24-hour elapsed reminder with 6-hour positive delivery grace and a 1-hour
  elapsed reminder with 30-minute positive delivery grace; and
- one local `archetype_default` binding from `lesson` to `lesson_standard`.

Recurrence, occurrence timing, and exceptions remain Spine-owned item state;
the profile contains no recurrence rules. Display text is English only, using
the existing unlocalized string fields. Exact content is governed by
[the pack specification](../../specs/kinflow-starter.md).

The current draft manifest is
`packs/kinflow-starter/kinflow-starter.1.0.0-draft.2.json`. It contains no
owner, subject, group, route, delivery target, generated Spine ID, timestamp,
receipt, credential, or environment-specific data.

The recorded Whetstone audit applies to the medical-only predecessor, not to
this expanded draft.

## Candidate future content

The following archetypes remain candidates and have no definitions yet:

- `passport_renewal`
- `game_or_competition`
- `flight`
- `birthday`

Their semantics must not be inferred from their names. The pack remains draft
while these definitions are developed and reviewed before a future `1.0.0`
release.
