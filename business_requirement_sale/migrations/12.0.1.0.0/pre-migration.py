# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr, """
        UPDATE sale_order_line sol
        SET br_deliverable_section_id = slc.br_deliverable_section_id
        FROM sale_layout_category slc
        WHERE slc.id = sol.layout_category_id
             AND sol.display_type = 'line_section'
        """,
    )
