# Kinflow appointments

[Draft 1](../packs/kinflow-appointments/kinflow-appointments.1.0.0-draft.1.json)
targets exact Spine `3e65ef0de9e73b62047a0f6328731db08ca91023` (0.12.0,
ledger schema 20) through `spine.pack-manifest.v2`.

`appointment` is an event-only archetype for scheduled in-person
administrative and other nonmedical appointments. The event start is the
reminder anchor. The venue can be recorded as the event's primary location.

The draft MUST bind `appointment_standard` as the archetype default. Its
template keys, elapsed offsets and late-delivery windows MUST match
`medical_appointment_standard` from
[kinflow-starter 1.0.1](../packs/kinflow-starter/kinflow-starter.1.0.1.json).
Every template MUST use ordinary rendering.

| Before the event start | Late-delivery window |
| --- | --- |
| 7 days | 24 hours |
| 24 hours | 6 hours |
| 2 hours | 1 hour |
| 30 minutes | 15 minutes |

The draft declares the archetype, its profile and the default binding intent.
Planning requires `draft_posture=inspect_only`. Installation requires a
released pack version.

The [stable 1.0.0 candidate](../packs/kinflow-appointments/kinflow-appointments.1.0.0.json)
has the same definitions and compatibility as draft 1.
