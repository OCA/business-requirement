# Copyright 2026 Binhex - Zuzanna Elzbieta Szalaty Szalaty
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

# The weight of each option, kept apart from the selection keys so that the
# stored value identifies the estimate and not its arithmetic value. A module
# adding an option has to add its weight here too, which the tests check.
IMPACT_WEIGHTS = {
    "minimal": 0.25,
    "low": 0.5,
    "medium": 1.0,
    "high": 2.0,
    "massive": 3.0,
}
CONFIDENCE_WEIGHTS = {
    "low": 0.5,
    "medium": 0.8,
    "high": 1.0,
}


class BusinessRequirement(models.Model):
    _inherit = "business.requirement"

    rice_reach = fields.Integer(
        string="Reach",
        help="How many users or events are affected over a given period, "
        "for instance the number of users per quarter.",
    )
    rice_impact = fields.Selection(
        selection=[
            ("minimal", "Minimal"),
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("massive", "Massive"),
        ],
        string="Impact",
        default="medium",
        help="How much each affected user benefits from the requirement.",
    )
    rice_confidence = fields.Selection(
        selection=[
            ("low", "Low (50%)"),
            ("medium", "Medium (80%)"),
            ("high", "High (100%)"),
        ],
        string="Confidence",
        default="medium",
        help="How confident you are about the reach and impact estimates.",
    )
    rice_effort = fields.Float(
        string="Effort",
        default=1.0,
        help="Total work needed, usually estimated in person-months.",
    )
    rice_score = fields.Float(
        string="RICE Score",
        compute="_compute_rice_score",
        store=True,
        index=True,
        aggregator="avg",
        digits=(16, 2),
        help="Reach x Impact x Confidence / Effort. The higher the score, "
        "the sooner the requirement should be addressed.",
    )

    @api.depends("rice_reach", "rice_impact", "rice_confidence", "rice_effort")
    def _compute_rice_score(self):
        for requirement in self:
            # Neither a negative reach nor an effort of zero or less is a
            # usable estimate, so the requirement is left unscored rather
            # than ranked below the ones nobody has estimated yet.
            if requirement.rice_reach < 0 or requirement.rice_effort <= 0:
                requirement.rice_score = 0
                continue
            # Impact and confidence are optional, and an unset one scores
            # zero. A key that is set but has no weight raises instead,
            # since that means a module added an option and forgot it.
            impact = (
                IMPACT_WEIGHTS[requirement.rice_impact]
                if requirement.rice_impact
                else 0
            )
            confidence = (
                CONFIDENCE_WEIGHTS[requirement.rice_confidence]
                if requirement.rice_confidence
                else 0
            )
            requirement.rice_score = (
                requirement.rice_reach * impact * confidence / requirement.rice_effort
            )
