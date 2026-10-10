# Pinned Spine source excerpts

Source: `01ebce7b0c5fb9234e0eab55daca96b01c5cb6a7`. Verbatim numbered
excerpts for bounded planning review, not a complete specification mirror.
Hashes below are for the complete original files, not individual excerpts.

## specs/archetype-facets.md

SHA-256: `6f5268c62c955c285e743f16a01560475ba99ac4df30c9e6c50b3433dc3f09c6`

Lines 38–127:

```text
38: ## 2. Model and invariants
39:
40: ### 2.1 Schema roots and revisions
41:
42: A schema root has an immutable `facet_schema_id`, owner scope, owner-local
43: `schema_key`, current revision pointer, and status `active` or `retired`.
44: Owner kinds follow existing catalog scopes: system, subject, subject_group. There is
45: no built-in domain taxonomy. Keys are lowercase ASCII `[a-z][a-z0-9_]{0,63}`.
46: The pair (owner scope, schema_key) is unique, including retired roots; keys are not
47: recycled. Retirement is terminal in this slice.
48:
49: A revision has `facet_schema_revision_id`, schema root ID, positive decimal-string
50: `revision_number`, `display_name`, nullable `description`, compatible item types
51: (nonempty subset of event/task), closed field declarations, and `definition_hash`.
52: The exact revision owns validation and query declarations. Revisions are immutable;
53: even description changes publish a new revision. The current pointer is a catalog
54: convenience, never a value-validation input. `flight_details.v1` in prose means the
55: first published definition, not a globally reserved key or a floating lookup alias.
56:
57: ### 2.2 Archetype bindings
58:
59: An active binding associates an exact archetype root with an exact schema revision
60: and a `facet_key`. At most one active binding exists per (archetype ID, facet_key).
61: The archetype and schema must have the same catalog owner in v1. Publishing a schema
62: revision does not move bindings. Explicit binding set supersedes the previous binding;
63: remove retires it. Compare the expected prior binding ID (null for first creation).
64: Bindings are optional eligibility declarations, not required data, defaults, or
65: automatic facet creation. Schema and archetype compatible item types must intersect.
66:
67: ### 2.3 Item values
68:
69: A complete facet snapshot belongs to `(item_id, item_version)` and contains at most
70: eight entries, unique by `facet_key`. Each entry records the exact schema revision,
71: binding ID, archetype assignment evidence, canonical values, and source authoring
72: receipt. Existing items begin with an empty snapshot. Absence differs from an empty
73: object. Field nulls are forbidden; remove an optional field by omitting it in a full
74: replacement. Missing required fields fail validation.
75:
76: Unrelated item edits copy the snapshot forward exactly. Catalog edits, retirement,
77: or binding changes do not rewrite it. Historical values remain decodable using their
78: stored immutable schema revision. A value replacement requires the current active
79: binding and active schema/archetype, including when upgrading an old revision.
80: An unchanged retained entry need not requalify against current catalog status.
81:
82: Every fresh `set`, including a same-value no-op, MUST require the target item's
83: concrete `item_type` in both the item's pinned assigned archetype revision's and
84: the selected pinned facet-schema revision's `compatible_item_types`. The binding's
85: nonempty intersection test alone is insufficient: an event/task archetype can bind
86: an event-only schema, but a task cannot set that facet. After active binding/catalog
87: eligibility and before value validation, incompatibility fails `wrong_item_type`,
88: `field=item_id` (CLI exit 2; admitted web domain_failure, HTTP 422). Remove-only
89: changes, unchanged copy-forward and compatible receipt replay do not re-run this
90: fresh-set test; they do not author a new value against a new schema revision.
91:
92: Changing or clearing an item's archetype while retaining a nonempty facet snapshot
93: fails `facet_archetype_conflict`; callers must explicitly clear facets first in this
94: initial slice. No command silently deletes data. Removing facets remains possible
95: after catalog retirement. Facets apply to the series item, not individual recurrence
96: occurrences; per-occurrence values are out of scope.
97:
98: ## 3. Closed type system and normalization
99:
100: V1 uses a small declarative field language, not arbitrary executable JSON Schema.
101: Each field has a key in the same ASCII key domain, a boolean `required`, and one type:
102:
103: | Type | Value and validation |
104: | --- | --- |
105: | `text` | Nonempty NFC string, no control characters; declared `max_length` 1–1024 Unicode code points. Whitespace is preserved, not trimmed. |
106: | `enum` | One exact string from 1–64 unique NFC choices, each 1–128 code points. Case-sensitive. |
107: | `boolean` | JSON true/false, without string/number coercion. |
108: | `integer` | Canonical signed decimal string: either `0` or an optional ASCII minus sign followed by an ASCII digit `1`–`9` and zero or more ASCII digits `0`–`9`. Leading zeros, plus signs and negative zero are forbidden. Inclusive declared min/max use the same encoding and stay within signed 64-bit range. |
109: | `date` | Valid proleptic Gregorian `YYYY-MM-DD`, years 0001–9999; descriptive only, never a temporal anchor. |
110: | `reference` | Existing Spine `subject` or `location` ID; declaration fixes the target kind. No polymorphic object or arbitrary URI. |
111:
112: Each declaration also has `queryable` (boolean, default false). Unknown schema keys,
113: field keys, types, coercions, floats, nulls, nested objects, arrays of values, regexes,
114: formulas, computed defaults, remote references and scripts are rejected. Definitions
115: have 1–32 fields. Full normalized definition is at most 32 KiB UTF-8 canonical JSON;
116: one values object at most 16 KiB; all item values together at most 64 KiB. Text is
117: normalized to NFC before validation/hashing; enum choices normalize then deduplicate,
118: with duplicate declarations rejected rather than silently collapsed.
119:
120: Definition normalization fills queryable=false, orders fields by key, enum choices
121: lexicographically by Unicode scalar value, and compatible types lexicographically.
122: Integers and dates are validated, not rewritten from permissive input. Hashes use
123: existing `spine.canonical-json.v1` and SHA-256. `definition_hash` covers a preimage
124: with `derivation_version=spine.facet-definition.v1` and the entire normalized revision
125: definition excluding generated IDs, revision number and hash. Catalog owner is a
126: root fact, not part of the portable definition hash.
127:
```

Lines 179–231:

