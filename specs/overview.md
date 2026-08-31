# Overview

## Status and normative language

This document is normative for the seed stage. The terms **MUST**, **MUST NOT**,
**SHOULD**, and **MAY** describe requirements, even before a machine-readable
pack contract exists.

## Purpose

Spine Packs provides independently versioned collections of reusable Spine
archetype and notification-profile definitions. An operator will eventually be
able to select a compatible pack, review a deterministic plan, apply approved
changes through Spine, and verify the installed result.

Packs MUST be declarative and owner-neutral. They are distribution artifacts,
not running components and not authoritative installation records.

## Ownership and authority

Spine remains the sole authority for:

- installed archetypes;
- installed notification profiles;
- owner and definition bindings;
- operation and installation receipts; and
- ownership of all installed state.

This repository is authoritative only for the source and released content of
the packs it publishes, together with their compatibility declarations. A pack
MUST NOT claim that content is installed. Installation state MUST be observed
from Spine through its public command surface.

Pack releases MUST be immutable. Corrections or semantic changes after release
MUST use a new version.

## Content neutrality

A reusable pack MUST NOT contain owner IDs, delivery targets, subjects, routes,
credentials, secrets, or environment-specific facts. Where installation needs
such values, they MUST come from explicit operator input or already-authoritative
Spine state and MUST NOT be written back into the reusable pack.

## Non-goals

This repository MUST NOT provide:

- a Spine daemon, service, or runtime fork;
- an alternative ledger, receipt authority, or scheduling implementation;
- direct reads from or writes to Spine's database;
- changes to Spine runtime behavior;
- owner-specific deployment configuration; or
- a finalized manifest schema before pack-format review.

An installer may be added after contract review, but its role will be bounded
translation and reconciliation through Spine's existing public commands, not
replacement of Spine authority.
