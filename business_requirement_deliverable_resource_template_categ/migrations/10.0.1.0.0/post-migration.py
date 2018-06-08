# -*- coding: utf-8 -*-
# © 2018 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    cr = env.cr
    if openupgrade.table_exists(cr, 'project_category_main') and \
            openupgrade.table_exists(cr, 'project_category'):
        query = """
            UPDATE business_requirement_resource_template m SET categ_id = a.id
              FROM project_category a, project_category_main b
            WHERE a.name = b.name
              AND m.categ_id = b.id
            ;
        """
        openupgrade.logged_query(cr, query)
    openupgrade.logging(
        "business_requirement_resource_template migration done."
    )