```text
179: ## 4. Proposed command surfaces
180:
181: All mutation requests use the owning proposed family, `command_id`, actor and explicit
182: action timestamp under the existing common command contract. Fresh requests require
183: the expected target revision/version. Read requests do not write receipts. Exact JSON
184: schemas and field spelling of common envelopes are now recorded in Section 10;
185: the remaining implementation gates still apply.
186:
187: | Command | Additional request facts | Terminal effects |
188: | --- | --- | --- |
189: | `facet_schema.create` | owner, schema_key, complete definition | `facet_schema_created` |
190: | `facet_schema.publish` | root ID, expected current revision ID, complete definition | `facet_schema_published`, `facet_schema_publish_noop` |
191: | `facet_schema.retire` | root ID, expected current revision ID | `facet_schema_retired`, `facet_schema_retire_noop` |
192: | `facet_schema.show` | root ID; optional exact revision ID | Complete root/revision readback |
193: | `facet_schema.list` | one explicit owner, status filter, limit/cursor | Bounded catalog page |
194: | `item_archetype.facet_binding.set` | archetype ID, facet_key, exact schema revision ID, expected binding ID | `facet_binding_set`, `facet_binding_set_noop` |
195: | `item_archetype.facet_binding.remove` | archetype ID, facet_key, expected binding ID | `facet_binding_removed`, `facet_binding_remove_noop` |
196: | `item_archetype.facet_binding.list` | archetype ID, limit/cursor | Binding page |
197: | `item.facets.update` | item ID, expected item version, changes | `item_facets_updated`, `item_facets_update_noop` |
198: | `item.facets.show` | item ID; optional exact item version | Complete pinned facet snapshot |
199: | `item.facets.query` | owner, exact schema revision ID, field, equality value, limit/cursor | Bounded matching item IDs/versions |
200:
201: `changes` contains 1–8 operations, sorted by facet_key for normalization; duplicate
202: keys fail. Each operation is `set` with facet_key, expected active binding ID, exact
203: schema revision ID and complete `values`, or `remove` with facet_key. There is no
204: merge/upsert of individual fields. All changes commit atomically in one new item
205: version. A structurally equal normalized final snapshot is a no-op; existing source
206: provenance is retained. Removing an absent key is a no-op. Same-value sets still
207: validate binding, schema and references on a fresh command. Catalog create collisions
208: are conflicts, not implicit overwrite or revival.
209:
210: Success receipts include command/receipt IDs, effect, changed, affected root/revision
211: or item IDs, prior/resulting versions, and sorted changed facet keys. Compatible
212: same-command replay returns recorded stable identities with `replayed=true` and
213: `changed=false`, rather than producing new rows (Section 10.2).
214: Common replay semantics apply before fresh version checks, but never bypass current
215: disclosure authorization in a permission-enforced adapter. Same ID/different normalized
216: semantic request fails `semantic_conflict`. Failed validation changes no state.
217:
218: Validation precedence: envelope/types/bounds; adapter admission; the private receipt
219: lookup and authorized replay branch in Section 6.2; for a fresh command, target/nested
220: authority and visibility/existence; expected versions; active binding/catalog eligibility
221: and concrete item-type compatibility; definition and value validation; reference access;
222: final snapshot limits; transaction. Reference authority is resolved before fresh domain
223: checks; reference lifecycle/value validation remains in the reference-access phase.
224: Inside the write transaction recheck versions and authority before committing.
225: Public errors do not reveal foreign target existence. Proposed domain reasons include
226: `facet_schema_invalid`, `facet_value_invalid`, `facet_binding_conflict`,
227: `facet_archetype_conflict`, `facet_schema_retired`, and `facet_reference_unavailable`;
228: use existing stale/conflict/permission/capacity envelopes where applicable. Field
229: errors carry paths, never echo private values. Machine error mapping is an explicit
230: contract-codification gate, not permission to improvise runtime strings.
231:
```

Lines 614–704:

```text
614: ### 10.1 Wire choices
615:
616: The canonical command is supplied by the transport route, not duplicated inside its
617: request. Each request requires the exact owning `contract_version`. Writes require
618: `command_id`, `actor_subject_id`, `action_timestamp_utc` (whole-second UTC `Z` form).
619: Requests are closed: unknown properties fail. Read requests carry no write identity.
620: IDs use the existing nonempty-string ID domain; generated IDs must additionally obey
621: Section 3.1, as checked by identity vectors rather than invented by a caller.
622:
623: Definitions are passed as `definition`, with `fields` an array of declarations using
624: `key`, `type`, `required`, optional `queryable`, and type-specific properties.
625: `max_length`, integer `min`/`max`, revision/item versions and page limits are canonical
626: decimal strings, not JSON numbers. Integer bounds are both required. Display metadata
627: uses the existing catalog lengths: display_name 1–160 code points, description null
628: or 1–2000 code points. NFC normalization precedes length and byte checks. Text controls
629: mean U+0000–U+001F and U+007F–U+009F; unpaired surrogates are rejected everywhere.
630: The exact definition preimage is
631: `{derivation_version: "spine.facet-definition.v1", definition: <normalized definition>}`.
632: The 32 KiB definition bound measures that normalized definition, not its enclosing
633: hash preimage. The 64 KiB values bound measures a canonical object mapping each
634: facet_key to its values object; per-entry provenance/definitions are not included.
635: Each individual values object remains limited to 16 KiB.
636:
637: Publish/retire use `expected_current_revision_id`. Binding set/remove require
638: `expected_binding_id`, including explicit null for no active binding. A missing active
639: binding with a non-null expectation is a conflict, not the absent-remove no-op.
640: Item updates use `expected_item_version`; optional historical read selection uses
641: `item_version`. A `set` requires `expected_binding_id` non-null; its values are a full
642: replacement. Duplicate declaration/change/entry keys are semantic errors, even when
643: the array elements differ structurally. Arbitrary scalar strings in the envelope are
644: not authorization to bypass the exact pinned field type and declaration constraints.
645:
646: ### 10.2 Success, failure and readback
647:
648: Successes contain `response_contract` equal to the command's owning family. Every
649: write response includes `command_id`, `command_receipt_id`, the closed `effect`,
650: `changed` and `replayed`. Fresh outcomes use `replayed=false`: changed writes include
651: `audit_id`, while fresh no-ops forbid it. Compatible replay uses `replayed=true` and
652: `changed=false`, creates no rows, and returns the stored receipt ID, effect and stable
653: result identities. An original changed effect requires its stored `audit_id`; an
654: original no-op effect forbids that field. On replay this is historical audit evidence,
655: never evidence of a newly performed write. The effect names the stored receipt's
656: outcome; it does not override the current invocation's changed=false result.
657:
658: All six writes support compatible replay. `facet_schema.create` replays only its
659: changed receipt; create collisions remain conflicts and there is no create no-op
660: receipt. Publish, retire, binding set, binding remove and item facet update may replay
661: their changed or no-op receipts. Prior/resulting version and binding facts stay exactly
662: as recorded, even if the target has since advanced; replay is not a current-state read.
663: For `item.facets.update`, replay returns
664: `changed_facet_keys=[]` and `reconciliation_performed=false`, regardless of the
665: original values of those two invocation-activity fields. It neither reconciles work
666: nor advances a version. `replayed` and the activity-field substitutions are response
667: projection facts only: they do not rewrite the receipt, semantic hash, stored effect,
668: or command-derived identities. Section 4's current disclosure checks still apply.
669:
670: Catalog receipts report `prior_revision_id`, `facet_schema_revision_id` and
671: `revision_number`; create has prior=null and number=1. Publish increments only on
672: change; retire and no-op preserve the revision. Binding set reports prior/resulting
673: IDs and schema revision. Remove reports the same retired binding ID as prior/result;
674: the absent-remove no-op reports both IDs as null. Item receipts report prior/resulting
675: item versions and sorted `changed_facet_keys` (empty on no-op or replay). Fresh changed
676: versions advance by one; replay preserves the original version pair.
677: `reconciliation_performed` reports whether committed work reconciliation ran on this invocation;
678: no-op, replay and dry-run require false. The sample changed receipt is for an item with no policies or
679: work and uses false. Section 5 defines verified retention and the exact true/false rule;
680: the boolean is not evidence of delivery or a count of cancelled/created work.
681:
682: Schema show returns a `root` and selected immutable `revision`; the selected revision
683: must belong to that root, but can differ from its current pointer. Stored definitions
684: are fully normalized, including explicit queryable=false. Item show returns sorted
685: `entries`; each contains the pinned schema revision/definition/hash, facet binding ID,
686: `archetype` assignment evidence (root/revision, selection_source and source_ref when
687: present), values, `source_command_receipt_id`, and `references` sorted by field key.
688: Reference state contains exactly one entry for every reference-valued field present.
689: Its ID/kind must agree with the pinned definition and value. An unreadable reference
690: denies the whole result; inactive but readable subject references are returned as
691: inactive. Existing readable location references always return status=active under
692: Section 6; no location-status column is required or inferred.
693: An empty snapshot returns entries=[], not null or an omitted field.
694:
695: Handler failures use the existing ok/command/error envelope. The proposed facet
696: domain reasons in Section 4 are carried as `error.code`; exact CLI exit mappings are
697: in the draft registry. Definition/value errors use exit 2, binding/archetype conflicts
698: 6, retired-schema use 2, and missing/unreadable references or inactive subjects uniformly 4 with
699: `facet_reference_unavailable`. Paths identify fields but never echo private values.
700: Admission/permission and operational-capacity envelopes remain owned by their adapters;
701: the facet handler schema does not replace or freeze them. Section 6.1 defines resolver
702: mappings, admission ordering and capacity wrappers. Fixture error
703: messages are illustrative safe prose, not byte-exact public message constants.
704:
```

