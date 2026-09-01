# kinflow-starter

`kinflow-starter` is a draft Spine pack. Current draft version
`1.0.0-draft.1` is not installable, released, or a publication of `1.0.0`.

## Exact draft contents

The first complete vertical slice contains:

- archetype `medical_appointment`, compatible with `event`;
- notification profile `medical_appointment_standard`, compatible with
  `event`;
- templates `seven_days_before`, `twenty_four_hours_before`,
  `two_hours_before`, and `thirty_minutes_before`, using negative elapsed
  target offsets and positive `deliver_within` grace windows; and
- one owner-neutral `archetype_default` binding intent from
  `medical_appointment` to `medical_appointment_standard`.

The draft manifest is
`packs/kinflow-starter/kinflow-starter.1.0.0-draft.1.json`. It contains no
owner, subject, group, route, delivery target, generated Spine ID, timestamp,
receipt, credential, or environment-specific data.

## Candidate future content

The following archetypes remain candidates and have no definitions yet:

- `lesson`
- `passport_renewal`
- `game_or_competition`
- `flight`
- `birthday`

Their semantics must not be inferred from their names. The pack remains draft
while these definitions are developed and reviewed before a future `1.0.0`
release.
