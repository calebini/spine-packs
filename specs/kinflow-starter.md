# kinflow-starter content

This document is normative for the approved content of `kinflow-starter` under
`spine.pack-manifest.v1`. It does not extend the manifest schema or authorize
installation. General format and authority rules remain in `pack-format.md`,
`overview.md`, `architecture.md`, and `compatibility.md`.

## Draft lineage

`1.0.0-draft.2` is the current draft. It MUST contain exactly the
`medical_appointment` and `lesson` archetypes, their respective standard
profiles, and one local default-binding intent per archetype.

The medical-only artifact `1.0.0-draft.1` and its positive fixture MUST remain
unchanged as review evidence. The medical archetype, profile (including all
template values), and binding in draft 2 MUST equal those in draft 1. Draft 2
MUST retain draft 1's exact compatibility declarations and empty dependencies.
Its new version and lesson content require a newly computed content digest.
Both artifacts remain drafts, not releases or evidence of installation.

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

In draft 2, archetypes and bindings MUST be ordered `lesson` then
`medical_appointment`; profiles MUST be ordered `lesson_standard` then
`medical_appointment_standard`. Template ordering is by key, not reminder time.

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