Lines 742–821:

```text
742: ### 10.3 Pagination and validation limits
743:
744: Catalog list defaults status=active and limit=25; explicit status selects active or
745: retired. Binding list returns only active bindings. Query returns current matching
746: item IDs/versions. All pages include the accepted decimal-string limit, `has_more`
747: and `next_cursor`; has_more=false requires null, true requires a nonempty opaque
748: cursor at most 4096 characters. Returned collection length cannot exceed limit.
749: Root IDs, facet keys and item IDs respectively determine the existing total order.
750:
751: Section 11 and its machine companion specify token encoding, authenticated binding,
752: snapshot identity, expiry and access context. No fixture with an arbitrary token proves pagination
753: security or freshness. Likewise, JSON Schema checks structure, not NFC, declared-field
754: validation, hash correctness, foreign-key visibility, byte ceilings or transactional
755: invariants. Test-only pure oracles cover selected semantic vectors; no application
756: validator, database migration, index or command handler is introduced by this bundle.
757:
758: ## 11. Authenticated facet pagination v1
759:
760: `contracts/archetype-facet-integration.v1.json` and
761: `contracts/schemas/archetype-facet-cursor.schema.json` define the dedicated
762: `spine.facet-cursor.v1` continuation. It does not extend or replace either existing
763: trusted-web cursor family. The three paginated commands are facet_schema.list,
764: item_archetype.facet_binding.list and item.facets.query. Show is never paginated.
765:
766: ### 11.1 Bytes, key and context
767:
768: Token: `fc1.<base64url(payload)>.<base64url(mac)>`, unpadded canonical base64url,
769: at most 4096 ASCII bytes. Payload is closed canonical Spine JSON UTF-8 per the cursor
770: schema. MAC is HMAC-SHA256 with the preimage `ASCII("spine.facet-cursor.v1")`, one NUL
771: byte, then the exact payload bytes. Reject wrong version, padding, noncanonical
772: base64url, duplicate JSON keys, unknown fields, noncanonical JSON, invalid schema or
773: MAC with invalid_request/field=cursor. Verify MAC with constant-time comparison before
774: interpreting payload fields. Never log token contents or signature diagnostics.
775:
776: Use a separately provisioned deployment secret of at least 32 random bytes per ledger,
777: not a model/request supplied key or the public vector key. Reads never create a key,
778: receipt or cursor cache. Trusted-local CLI receives key and context through protected
779: operator configuration; web receives them through service configuration. Missing config
780: fails preflight for paginated commands, including first pages, rather than issuing unsigned
781: cursors. This is configuration, not executor authentication. Provision a persistent random
782: `cursor_ledger_id` and `cursor_generation` with the key outside the ledger; use distinct
783: values for copies/clones and rotate generation after restore. These config IDs are not
784: canonical coordination IDs. Rotation invalidates outstanding cursors. No new DB columns.
785:
786: `context_hash` is a keyed digest of the closed object containing `mode`,
787: `cursor_ledger_id`, `cursor_generation`, and `principal`. For trusted_local, principal
788: is `{os_uid: <canonical decimal string>}`; full-scope local users still do not assert a
789: web account. For permission_enforced, principal is the exact identity mapping from
790: `contracts/trusted-web-read-cursor.v2.json` (ledger/realm/recovery, account/subject/
791: binding revisions, selection ID and access_epoch). Full-scope single-operator web
792: remains permission_enforced for identity binding; its access proof records that
793: deployment mode. No caller-controlled actor field substitutes for this context.
794:
795: For all three digest fields below, use lowercase hex HMAC-SHA256 over canonical JSON
796: of `{contract_version: <domain>, value: <specified object>}` with the same key.
797: Domains are `spine.facet-cursor-context.v1`, `spine.facet-cursor-access.v1`, and
798: `spine.facet-cursor-source.v1`; signatures retain their separate domain above.
799: Keying prevents a cursor digest becoming an oracle for low-entropy protected facts.
800:
801: ### 11.2 Query, source and access binding
802:
803: `query_hash` is ordinary lowercase SHA-256 over canonical JSON of
804: `{contract_version:"spine.facet-query.v1", command:<canonical command>, request:<normalized request>}`.
805: The request excludes only cursor, includes contract_version and limit (default 25),
806: and fills list status=active. NFC/type normalization follows the pinned schema;
807: owner discriminators and exact schema/archetype IDs are retained. Changing limit,
808: predicate, owner, revision, status or command mid-pagination is invalid_request.
809: Bind this digest and command in every payload. Do not accept a token from another route.
810:
811: Recompute the complete bounded authorized candidate set on each page in one snapshot,
812: not only the page after last_key. Use indexed enumeration plus LIMIT 101; more than 100
813: candidates or resolved resources fails capacity before returning any page. This is a
814: v1 total-candidate ceiling, not just a page limit. Do not silently cap or paginate an
815: incomplete set. Candidate enumeration includes nonmatching items/roots, so a later
816: matching value or newly visible candidate changes the snapshot. No global JSON scan.
817:
818: `source_snapshot_hash` covers a closed `{command, query_hash, facts}` object, with
819: facts exactly as follows, ordered by the specified primary key:
820:
821: - Schema list: facts is `{roots: [...]}` containing all authorized roots in the named owner (before status filter), each
```

