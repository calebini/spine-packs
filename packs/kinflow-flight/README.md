# kinflow-flight

The [1.0.0 release candidate](kinflow-flight.1.0.0.json) carries the
departures and arrivals from draft 2 unchanged, with stable manifest status.
Use the checksum-verified release asset for installation after publication.

[Version 1.0.0-draft.2](kinflow-flight.1.0.0-draft.2.json) adds scheduled
flight arrivals to the departures in
[version 1.0.0-draft.1](kinflow-flight.1.0.0-draft.1.json). Both drafts target
Spine 0.12.0, ledger schema 20, and support read-only planning with
`draft_posture=inspect_only`.

## Flight departure

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

## Flight arrival

`flight_arrival` uses the scheduled landing instant as the event start and
the arrival airport as its primary location. A separate pickup task holds
the meetup due time and the specific meetup location. The arrival facet has
three optional fields: flight number, origin airport, and arrival terminal.
Only flight number is queryable.

| Relative to scheduled landing | Presentation in `flight_arrival_standard` | Late-delivery window |
| --- | --- | --- |
| 24 hours before | Ordinary reminder | 6 hours |
| 1 hour before | Flight number, origin-airport label and terminal when available and authorized | 30 minutes |
| At scheduled landing | The same arrival details when available and authorized | 15 minutes |

In draft 2, select `flight_arrival` to inspect the six arrival objects or
`flight` to inspect the seven objects for the departure default.
`selection.mode=all` includes all 14 objects, including the ordinary
`flight_standard` departure profile. See the
[content specification](../../specs/flight-content-proposal.md) for item
authoring and disclosure semantics.
