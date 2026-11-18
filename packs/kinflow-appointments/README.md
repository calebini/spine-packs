# kinflow-appointments

The [1.0.0 release candidate](kinflow-appointments.1.0.0.json) carries the
appointment bundle from draft 1 unchanged, with stable manifest status.
Use the checksum-verified release asset for installation after publication.

[Version 1.0.0-draft.1](kinflow-appointments.1.0.0-draft.1.json) defines an
event archetype for in-person administrative and other nonmedical appointments.
Its default profile, `appointment_standard`, follows the medical appointment
reminder cadence with ordinary rendering.

Use `draft_posture=inspect_only` to plan against Spine 0.12.0, ledger schema 20.
Selecting `appointment` or the whole pack selects the same three configuration
objects. See the [content spec](../../specs/kinflow-appointments.md) for the
reminder timing and late-delivery windows.
