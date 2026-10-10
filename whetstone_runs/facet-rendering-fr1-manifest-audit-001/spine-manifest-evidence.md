# Exact Spine evidence for the FR-1 manifest review

Source pin: `57cda1c2d5589360ee8efe7155fd20b503034c2a`, runtime `0.9.1`, schema `19`.
These are focused schema fragments and normalization-source excerpts, not a
complete executable public schema closure. No Spine code was imported.
The reviewer may inspect this supplied evidence only; no further checkout access
or external browsing is authorized. All full-source hashes use exact Git blob bytes.

## contracts/schemas/archetype-facet-types.schema.json

Full-source SHA-256: `689163800b0aaa07b87a1fc75a7bea7150bd70f1bcf2fbad901466cdf594dcda`.

```json
{
  "$id": "https://cortext.local/spine/contracts/schemas/archetype-facet-types.schema.json",
  "$defs": {
    "key": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_]{0,63}(?![\\s\\S])"
    },
    "signedInteger": {
      "type": "string",
      "pattern": "^(0|-?[1-9][0-9]*)(?![\\s\\S])",
      "maxLength": 20,
      "$comment": "Semantic validation enforces signed 64-bit range."
    },
    "field": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "max_length"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "text"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            },
            "max_length": {
              "type": "string",
              "pattern": "^([1-9]|[1-9][0-9]{1,2}|10[01][0-9]|102[0-4])(?![\\s\\S])"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "choices"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "enum"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            },
            "choices": {
              "type": "array",
              "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 128
              },
              "minItems": 1,
              "maxItems": 64,
              "uniqueItems": true
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "boolean"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "min",
            "max"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "integer"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            },
            "min": {
              "$ref": "archetype-facet-types.schema.json#/$defs/signedInteger"
            },
            "max": {
              "$ref": "archetype-facet-types.schema.json#/$defs/signedInteger"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "date"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "key",
            "required",
            "type",
            "target_kind"
          ],
          "properties": {
            "key": {
              "$ref": "archetype-facet-types.schema.json#/$defs/key"
            },
            "required": {
              "type": "boolean"
            },
            "type": {
              "const": "reference"
            },
            "queryable": {
              "type": "boolean",
              "default": false
            },
            "target_kind": {
              "enum": [
                "subject",
                "location"
              ]
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "definition": {
      "type": "object",
      "required": [
        "display_name",
        "description",
        "compatible_item_types",
        "fields"
      ],
      "properties": {
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "anyOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 2000
            },
            {
              "type": "null"
            }
          ]
        },
        "compatible_item_types": {
          "type": "array",
          "items": {
            "enum": [
              "event",
              "task"
            ]
          },
          "minItems": 1,
          "maxItems": 2,
          "uniqueItems": true
        },
        "fields": {
          "type": "array",
          "items": {
            "$ref": "archetype-facet-types.schema.json#/$defs/field"
          },
          "minItems": 1,
          "maxItems": 32
        }
      },
      "additionalProperties": false
    },
    "normalizedDefinition": {
      "allOf": [
        {
          "$ref": "#/$defs/definition"
        },
        {
          "properties": {
            "fields": {
              "items": {
                "required": [
                  "queryable"
                ]
              }
            }
          }
        }
      ]
    }
  }
}
```

## contracts/schemas/notification-rendering-definition-types.schema.json

Full-source SHA-256: `3b6ea94ce86bbb06f45c63516700235edba43cd0800ed4be05261fc774848344`.

