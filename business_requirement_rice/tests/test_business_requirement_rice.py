# Copyright 2026 Binhex - Zuzanna Elzbieta Szalaty Szalaty
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import TransactionCase

from odoo.addons.business_requirement_rice.models.business_requirement import (
    CONFIDENCE_WEIGHTS,
    IMPACT_WEIGHTS,
)


class TestBusinessRequirementRice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.requirement = cls.env["business.requirement"].create(
            {"description": "Export to spreadsheet"}
        )

    def test_default_score_is_zero(self):
        """A requirement with no reach is not scored yet"""
        self.assertEqual(self.requirement.rice_score, 0)

    def test_compute_score(self):
        self.requirement.write(
            {
                "rice_reach": 500,
                "rice_impact": "high",
                "rice_confidence": "medium",
                "rice_effort": 4.0,
            }
        )
        # 500 * 2 * 0.8 / 4
        self.assertEqual(self.requirement.rice_score, 200)

    def test_compute_score_recomputed_on_change(self):
        self.requirement.write(
            {
                "rice_reach": 100,
                "rice_impact": "medium",
                "rice_confidence": "medium",
                "rice_effort": 1.0,
            }
        )
        # 100 * 1 * 0.8 / 1
        self.assertEqual(self.requirement.rice_score, 80)
        self.requirement.rice_impact = "massive"
        # 100 * 3 * 0.8 / 1
        self.assertEqual(self.requirement.rice_score, 240)

    def test_score_without_impact_or_confidence(self):
        """Impact and confidence are optional, so they must not raise"""
        self.requirement.write(
            {
                "rice_reach": 100,
                "rice_impact": False,
                "rice_confidence": False,
                "rice_effort": 1.0,
            }
        )
        self.assertEqual(self.requirement.rice_score, 0)

    def test_every_option_has_a_weight(self):
        """An option with no weight must fail here, not when a user reads it"""
        descriptions = self.env["business.requirement"].fields_get(
            ["rice_impact", "rice_confidence"]
        )
        self.assertEqual(
            {key for key, _label in descriptions["rice_impact"]["selection"]},
            set(IMPACT_WEIGHTS),
        )
        self.assertEqual(
            {key for key, _label in descriptions["rice_confidence"]["selection"]},
            set(CONFIDENCE_WEIGHTS),
        )

    def test_zero_effort_does_not_raise(self):
        """Effort is free text, so it must not divide by zero"""
        self.requirement.write({"rice_reach": 100, "rice_effort": 0.0})
        self.assertEqual(self.requirement.rice_score, 0)

    def test_negative_effort_does_not_raise(self):
        self.requirement.write({"rice_reach": 100, "rice_effort": -2.0})
        self.assertEqual(self.requirement.rice_score, 0)

    def test_negative_reach_is_not_scored(self):
        """A negative reach is as unusable an estimate as a negative effort"""
        self.requirement.write({"rice_reach": -100, "rice_effort": 1.0})
        self.assertEqual(self.requirement.rice_score, 0)

    def test_score_is_searchable_and_sortable(self):
        """The score is stored, so it can order a list view"""
        low = self.requirement
        low.write({"rice_reach": 10, "rice_effort": 1.0})
        high = low.copy({"rice_reach": 1000})
        found = self.env["business.requirement"].search(
            [("id", "in", (low + high).ids)], order="rice_score desc"
        )
        self.assertEqual(found[0], high)
        self.assertEqual(
            self.env["business.requirement"].search_count(
                [("id", "in", (low + high).ids), ("rice_score", ">", 100)]
            ),
            1,
        )
