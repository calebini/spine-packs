# kinflow-flight

[Version 1.0.0-draft.1](kinflow-flight.1.0.0-draft.1.json) is the first draft of
the standalone flight pack for Spine 0.12.0, ledger schema 20. The installer can
plan it with `draft_posture=inspect_only`. The plan is ineligible for apply.

`flight` is a scheduled departure. Its default profile is
`flight_details_standard`. Missing values are omitted when Spine renders an
eligible reminder. Rendering the details requires the corresponding Spine
disclosure permissions. The pack also includes `flight_standard` for callers
that explicitly choose the ordinary profile.

| Before departure | Presentation in the default profile | Late-delivery window |
| --- | --- | --- |
| 7 days | Flight number and airport labels | 24 hours |
| 24 hours | Ordinary reminder | 6 hours |
| 4 hours | Flight number and airport labels | 1 hour |
| 1 hour | Departure gate, when available | 15 minutes |

All six fields are optional. Flight number and destination support exact
facet queries. Destination queries match the referenced Spine location ID.
Arrival timestamp and timezone are informational text excluded from both
rendering definitions.

Use `selection.mode=all` in a v2 install request to inspect the complete
eight-object pack, including `flight_standard`. Selecting only the `flight`
archetype includes the seven objects in its default configuration. See the
[content design](../../specs/flight-content-proposal.md) for exact field,
rendering and disclosure semantics.