```json
{
  "$id": "https://cortext.local/spine/contracts/schemas/notification-rendering-definition-types.schema.json",
  "$defs": {
    "selection": {
      "type": "object",
      "required": [
        "selection_key",
        "facet_key",
        "facet_schema_revision_id",
        "field_key",
        "label",
        "projection"
      ],
      "properties": {
        "selection_key": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_-]{0,63}$"
        },
        "facet_key": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_-]{0,63}$"
        },
        "facet_schema_revision_id": {
          "type": "string",
          "minLength": 1,
          "maxLength": 256
        },
        "field_key": {
          "type": "string",
          "pattern": "^[a-z][a-z0-9_-]{0,63}$"
        },
        "label": {
          "type": "string",
          "minLength": 1,
          "maxLength": 40
        },
        "projection": {
          "enum": [
            "value",
            "location_label"
          ]
        }
      },
      "additionalProperties": false
    },
    "revision": {
      "type": "object",
      "required": [
        "display_name",
        "description",
        "compatible_item_types",
        "base_rendering_contract",
        "base_rendering_profile",
        "selections"
      ],
      "properties": {
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 2000
            },
            {
              "type": "null"
            }
          ]
        },
        "compatible_item_types": {
          "type": "array",
          "items": {
            "enum": [
              "event",
              "task"
            ]
          },
          "minItems": 1,
          "maxItems": 2,
          "uniqueItems": true
        },
        "base_rendering_contract": {
          "const": "spine.notification-rendering.v1"
        },
        "base_rendering_profile": {
          "const": "spine.notification-rendering.concise-en-ca.v1"
        },
        "selections": {
          "type": "array",
          "minItems": 1,
          "maxItems": 8,
          "items": {
            "$ref": "notification-rendering-definition-types.schema.json#/$defs/selection"
          }
        }
      },
      "additionalProperties": false
    }
  }
}
```

## contracts/schemas/notification-profile-types-v2.schema.json