## specs/notification-rendering-definitions.md

SHA-256: `f7ec98452f90ca55f78e661a61ff2c036fda84f4931884c0c7f637c076f899a7`

Lines 77–126:

```text
77: ## 3. Logical catalog
78:
79: ### 3.1 Definition root and revision
80:
81: A `notification_rendering_definition` root has an immutable ID, immutable owner
82: (`system|subject|subject_group` with the corresponding owner ID), owner-local key,
83: `active|retired` status, current revision pointer, and creation/retirement provenance.
84: Owner plus key is unique even after retirement. System definitions follow existing
85: read-only system-catalog rules; ordinary operators cannot create them.
86:
87: Each immutable revision contains its root ID, contiguous revision number, display
88: name, nullable description, supported item types (`event`, `task`, or both), a pinned
89: base-renderer contract/profile, ordered field selections and a canonical content hash.
90: Display metadata is revisioned in this proposal; there is no independent mutable
91: metadata operation in the first slice. Section 13 defines IDs, revision preimages
92: and encodings; example strings are not an alternative derivation rule.
93:
94: Publishing never modifies a prior revision. Retiring a root prevents fresh selection
95: or application; historical reads and decoding remain available. Existing policies
96: retain their exact selection. Retirement is not an emergency disclosure revocation;
97: Section 8 separates those meanings.
98:
99: ### 3.2 Field selection
100:
101: Each selection has a unique `selection_key`, `facet_key`, exact
102: `facet_schema_revision_id`, declared `field_key`, a literal display `label`, and
103: `projection=value|location_label`. Projection must agree with the declared field type.
104: Array order is presentation order and hash-bearing. Duplicate selections of the same
105: facet/schema/field are invalid. There is no wildcard, latest-revision selector, nested
106: lookup or cross-item traversal.
107:
108: The referenced schema revision must exist, belong to the definition's owner in this
109: first slice, and declare the field. An applicable item must actually hold that facet
110: key with that exact schema revision. Matching field names in another revision are
111: not sufficient, even if their apparent types happen to match. A definition may be
112: reused by several archetypes that bind the same schema; it need not embed an archetype ID.
113:
114: First-slice value types are `text`, `enum`, `integer`, `boolean`, and `date`.
115: One reference type is also supported by this proposal: a facet `reference` field
116: whose declared target kind is `location`. It may project only that location's
117: canonical `label`, using Section 6.1. Subject references and other reference kinds,
118: arbitrary referenced fields, nested traversal and raw-ID output are rejected at
119: definition authoring. A location remains a reference, never copied into a text field
120: solely to satisfy this renderer. This restriction does not change which field types
121: facets themselves support.
122:
123: All selected values are optional message detail in this first slice. There is no
124: required-detail mode that cancels an otherwise eligible ordinary reminder. Labels
125: and text are plain data, not instructions, HTML, mention syntax or adapter directives.
126:
```

Lines 417–463:

```text
417: ## 9. Command and pack boundary
418:
419: Reserve the `notification_rendering_definition` command family with create,
420: publish, retire, show and list operations. These names are specified, not registered
421: CLI commands. Writes require exact expected revisions where applicable, command IDs,
422: actor/time attribution, atomic audit and replay receipts. Publish of equivalent
423: normalized content and repeated retirement need deterministic no-op semantics. Reads
424: are bounded, permission-aware on protected transports, and nondurable. Section 13
425: defines envelopes, effects, identity preimages and field limits. Cursor authentication
426: and physical query plans remain implementation gates.
427:
428: The `notification_rendering_disclosure` family defines provision/revoke/show/list
429: operations for reusable disclosure authorizations and their application evidence. They share common
430: audit/replay rules but are distinct from publishing a rendering definition. No current
431: catalog, schedule or permission command accepts these new facts by implication.
432:
433: Versioned profile and direct-policy authoring contracts must express exact selection
434: and explicit clearing to ordinary rendering. Existing closed v1/v2 schemas are not
435: extended silently. The implemented `rendering_profile` constant names an algorithm;
436: it is not interchangeable with a reusable definition ID or a notification profile ID.
437:
438: Packs may supply owner-neutral schema definitions, archetype bindings, rendering
439: definitions and profile references. A future installer resolves pack-local references
440: to exact Spine IDs, provisions dependencies before references, and verifies canonical
441: readback. Each command remains its own transaction unless a separate atomic composite
442: is explicitly contracted. Partial installation is reported and replayed, not described
443: as globally atomic. Missing dependencies block dependent writes, not ordinary reminders.
444: Pack upgrades must detect operator divergence and require explicit reconciliation;
445: they cannot overwrite customizations, grant disclosure, or rewrite live item policies
446: merely because a bundled default changed.
447:
448: ## 10. Flight example and expected behavior
449:
450: A pack could supply a `flight_details` schema with scalar `flight_number` and
451: `terminal`, a flight archetype binding to that schema revision, and a rendering
452: definition selecting those fields in that order. An installed notification profile
453: could select it only for the one-hour template while keeping other reminders ordinary.
454:
455: The reminder still fires solely under its existing offset and late-handling policy.
456: If the current item has `AC872` and `1`, approved detail appears as in Section 4.
457: If terminal is absent, only flight number appears. If the facet was upgraded to a
458: different schema revision, neither field is borrowed from history; ordinary prose
459: remains until an explicit compatible selection is applied. Publishing a new catalog
460: revision changes none of these existing reminders. Reference-valued origin/destination
461: fields may select the referenced location's label under Section 6.1 and the approved
462: location set, without replacing primary location.
463:
```

Lines 538–642:

```text
538: ### 13.1 Versions, normalization and identities
539:
540: Implemented local versions are `spine.notification-rendering-definitions.v1` (catalog),
541: `spine.notification-rendering-disclosures.v1` (authorization management),
542: `spine.notification-rendering-presentation.v1` (authoring/application fragments) and
543: `spine.notification-rendering-details-evidence.v1` (attempt evidence extension).
544: The last two are fragments within the integration's versioned successor envelopes,
545: not new fields accepted by frozen profile, schedule or attempt contracts.
546:
547: Use `spine.canonical-json.v1` from the ontology: sorted object keys, preserved array
548: order, UTF-8, explicit nulls/booleans, decimal-string integers, no JSON numbers and no
549: Unicode normalization. Reject invalid scalar Unicode. IDs/keys are exact strings,
550: not whitespace-trimmed or case-folded. Normalize display names, non-null descriptions
551: and selector labels using ordinary renderer text normalization before validation and
552: hashing. Empty normalized strings and forbidden control characters are invalid.
553: Sort compatible item types, approved/effective selection keys and permitted location
554: IDs lexicographically; reject duplicates rather than silently collapsing them. Preserve
555: selection array order. Projection/type equality, unique selection keys and unique
556: `(facet_key, facet_schema_revision_id, field_key)` tuples are semantic checks beyond
557: JSON Schema. Date validity and canonical integer encoding remain facet authority.
558:
559: For SHA-256 below, hash canonical UTF-8 bytes; digests are lowercase hex. Definition
560: content preimage is exactly `{contract_version, canonical_json_version, revision}`
561: using the catalog version and normalized complete revision. Scope preimage is exactly
562: `{contract_version, canonical_json_version, scope}` using the disclosure version and
563: normalized complete immutable scope. Profile revision is absent from scope; it remains
564: in the application origin. Empty permitted-location arrays are explicit and retained.
565: Each disclosed location must be in that list. Extra fields, wildcards and omitted
566: use-scope branches are invalid.
567:
568: New row IDs use the existing `spine.command-id.v1` derivation, not content IDs. These
569: are the exact row roles, prefixes (identical to role), and request paths:
570:
571: | Creation | Row role/prefix | Request path |
572: |---|---|---|
573: | Definition create | `notification_rendering_definition` | `/definition` |
574: | Definition create or publish | `notification_rendering_definition_revision` | `/revision` |
575: | Disclosure provision | `notification_rendering_disclosure` | `/scope` |
576: | Every fresh terminal write, including no-op | `audit` | `/audit` |
577: | Every fresh terminal write, including no-op | `command_receipt` | `/` |
578:
579: The command-derived preimage contains exactly `derivation_version`, full `command`,
580: `command_id`, `row_role`, `request_path`. The ID is `<prefix>_<digest>`. Revision
581: numbers begin at `"1"`, increment only on changed publish, and are not IDs. Root
582: owner/key remain immutable. A different command cannot recreate an occupied owner/key,
583: even if retired. Identical disclosure scopes may be provisioned under distinct command
584: IDs; they remain explicit records and therefore make automatic resolution ambiguous.
585:
586: ### 13.2 Mutation, read and failure semantics
587:
588: The closed request/response schemas bind commands to their exact contract version.
589: New writes carry command ID, actor and UTC timestamp. Dry run uses the existing
590: `CommandContext.dry_run` flag (default false), not a JSON request field. Receipt
591: comparison uses the full normalized request, plus command and contract version.
592: Dry-run performs validation and deterministic preview,
593: but writes no root, revision, grant, audit or receipt. Preview IDs are predictions,
594: not evidence of persistence; return the same would-be audit/receipt IDs as the commit
595: path, qualified by `dry_run=true`, under the shared command contract. Existing receipt
596: replay precedes freshness and lifecycle
597: validation, after current admission/shape checks. Mismatched command ID reuse is
598: `semantic_conflict`. Replay returns the original record/effect/IDs with
599: `replayed=true, changed=false`; it must not render a fresh catalog snapshot or authorize
600: new disclosure. Dry-run replay follows that same branch with `dry_run=true`.
601: Fresh success atomically persists state, one audit and one receipt. Errors persist none;
602: handler-level dry-run errors carry `dry_run=true` under the existing context contract.
603: Every success and handler-failure response, including show/list, replay and no-op,
604: MUST omit `dry_run` on ordinary execution and include only `dry_run=true` for a
605: dry-run context. `dry_run=false` is not a valid wire response. Read previews retain
606: their ordinary read fields; the marker does not imply a mutation or durable evidence.
607:
608: Publish requires an active root and matching `expected_current_revision_id`; equal
609: normalized content is `rendering_definition_publish_noop`. Retire also requires the
610: exact current revision; repeated retirement returns `rendering_definition_retire_noop`
611: only with the same reason code, otherwise `semantic_conflict`. Revocation similarly
612: requires exact immutable `expected_scope_hash`; repeating the same reason is
613: `rendering_disclosure_revoke_noop`, changing it conflicts. No-op records preserve
614: original creation/publish/retirement/revocation provenance. Revocation does not publish
615: a replacement scope. Provision requires an active, accessible definition and validates
616: all fields, owner/use/destination and allowed references before storing the grant.
617:
618: Fresh validation precedence is: bounded decoding and closed shape/version; admission;
619: receipt replay comparison; target/dependency existence and permission; expected revision
620: or scope hash; lifecycle; selector/type/ownership/scope semantics; normalized no-op
621: comparison; atomic persistence. Missing or inaccessible protected resources do not
622: leak their existence. Invalid definition dependencies/types use
623: `rendering_definition_invalid`; retired fresh use uses `rendering_definition_retired`.
624: No matching authorization uses `rendering_disclosure_unavailable`, multiple matching
625: records use `rendering_disclosure_ambiguous`, and an explicit nonmatching scope uses
626: `rendering_disclosure_scope_mismatch`. At attempt start these expected disclosure
627: failures instead omit optional detail after ordinary admission, never author a grant.
628:
629: Show may address an exact historical definition revision belonging to the named root;
630: omission reads the current revision. Definition list returns current revision records
631: in root-ID order; disclosure list returns grant-ID order, filtered by explicit owner
632: and lifecycle status. Limit is a decimal string from 1 through 100; no counts or total
633: ledger scan. Fetch at most limit+1 indexed candidates, return at most limit, and return
634: a non-null cursor exactly when more exist. Both list responses MUST echo the accepted
635: request `limit` as a required decimal string, including empty and dry-run pages;
636: `len(records) <= int(limit)` is a semantic invariant. JSON Schema enforces the wire
637: domain and absolute 100-row cap, not that cross-field count comparison. Read calls
638: write no receipt or audit.
639: Owner-filtered indexes, consistent permissions, signed cursor payload/version/key
640: management and stale-cursor semantics must be specified before implementing these
641: reads; an opaque string in the schema does not complete that contract.
642:
```

## specs/notification-rendering-integration.md

SHA-256: `2a77e5670ba2174c0727b922f1eaa21fe540456fb14f22058ffab95c3783835f`

Lines 35–125:

```text
35: ## 2. Versioned integration surfaces
36:
37: Reserve these successors. They are not added to compiled runtime declarations,
38: packaged web registries or capabilities by this document.
39:
40: | Surface | Specified successor | Integration delta |
41: | --- | --- | --- |
42: | Profile create/revise/show/list and revision content | `spine.notification-profiles.v2` | Optional template rendering reference, exact revision decoder |
43: | Profile application/readback | `spine.notification-profile-application.v2`, `spine.notification-profile-readback.v2` | Per-policy presentation pins and separate presentation hash |
44: | Schedule create/update | `spine.schedule-create.v3`, `spine.schedule-update.v3` | Application selections and explicit policy-presentation edit branch |
45: | Direct reminder authoring/edit | `spine.notification-schedule-authoring.v2` | Optional direct presentation selection; existing timing identity unchanged |
46: | Full schedule readback | `spine.schedule-show.v2` | Current policy presentation plus v1/v2 persisted attempt rendering |
47: | Attempt rendering envelope | `spine.notification-rendering.v2` | Ordinary base plus approved detail evidence in one final rendering |
48: | Integration capability | `spine.notification-rendering-integration.v1` | Atomic enablement of this complete integration |
49:
50: Existing metadata-only profile updates, archetype/binding commands, recurrence,
51: opportunity/materialization and compact/read-only web contracts retain their exact
52: versions and shapes. An old read projection cannot mislabel v2 rendering as v1:
53: retain its documented summary/redaction policy, or reject an unsupported full-evidence
54: projection. No new fields are injected into the frozen web v1/v2 families.
55:
56: Old authoring requests remain ordinary on fresh creation. When they copy existing
57: policies unchanged, they must preserve their presentation supporting facts. An old
58: whole-plan replacement that would remove or change a selected presentation without
59: expressing that intent MUST fail `unsupported_field`, field `notification_plan`,
60: with no writes and a fixed upgrade-contract diagnostic. It must not silently clear
61: details, auto-resolve a new grant or drop sidecar state. Exact stored receipt replay
62: remains unchanged and must not require today's catalogs to be active.
63:
64: For `notification_profile.revise`, compatible stored receipt replay precedes all
65: fresh-execution checks, including the guard below; incompatible command-ID reuse
66: still fails under the existing replay rules. On fresh execution, perform existing
67: root/lifecycle and expected-current-revision checks first. If the current revision
68: uses the v2 decoder, a `spine.notification-profiles.v1` revise request MUST fail
69: `unsupported_field`, field `revision`, with diagnostic
70: `Use spine.notification-profiles.v2 to revise a v2 profile revision.`
71: This includes v2 revisions whose templates are all ordinary and requests that would
72: otherwise be no-ops. Do not demote to v1, copy pins implicitly, or silently clear them.
73: No revision, pointer, audit or receipt is written by that failure. V1-to-v1 revision
74: remains unchanged; a v2 request may revise a v1 or v2 current revision using the v2
75: normalization/hashes. In v2 complete replacements, omitted template rendering means
76: ordinary as specified below. Historical v1 hashes and compatible replay never change.
77: Metadata-only updates and retirement remain governed by their existing contracts.
78:
79: All writers must understand copy-forward before storage activation, even writers
80: whose public schema cannot author rendering. A runtime without the integration
81: capability must reject the activated schema at bounded preflight. Enclosing schemas,
82: runtime family requirements and release manifests must ship atomically, with old
83: history decoders retained. This is internal historical decoding, not a second model.
84:
85: ## 3. Authoring and application
86:
87: ### 3.1 Profile revisions and complete plans
88:
89: V2 profile templates add `rendering` with the closed union `{kind: ordinary}` or
90: `{kind: definition, definition: <definitionReference>}`. Omission normalizes to
91: ordinary. They never store disclosure IDs, destinations or effective field subsets.
92: The existing definitionReference pins root and exact revision. Definition/profile/
93: schema owner equality and compatibility rules remain logical Section 5.
94:
95: V2 revision and template hashes use new preimages: respectively
96: `{derivation_version: spine.notification-profile-revision-hash.v2, canonical_json_version,
97: revision}` and `{derivation_version: spine.notification-profile-template-hash.v2,
98: canonical_json_version, template}`. `revision` is the complete normalized revision;
99: `template` is a normalized template without its derived hash. Neither rewrites v1
100: hashes. The ordinary effective-policy-set hash still excludes presentation; add a
101: separate `effective_presentation_set_hash` defined in Section 4.
102:
103: V3 schedule `notification_plan` and complete replacement plans add an optional
104: `rendering_applications` array, maximum 32, sorted by `(source_kind, source_key)`.
105: Each entry is exactly `{source_kind, source_key, selection}`: source_kind is
106: `profile_template|custom_addition`; source_key is the existing template/policy key;
107: selection is the existing `authoringSelection` schema. Replaced templates still use
108: `profile_template` as address; composition derives `profile_replacement` as origin.
109: No duplicate address, suppressed/missing address or client-supplied origin is legal.
110:
111: For each surviving profile template whose definition is not ordinary, an application
112: entry is required: it selects that exact definition with explicit effective keys and
113: exact/unique-match authorization, or explicitly chooses ordinary. An alternate
114: definition is allowed only on a named complete template replacement and must pass
115: fresh definition checks. For ordinary templates and custom additions, omission means
116: ordinary, while an explicit entry may opt into a definition with fresh validation.
117: Missing required application is `missing_required_field`; unknown/duplicate address
118: or incompatible template pin is `semantic_conflict`, field `rendering_applications`.
119: A missing grant fails authoring rather than silently switching to ordinary.
120:
121: Suppression, replacements and additions compose first; normalize and reject duplicate
122: ordinary policies before applying presentation. Two identical timing/target/recipient
123: policies with different renderings are still duplicates, not two sends. Full-plan
124: replacement is still full replacement, not a new patch/upsert interpretation.
125:
```

Lines 160–214:

```text
160: ### 3.3 Fresh trusted-local creation and explicit adoption
161:
162: This slice does not add an owner input or ownership establishment to the trusted-local
163: schedule-create command. Fresh trusted-local creation is therefore **ordinary-only**:
164: a definition selection fails `rendering_disclosure_unavailable` before any durable
165: item, policy, work, audit or receipt commit. A profile containing definition pins may
166: still be used at creation, but every surviving pinned template must have an explicit
167: ordinary application entry under Section 3.1. Never infer an owner from that profile.
168:
169: `materialization=none` suppresses only the invoking command's work creation. It is
170: not a scheduler hold. Automatic planning can materialize missing actionable work for
171: the committed active policies regardless of pending ownership adoption or presentation
172: setup. Without an operational exclusion, an ordinary reminder may start between any
173: two setup steps, including for a reminder already due within its late-delivery grace.
174:
175: If details must be configured before any reminder can start, the operator MUST establish
176: and verify an operational exclusion of concurrent materialization **before creation**
177: and retain it until the presentation edit commits. This includes automatic schedulers,
178: other explicit materializers and their in-flight operations: for example, quiesce the
179: relevant worker/scheduler processes and exclude other materializing callers. Merely
180: requesting a stop, omitting initial work, or relying on an unadopted owner is not proof
181: of exclusion. Keep the exclusion through step 4 when explicit materialization is to
182: control readiness, allowing only that designated materialization. This is an external
183: operational precondition, not an implicit command lock or new durable hold state.
184: If exclusion cannot be verified or is lost, no details-before-delivery guarantee may
185: be claimed. This amendment authorizes no automatic service stop/restart.
186:
187: The supported detail-enabled setup sequence, subject to that ordering qualification, is:
188:
189: 1. Create the item with ordinary presentations and materialization mode `none` to
190:    avoid work creation by this command; this does not exclude automatic scheduling.
191: 2. Explicitly adopt the created item's exact current version into a subject/group
192:    owner using the existing trusted-local ownership provisioning boundary in
193:    [the web API specification, Section 4](trusted-multi-operator-web-api.md).
194:    Adoption is not ownership transfer and grants no inferred creator entitlement.
195: 3. Read the current item version/policy IDs and apply the Section 3.2 presentation-only
196:    edit against that version, resolving the exact definition/disclosure. This edit
197:    still requires materialization mode `none` and creates no work.
198: 4. When delivery is wanted, invoke the existing bounded notification-work
199:    materialization command explicitly and verify the resulting work/readback.
200:    Release any operational exclusion deliberately after the required setup succeeds.
201:    Normal current-time/late-handling eligibility still applies; setup delay neither
202:    extends grace nor creates a guarantee that an expired opportunity will be delivered.
203:
204: These are separately receipted transactions, not one atomic composite. If adoption
205: or selection fails, the already created item remains ordinary; do not auto-delete it
206: or claim the entire sequence rolled back. If strict ordering was required, do not
207: automatically release the exclusion on failure: the operator must finish setup or
208: explicitly accept ordinary delivery before resuming materialization. Retrying uses
209: each step's own command ID and current-version checks. If ordinary work was already materialized, existing
210: attempt/continuity rules apply; later setup cannot retract an already started send.
211: Protected creation's existing envelope ownership orchestration is not removed, but
212: this amendment neither activates rendering there nor extends its registry. An atomic
213: trusted-local owner-plus-rendering create would require a separate explicit contract.
214:
```

