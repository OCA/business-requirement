# -*- coding: utf-8 -*-
# Copyright 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Business Requirement Gap Analysis Task",
    'summary': """Add Gap Analysis Task to your Business Requirement""",
    'author': "Elico Corp, Odoo Community Association (OCA)",
    'website': "https://github.com/OCA/business-requirement",
    'category': 'Business Requirements Management',
    'version': '10.0.1.0.0',
    'depends': ['business_requirement_deliverable_project_task_categ'],
    'data': [
        'wizard/create_gap_task.xml',
        'views/business_requirement_gap_analysis_task.xml',
        'views/res_config.xml',
    ],
    'demo': ['data/gap_analysis_task_demo.xml',
             'data/business_requirement_demo.xml'],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
}