Full-source SHA-256: `e1587494d473198b49f16be89e27de12e32df512821d5670f9c8bf48f654f875`.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cortext.local/spine/contracts/schemas/notification-profile-types-v2.schema.json",
  "title": "Spine Notification Profile Types v2 (source only)",
  "$defs": {
    "key": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9_-]{0,63}(?![\\s\\S])"
    },
    "owner": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "owner_kind"
          ],
          "properties": {
            "owner_kind": {
              "const": "system"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "owner_kind",
            "owner_subject_id"
          ],
          "properties": {
            "owner_kind": {
              "const": "subject"
            },
            "owner_subject_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "owner_kind",
            "owner_group_id"
          ],
          "properties": {
            "owner_kind": {
              "const": "subject_group"
            },
            "owner_group_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "itemTypes": {
      "type": "array",
      "minItems": 1,
      "maxItems": 2,
      "uniqueItems": true,
      "items": {
        "enum": [
          "event",
          "task"
        ]
      }
    },
    "archetypeRevision": {
      "type": "object",
      "required": [
        "display_name",
        "description",
        "compatible_item_types"
      ],
      "properties": {
        "display_name": {
          "type": "string",
          "minLength": 1,
          "maxLength": 160
        },
        "description": {
          "oneOf": [
            {
              "type": "string",
              "minLength": 1,
              "maxLength": 2000
            },
            {
              "type": "null"
            }
          ]
        },
        "compatible_item_types": {
          "$ref": "#/$defs/itemTypes"
        }
      },
      "additionalProperties": false
    },
    "template": {
      "type": "object",
      "required": [
        "template_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "template_key": {
          "$ref": "#/$defs/key"
        },
        "schedule": {
          "$ref": "notification-types.schema.json#/$defs/schedule"
        },
        "late_handling": {
          "$ref": "notification-types.schema.json#/$defs/lateHandling"
        },
        "rendering": {
          "$ref": "notification-rendering-integration-types.schema.json#/$defs/templateRendering"
        }
      },
      "additionalProperties": false
    },
    "profileRevision": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "#/$defs/itemTypes"
        },
        "templates": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": {
            "$ref": "#/$defs/template"
          }
        }
      },
      "additionalProperties": false
    },
    "archetypeSelection": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "item_archetype_id",
            "revision_resolution",
            "selection_source"
          ],
          "properties": {
            "item_archetype_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "revision_resolution": {
              "const": "current"
            },
            "selection_source": {
              "enum": [
                "operator_explicit",
                "agent_selected",
                "imported"
              ]
            },
            "source_ref": {
              "type": "string",
              "minLength": 1
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "item_archetype_id",
            "revision_resolution",
            "item_archetype_revision_id",
            "selection_source"
          ],
          "properties": {
            "item_archetype_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "revision_resolution": {
              "const": "exact"
            },
            "item_archetype_revision_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "selection_source": {
              "enum": [
                "operator_explicit",
                "agent_selected",
                "imported"
              ]
            },
            "source_ref": {
              "type": "string",
              "minLength": 1
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "replacement": {
      "type": "object",
      "required": [
        "template_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "template_key": {
          "$ref": "#/$defs/key"
        },
        "schedule": {
          "$ref": "notification-types.schema.json#/$defs/schedule"
        },
        "late_handling": {
          "$ref": "notification-types.schema.json#/$defs/lateHandling"
        }
      },
      "additionalProperties": false
    },
    "customAddition": {
      "type": "object",
      "required": [
        "policy_key",
        "schedule",
        "late_handling"
      ],
      "properties": {
        "policy_key": {
          "$ref": "#/$defs/key"
        },
        "schedule": {
          "$ref": "notification-types.schema.json#/$defs/schedule"
        },
        "late_handling": {
          "$ref": "notification-types.schema.json#/$defs/lateHandling"
        }
      },
      "additionalProperties": false
    },
    "overlays": {
      "type": "object",
      "properties": {
        "suppress_template_keys": {
          "type": "array",
          "maxItems": 32,
          "uniqueItems": true,
          "items": {
            "$ref": "#/$defs/key"
          }
        },
        "replacements": {
          "type": "array",
          "maxItems": 32,
          "items": {
            "$ref": "#/$defs/replacement"
          }
        },
        "custom_additions": {
          "type": "array",
          "maxItems": 32,
          "items": {
            "$ref": "#/$defs/customAddition"
          }
        }
      }
    },
    "createPlan": {
      "oneOf": [
        {
          "type": "object",
          "required": [
            "mode",
            "custom_additions"
          ],
          "properties": {
            "mode": {
              "const": "none"
            },
            "custom_additions": {
              "type": "array",
              "minItems": 1,
              "maxItems": 32,
              "items": {
                "$ref": "#/$defs/customAddition"
              }
            },
            "rendering_applications": {
              "$ref": "notification-rendering-integration-types.schema.json#/$defs/applications"
            }
          },
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "mode",
            "notification_profile_id",
            "revision_resolution"
          ],
          "properties": {
            "mode": {
              "const": "explicit"
            },
            "notification_profile_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "revision_resolution": {
              "enum": [
                "current",
                "exact"
              ]
            },
            "notification_profile_revision_id": {
              "$ref": "notification-types.schema.json#/$defs/id"
            },
            "suppress_template_keys": {
              "$ref": "#/$defs/overlays/properties/suppress_template_keys"
            },
            "replacements": {
              "$ref": "#/$defs/overlays/properties/replacements"
            },
            "custom_additions": {
              "$ref": "#/$defs/overlays/properties/custom_additions"
            },
            "rendering_applications": {
              "$ref": "notification-rendering-integration-types.schema.json#/$defs/applications"
            }
          },
          "allOf": [
            {
              "if": {
                "properties": {
                  "revision_resolution": {
                    "const": "exact"
                  }
                },
                "required": [
                  "revision_resolution"
                ]
              },
              "then": {
                "required": [
                  "notification_profile_revision_id"
                ]
              },
              "else": {
                "not": {
                  "required": [
                    "notification_profile_revision_id"
                  ]
                }
              }
            }
          ],
          "additionalProperties": false
        },
        {
          "type": "object",
          "required": [
            "mode",
            "scope_chain",
            "on_no_match"
          ],
          "properties": {
            "mode": {
              "const": "archetype_default"
            },
            "scope_chain": {
              "type": "array",
              "minItems": 1,
              "maxItems": 8,
              "uniqueItems": true,
              "items": {
                "$ref": "#/$defs/owner"
              }
            },
            "on_no_match": {
              "enum": [
                "fail",
                "use_custom_only"
              ]
            },
            "suppress_template_keys": {
              "$ref": "#/$defs/overlays/properties/suppress_template_keys"
            },
            "replacements": {
              "$ref": "#/$defs/overlays/properties/replacements"
            },
            "custom_additions": {
              "$ref": "#/$defs/overlays/properties/custom_additions"
            },
            "rendering_applications": {
              "$ref": "notification-rendering-integration-types.schema.json#/$defs/applications"
            }
          },
          "additionalProperties": false
        }
      ]
    },
    "normalizedRevision": {
      "type": "object",
      "required": [
        "compatible_item_types",
        "templates"
      ],
      "properties": {
        "compatible_item_types": {
          "$ref": "notification-profile-types.schema.json#/$defs/itemTypes"
        },
        "templates": {
          "type": "array",
          "minItems": 1,
          "maxItems": 32,
          "items": {
            "type": "object",
            "required": [
              "template_key",
              "schedule",
              "late_handling",
              "rendering",
              "normalized_template_hash"
            ],
            "properties": {
              "template_key": {
                "$ref": "notification-profile-types.schema.json#/$defs/key"
              },
              "schedule": {
                "$ref": "notification-types.schema.json#/$defs/schedule"
              },
              "late_handling": {
                "$ref": "notification-types.schema.json#/$defs/lateHandling"
              },
              "rendering": {
                "$ref": "notification-rendering-integration-types.schema.json#/$defs/templateRendering"
              },
              "normalized_template_hash": {
                "$ref": "notification-types.schema.json#/$defs/sha256"
              }
            },
            "additionalProperties": false
          }
        }
      },
      "additionalProperties": false
    }
  }
}
```

## src/spine/core/facets.py:1–132

Full-source SHA-256: `b89544dc0fb9b508ac5dd616219b1bffd3466e58620c59cdb55ae744fe0ec60f`.

```python
"""Pure, version-pinned facet codecs. No catalog, reference or permission I/O."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import date
from typing import Any, NoReturn

from spine.core.canonical_json import canonical_json_bytes, canonical_json_text
from spine.core.errors import SpineValidationError

DEFINITION_VERSION = "spine.facet-schemas.v1"
VALUE_VERSION = "spine.item-facets.v1"
CANONICAL_VERSION = "spine.canonical-json.v1"
KEY = re.compile(r"[a-z][a-z0-9_]{0,63}\Z", re.ASCII)
INTEGER = re.compile(r"(?:0|-?[1-9][0-9]*)\Z", re.ASCII)


def fail(code: str = "facet_value_invalid") -> NoReturn:
    raise SpineValidationError(code, "facet facts do not satisfy the pinned contract")


def nfc(value: str) -> str:
    if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        fail()
    return unicodedata.normalize("NFC", value)


def key(value: object) -> str:
    if not isinstance(value, str) or not KEY.fullmatch(value):
        fail()
    return str(value)


def integer(value: object) -> int:
    if not isinstance(value, str) or len(value) > 20 or not INTEGER.fullmatch(value):
        fail()
    result = int(value)
    if not -(2**63) <= result < 2**63:
        fail()
    return result


def _text(value: object, maximum: int, *, controls: bool = False) -> str:
    if not isinstance(value, str):
        fail()
    value = nfc(str(value))
    if not 1 <= len(value) <= maximum or (controls and any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in value)):
        fail()
    return value


def _object(value: object, required: set[str], optional: set[str] | None = None) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) - required - (optional or set()) or required - set(value):
        fail()
    return dict(value)


def normalize_definition(value: object) -> dict[str, Any]:
    try:
        result = _object(value, {"display_name", "description", "compatible_item_types", "fields"})
        result["display_name"] = _text(result["display_name"], 160)
        if result["description"] is not None:
            result["description"] = _text(result["description"], 2000)
        types = result["compatible_item_types"]
        if not isinstance(types, list) or not 1 <= len(types) <= 2 or any(t not in ("event", "task") for t in types):
            fail()
        if len(set(types)) != len(types):
            fail()
        result["compatible_item_types"] = sorted(types)
        fields = result["fields"]
        if not isinstance(fields, list) or not 1 <= len(fields) <= 32:
            fail()
        normalized = []
        for raw in fields:
            if not isinstance(raw, dict):
                fail()
            extras = {
                "text": {"max_length"},
                "enum": {"choices"},
                "integer": {"min", "max"},
                "boolean": set(),
                "date": set(),
                "reference": {"target_kind"},
            }
            kind = raw.get("type")
            if not isinstance(kind, str) or kind not in extras:
                fail()
            field = _object(raw, {"key", "type", "required"} | extras[kind], {"queryable"})
            field["key"] = key(field["key"])
            field.setdefault("queryable", False)
            if type(field["required"]) is not bool or type(field["queryable"]) is not bool:
                fail()
            if kind == "text" and not 1 <= integer(field["max_length"]) <= 1024:
                fail()
            if kind == "integer" and integer(field["min"]) > integer(field["max"]):
                fail()
            if kind == "reference" and field["target_kind"] not in ("subject", "location"):
                fail()
            if kind == "enum":
                choices = field["choices"]
                if not isinstance(choices, list) or not 1 <= len(choices) <= 64:
                    fail()
                choices = [_text(c, 128) for c in choices]
                if len(set(choices)) != len(choices):
                    fail()
                field["choices"] = sorted(choices)
            normalized.append(field)
        if len({f["key"] for f in normalized}) != len(normalized):
            fail()
        result["fields"] = sorted(normalized, key=lambda f: f["key"])
        if len(canonical_json_bytes(result)) > 32768:
            fail()
        return result
    except SpineValidationError as exc:
        raise SpineValidationError("facet_schema_invalid", "invalid facet definition") from exc


def definition_hash(definition: dict[str, Any]) -> str:
    return hashlib.sha256(
        canonical_json_bytes(
            {
                "derivation_version": "spine.facet-definition.v1",
                "definition": definition,
            }
        )
    ).hexdigest()


```

## src/spine/core/rendering_definitions.py:1–130

Full-source SHA-256: `b62b92250578bd19dd286bf60e63a111649c8b48ed8dbf95109af9b6623ace9a`.

```python
"""Pure codecs for the candidate rendering integration; no capability activation."""

from __future__ import annotations

import copy
from collections.abc import Mapping
from typing import Any

from spine.core.canonical_json import canonical_json_bytes, canonical_json_text
from spine.core.errors import SpineValidationError
from spine.core.facets import parse_object
from spine.core.hashing import hash_canonical_json
from spine.core.notification_profiles import (
    NormalizedProfileRevision,
    normalize_catalog_key,
    normalize_owner,
    normalize_profile_revision,
)
from spine.core.notification_rendering import _normalized_text

CANON = "spine.canonical-json.v1"
DEFINITIONS = "spine.notification-rendering-definitions.v1"
DISCLOSURES = "spine.notification-rendering-disclosures.v1"
PRESENTATION = "spine.notification-rendering-presentation.v1"
PROFILE_V2 = "spine.notification-profiles.v2"
MAX_INTEGER = 9223372036854775807


def fail(code: str, field: str, message: str = "rendering request could not complete") -> Any:
    raise SpineValidationError(f"{code}:{field}", message)


def exact(value: object, required: set[str], optional: set[str] | None = None, field: str = "request") -> dict[str, Any]:
    if not isinstance(value, Mapping):
        fail("invalid_request", field)
    result = copy.deepcopy(dict(value))
    extra = set(result) - required - (optional or set())
    prefix = "" if field == "request" else field + "."
    if extra:
        fail("unsupported_field", prefix + sorted(extra)[0])
    missing = required - set(result)
    if missing:
        fail("missing_required_field", prefix + sorted(missing)[0])
    canonical_json_bytes(result)  # Reject numbers and invalid Unicode before interpretation.
    return result


def identity(value: object, field: str, maximum: int = 256) -> str:
    if not isinstance(value, str) or not 1 <= len(value) <= maximum:
        fail("invalid_request", field)
    canonical_json_bytes(value)
    return value


def text(value: object, field: str, maximum: int) -> str:
    try:
        result = _normalized_text(identity(value, field, max(maximum, 32768)), field)
    except SpineValidationError as exc:
        fail("invalid_request", field, str(exc))
    if not result or len(result) > maximum:
        fail("invalid_request", field)
    return result


def owner(value: object) -> dict[str, Any]:
    normalized = normalize_owner(value)
    return {k: v for k, v in normalized.items() if v is not None}


def sorted_strings(value: object, field: str, maximum: int, *, minimum: int = 0, keys: bool = False) -> list[str]:
    if not isinstance(value, list) or not minimum <= len(value) <= maximum:
        fail("invalid_request", field)
    values = [normalize_catalog_key(v, field) if keys else identity(v, field) for v in value]
    if len(values) != len(set(values)):
        fail("semantic_conflict", field, "duplicate values are not permitted")
    return sorted(values)


def definition_reference(value: object) -> dict[str, str]:
    result = exact(value, {"notification_rendering_definition_id", "notification_rendering_definition_revision_id"}, field="definition")
    return {k: identity(v, "definition." + k) for k, v in result.items()}


def normalize_revision(value: object) -> dict[str, Any]:
    revision = exact(
        value,
        {"display_name", "description", "compatible_item_types", "base_rendering_contract", "base_rendering_profile", "selections"},
        field="revision",
    )
    revision["display_name"] = text(revision["display_name"], "revision.display_name", 160)
    if revision["description"] is not None:
        revision["description"] = text(revision["description"], "revision.description", 2000)
    types = revision["compatible_item_types"]
    if not isinstance(types, list) or not 1 <= len(types) <= 2 or any(not isinstance(v, str) or v not in {"event", "task"} for v in types):
        fail("rendering_definition_invalid", "revision.compatible_item_types")
    if len(types) != len(set(types)):
        fail("rendering_definition_invalid", "revision.compatible_item_types")
    revision["compatible_item_types"] = sorted(types)
    if (
        revision["base_rendering_contract"] != "spine.notification-rendering.v1"
        or revision["base_rendering_profile"] != "spine.notification-rendering.concise-en-ca.v1"
    ):
        fail("rendering_definition_invalid", "revision.base_rendering_contract")
    selections = revision["selections"]
    if not isinstance(selections, list) or not 1 <= len(selections) <= 8:
        fail("rendering_definition_invalid", "revision.selections")
    names, sources = set(), set()
    normalized = []
    for selection in selections:
        selection = exact(
            selection,
            {"selection_key", "facet_key", "facet_schema_revision_id", "field_key", "label", "projection"},
            field="revision.selections",
        )
        for k in ("selection_key", "facet_key", "field_key"):
            selection[k] = normalize_catalog_key(selection[k], "revision.selections." + k)
        identity(selection["facet_schema_revision_id"], "revision.selections.facet_schema_revision_id")
        selection["label"] = text(selection["label"], "revision.selections.label", 40)
        if selection["projection"] not in {"value", "location_label"}:
            fail("rendering_definition_invalid", "revision.selections.projection")
        source = tuple(selection[k] for k in ("facet_key", "facet_schema_revision_id", "field_key"))
        if selection["selection_key"] in names or source in sources:
            fail("rendering_definition_invalid", "revision.selections", "duplicate selection")
        names.add(selection["selection_key"])
        sources.add(source)
        normalized.append(selection)
    revision["selections"] = normalized
    bounded(revision, 8192, "revision")
    return revision

```

## src/spine/core/notification_rendering.py:412–420

Full-source SHA-256: `6bfe60d40701d6049d1fdaccaae25a283b764efe2a9dc19abf18ddd5d0459d2b`.

```python
def _normalized_text(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise SpineValidationError("notification_rendering_invalid_text", f"{field} must be text")
    result = _WHITESPACE.sub(" ", value.strip())
    if not result:
        raise SpineValidationError("notification_rendering_invalid_text", f"{field} normalizes to empty")
    if any(unicodedata.category(char).startswith("C") for char in result):
        raise SpineValidationError("notification_rendering_invalid_text", f"{field} contains a control character")
    return result
```