Lines 488–560:

```text
488: ## 8. Catalog reads, indexes and capacity
489:
490: Create `notification_rendering_catalog_state(singleton I PK CHECK=1, generation I)`;
491: initialize to 1. Changed create/publish/retire/provision/revoke increments once per
492: transaction. No-op, replay and reads do not increment. Overflow fails closed. Global
493: generation deliberately invalidates pages across owners; it is not a user-visible count.
494:
495: Required indexes: roots `(owner_kind,owner_subject_id,owner_group_id,status,root_id)`
496: with required owner/status predicates; disclosures likewise ending in
497: disclosure_authorization_id; revisions `(root_id,revision_number)`; fields by revision;
498: policy presentations by `(item_id,item_version,notification_policy_id)` and by grant;
499: template-renderings by definition revision. Root/revision IDs refer to the full column
500: names in Section 5. Add reverse-FK indexes for all reference tables and receipt FKs.
501:
502: `match_hash` hashes exactly `{derivation_version: spine.rendering-disclosure-match.v1,
503: canonical_json_version, item_owner, definition, use_scope, destination}`. These fields
504: come from the normalized scope; fields and permitted locations are intentionally
505: excluded. Index disclosures `(match_hash,status,disclosure_authorization_id)`. Unique
506: resolution inspects at most 101 active candidates; if more than 100 exist, fail capacity,
507: even if an early candidate matched. Under the cap, compare full structural scope,
508: effective-key subset and required authority; zero/multiple matching grants retain
509: existing unavailable/ambiguous errors. Empty facet values do not constrain the allowed
510: location set at authoring; each actual location is checked at attempt time. Exact-ID
511: selection uses a PK lookup and the same semantic checks. Never globally scan grants.
512:
513: List uses binary root/grant keyset order, not OFFSET. Filter owner/lifecycle and
514: authority before page size; no totals. Fetch at most limit+1 authorized candidates.
515: Permission-enforced enumeration must use owner rights or indexed grant candidate
516: unions, not unbounded post-filtering. Up to 101 candidates, 100 returned records,
517: 100 access-proof rows, 4 MiB serialized response, 5 seconds and 100000 SQLite VM
518: steps per read (including fence); lower configured limits win. Exceeding a bound is
519: environment_failure, never a partial successful page. Definitions/scopes have their
520: existing per-record byte bounds. One attempt resolves <=8 selections/unique locations
521: by PK; no catalog discovery at send time. Existing runtime transaction ceilings apply.
522:
523: Reserve `spine.notification-rendering-cursor.v1`, prefix `nrc1`. Token is
524: `nrc1.<key_id>.<base64url(payload)>.<base64url(mac)>`, canonical unpadded base64url.
525: MAC = HMAC-SHA256(key, UTF8(`spine.notification-rendering-cursor.v1`) + NUL +
526: UTF8(key_id) + NUL + canonical payload bytes). Protected key config reuses the facet
527: cursor file lifecycle/permissions and minimum 32-byte secret, but uses a distinct
528: domain; no generated fallback. Max token 4096 bytes, original TTL 900 seconds, fixed
529: expiry across pages. Key retirement, restore-generation change or ledger clone invalidates it.
530:
531: Payload has exactly: contract_version, ledger_instance_id, key_generation, command,
532: query_hash, context_hash, access_hash, catalog_generation, last_id, issued_at_utc,
533: expires_at_utc, access_epoch, access_valid_until_utc. Canonical query is
534: `{owner,status,limit}`. Status is required by both existing closed list contracts:
535: definition lists accept `active|retired`, disclosure lists accept `active|revoked`.
536: Omitted, null or otherwise invalid status fails request validation before cursor
537: processing; there is no unfiltered-list mode or null-status normalization. Use the
538: admitted status enum verbatim. Limit is bound, not adjustable mid-pagination.
539: Hash preimages use the exact
540: objects `{derivation_version,canonical_json_version,<named object>}` with domains
541: `spine.rendering-cursor-query.v1`, `spine.rendering-cursor-context.v1`,
542: `spine.rendering-cursor-access.v1` and keys query, context, access respectively.
543: Context is `{mode,account_id,subject_id,audience,ledger_instance_id}`; trusted-local
544: uses null account/subject and audience `trusted_local_full_scope`. Access is
545: `{access_epoch,valid_until_utc}` from the existing permission resolver;
546: trusted-local uses nulls. Payload access_valid_until_utc is that valid_until_utc,
547: null when no temporal transition exists. It limits expiry to the next temporal access
548: transition. Continuation verifies access_hash against these authenticated payload facts,
549: then recomputes authority at current time, checks current epoch/context and rejects an
550: expired transition bound. It does not compare a fresh evaluation timestamp with the
551: old one. Section 11 and the cursor schemas close token field domains and reference
552: vectors; stateful permission and catalog fences remain runtime obligations.
553:
554: Malformed/MAC/query/expired/source/context mismatch is stale_cursor without payload
555: release; missing key/config or capacity is environment_failure. Revalidate current
556: authority and catalog generation after serialization, before release. First-page
557: source/access change is environment_failure; continuation is stale_cursor. No automatic
558: reconstruction, retry, durable cursor session or read receipt. Concurrent retirement,
559: revocation and access changes must never release a stale page.
560:
```

Lines 668–691:

```text
668: Profile create/revise/show/list v2 use the closed successor schemas. V2 read records
669: project a normalized owner object and selected revision envelope rather than raw SQL
670: joins. revision_contract selects the historical v1 or v2 content decoder; old hashes
671: are never recomputed as v2. V2 normalization preserves existing timing normalization,
672: sorts compatible_item_types and templates by template_key, and inserts explicit
673: ordinary rendering for omission. Hash each template without derived fields first;
674: the complete normalized revision includes those normalized_template_hash values.
675: Catalog IDs, row indexes and timestamps do not enter the revision-content preimage.
676: Profile-list v2 retains the existing 1–500 request limit and a maximum 500-entry
677: response; the separate rendering-definition/disclosure catalog's 100-entry bound
678: does not apply to notification-profile lists.
679:
680: Application v2 is a closed projection of a persisted selected-profile application,
681: not a replacement plan or an instruction to select a profile. It carries explicit
682: application_contract, existing application/profile/revision/binding IDs, selection
683: mode, scope_chain, normalized_profile_revision_hash, suppress_template_keys,
684: replacements, custom_additions, ordinary effective-policy hash,
685: effective_presentation_set_hash and policy
686: mappings ordered by notification_policy_id. Each mapping retains policy_origin and
687: source_key as well as the resolved presentation/hash. No selected profile means null
688: application, including custom-only policies; those policies still expose presentation
689: through ordinary policy projections. Schedule create/update notification_profile is
690: this application projection or null. Full schedule.show uses readback v2 with nullable
691: application, nullable pinned/current revision IDs, and the existing upgrade/divergence
```

## docs/NOTIFICATION_RENDERING_GUIDE.md

SHA-256: `ac62bbad1d786579d109d01d04436df8eb7dbecf7b6ff4bbd33c60d1d70d7e78`

Lines 1–94:

```text
1: # Facet-aware notification rendering
2:
3: This is the trusted-local operator guide for the schema-19 rendering release.
4: Start with ordinary scheduling in [the quickstart](AGENT_QUICKSTART.md); use this
5: guide only when reminders should include explicitly selected facet facts.
6:
7: ## Quick decision
8:
9: - Ordinary reminders need no definition or disclosure configuration. Their wording,
10:   work identity and delivery behavior stay unchanged.
11: - Details such as a flight number or terminal require a rendering definition,
12:   destination-specific disclosure authorization, and a recorded policy presentation.
13: - Full evidence uses `spine.schedule-show.v2`. `--compact` stays the existing short
14:   receipt: it deliberately excludes facet values and disclosure evidence.
15: - This release exposes the new families through the local command surface, **not**
16:   the current web command/facet registries. Existing web reads keep their established
17:   summaries or fail closed when their full old projection cannot represent v2.
18: - No definition, profile, pack or chat membership implicitly approves disclosure.
19:
20: The CLI still requires a concrete ledger path. All examples below are request
21: shapes, not authorization to modify a real ledger or send a message.
22:
23: ## 1. Define what can appear
24:
25: Use `notification_rendering_definition.create` with
26: `contract_version=spine.notification-rendering-definitions.v1`. An owner-scoped
27: definition pins the facet schema revision, field keys, labels and compatible item
28: types. It appends bounded deterministic details to the existing concise reminder;
29: it cannot contain executable templates, network lookups or model instructions.
30:
31: Direct scalar values and explicitly permitted location **labels** are supported.
32: Location references remain references; do not copy addresses into string fields to
33: bypass that model. Location projection never releases an address, coordinates or
34: provider metadata. Canonical facts of referenced locations remain immutable.
35:
36: For request shape and vocabulary, see
37: [definition authoring example](../tests/fixtures/notification_rendering_definitions/contracts/request_definition_create.json)
38: and [the command schemas](../contracts/schemas/notification-rendering-definition-commands.schema.json).
39: Use returned IDs, not fixture IDs, when configuring an actual ledger.
40:
41: Read a root/revision with `notification_rendering_definition.show`. Publish a new
42: immutable revision with `.publish`; retire a root with `.retire`. Publishing does
43: not upgrade existing policy pins. Retirement blocks new selection, but existing
44: reminders retain their selected revision. Retirement is **not** disclosure revocation.
45:
46: ## 2. Record reusable, scoped disclosure
47:
48: Use `notification_rendering_disclosure.provision` with
49: `contract_version=spine.notification-rendering-disclosures.v1`. Record the explicit
50: operator instruction and exact scope: item owner, definition root/revision, approved
51: selection keys, profile or direct-policy use, recipient, delivery target, channel,
52: adapter, destination source, target reference, and permitted location IDs.
53:
54: For example: “Include flight number and terminal for this profile's reminders to
55: this family chat.” This is a reusable configuration, not approval of all fields in
56: the facet, all destinations, future definition revisions, or changes in a chat's
57: audience. Each policy records its resolved authorization and selected keys. An
58: event-specific exception can choose a narrower subset; it cannot broaden the grant.
59:
60: Exact authorization IDs avoid ambiguity. Unique-match resolution succeeds only
61: when exactly one current authorization covers the request; ambiguous or missing
62: matches fail authoring atomically. `.show`/`.list` inspect grants; `.revoke` withdraws
63: one without changing historical attempt evidence. Use a new authorization for a
64: new scope rather than editing an immutable grant.
65:
66: See [the scoped authorization example](../tests/fixtures/notification_rendering_definitions/contracts/request_disclosure_provision.json).
67:
68: ## 3. Apply without confusing presentation with scheduling
69:
70: Select these request families explicitly:
71:
72: | Operation | Request selector |
73: | --- | --- |
74: | Profile create/revise/show/list | `spine.notification-profiles.v2` |
75: | Composite creation | `spine.schedule-create.v3` |
76: | Composite update | `spine.schedule-update.v3` |
77: | Full readback | `spine.schedule-show.v2` |
78: | Direct reminder create/edit | nested `authoring_contract=spine.notification-schedule-authoring.v2` |
79:
80: Profile v2 templates carry a `rendering` pin or explicit ordinary rendering. Applying
81: a profile resolves the actual disclosure authorization on the item policy; the
82: profile itself is not a disclosure grant. Existing v1 revisions and receipts retain
83: their original decoders and hashes. Use v2 full readback for successor revisions;
84: do not silently strip rendering to submit a v1 revision.
85:
86: For a fresh trusted-local item:
87:
88: 1. Create with ordinary presentation and `materialization.mode=none`.
89: 2. Establish the item owner through explicit `web_access.plan`/`web_access.apply`
90:    adoption. Creation does not infer ownership from the actor, route or archetype.
91: 3. Attach/verify facet values and issue a v3 presentation-only update, again with
92:    `materialization.mode=none`, using current policy IDs and target item version.
93: 4. Materialize a deliberate bounded horizon if delivery is wanted; verify evidence.
94:
```

Lines 140–159:

```text
140: file owned by the runtime user or root, with no group/other permissions (normally
141: `0600`), containing:
142:
143: ```json
144: {
145:   "contract_version": "spine.notification-rendering-cursor-config.v1",
146:   "key_id": "rendering-1",
147:   "key_generation": "generation-1",
148:   "ledger_instance_id": "<system.info ledger instance>",
149:   "secret_hex": "<32-64 cryptographically random bytes encoded as lowercase hex>"
150: }
151: ```
152:
153: Generate the secret outside model-authored requests; do not put it in chat, receipts,
154: repository files or logs. Keep filters, status and limit unchanged across pages.
155: Rotation, ledger restore/context changes, catalog/access epoch changes or expiry make
156: old cursors stale. Restart from the first page; do not decode and edit cursor payloads.
157:
158: ## Release and rollback checklist
159:
```

