"""Apply preflight is fresh, deterministic, and incapable of Spine writes."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests/runtime"))

from spine_packs import artifacts as a
from spine_packs.planning import PlanError, plan_installation
from spine_packs.preflight import preflight_apply
from test_planning import FakeSpine, catalog, manifest, request


def approval(plan):
    return a.seal({
        "artifact_schema": "spine.pack-install-approval.v1",
        "plan_digest": plan["content_identity"]["digest"],
        "approve_complete_plan": True,
        "acknowledge_single_operator": True,
        "authorized_update_action_ids": plan["decision_action_ids"],
        "execution": {
            "execution_id": "123e4567-e89b-42d3-a456-426614174000",
            "actor_subject_id": "subject_operator",
            "action_timestamp_utc": "2026-09-12T10:00:00Z",
        },
    })


class ApplyPreflightTests(unittest.TestCase):
    def released_missing(self):
        pack = manifest(released=True)
        plan = plan_installation(pack, request(), FakeSpine())
        self.assertTrue(plan["apply_eligible"])
        return pack, plan

    def assert_failure(self, code, pack, plan, approved, transport=None):
        with self.assertRaises(PlanError) as caught:
            preflight_apply(pack, plan, approved, transport or FakeSpine())
        self.assertEqual(caught.exception.code, code)

    def test_success_reobserves_plan_and_returns_execution_facts(self):
        pack, plan = self.released_missing()
        approved = approval(plan)
        transport = FakeSpine()
        result = preflight_apply(pack, plan, approved, transport)
        self.assertEqual(result["plan_digest"], plan["content_identity"]["digest"])
        self.assertEqual(result["approval_digest"], approved["content_identity"]["digest"])
        self.assertEqual(result["action_ids"], [x["action_id"] for x in plan["actions"]])
        self.assertTrue(transport.calls)
        self.assertTrue(all(command in {
            "system.info", "item_archetype.list", "item_archetype.show",
            "notification_profile.list", "notification_profile.show",
            "notification_profile.binding.list",
        } for command, _ in transport.calls))

    def test_draft_plan_stops_before_transport(self):
        pack = manifest()
        plan = plan_installation(pack, request(), FakeSpine())
        transport = FakeSpine()
        self.assert_failure("draft_plan_not_applicable", pack, plan, approval(plan), transport)
        self.assertEqual(transport.calls, [])

    def test_wrong_plan_or_incomplete_update_approval_is_rejected(self):
        pack, plan = self.released_missing()
        approved = approval(plan)
        approved["plan_digest"] = "f" * 64
        self.assert_failure("invalid_or_incomplete_approval", pack, plan, a.seal(approved))

        entries = catalog(pack)
        entries["profiles"][0]["display_name"] = "Old name"
        drift_plan = plan_installation(pack, request(), FakeSpine(entries))
        incomplete = approval(drift_plan)
        incomplete["authorized_update_action_ids"] = []
        self.assert_failure(
            "invalid_or_incomplete_approval", pack, drift_plan, a.seal(incomplete)
        )

    def test_manifest_or_catalog_change_is_stale(self):
        pack, plan = self.released_missing()
        changed_pack = manifest("medical_and_lesson", released=True)
        self.assert_failure("manifest_identity_mismatch", changed_pack, plan, approval(plan))

        self.assert_failure("stale_plan", pack, plan, approval(plan), FakeSpine(catalog(pack)))

    def test_invalid_plan_stops_before_transport(self):
        pack, plan = self.released_missing()
        invalid = deepcopy(plan)
        invalid["actions"][0]["command"] = "notification_profile.binding.set"
        transport = FakeSpine()
        self.assert_failure("invalid_plan", pack, invalid, approval(plan), transport)
        self.assertEqual(transport.calls, [])


if __name__ == "__main__":
    unittest.main()
