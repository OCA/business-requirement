# Copyright 2026 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    """Let the upgrade update the estimation group.

    The group was noupdate up to 18.0, so it would keep its old name and stay
    without the privilege that replaces its category in 19.0.
    """
    cr.execute(
        """
        UPDATE ir_model_data
        SET noupdate = FALSE
        WHERE module = 'business_requirement_deliverable'
            AND name = 'group_business_requirement_estimation'
        """
    )
