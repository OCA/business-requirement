# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': "Business Requirement Gap Analysis Task",
    'summary': """Add Gap Analysis Task to your Business Requirement""",
    'author': "Elico Corp, Odoo Community Association (OCA)",
    'website': "https://github.com/OCA/business-requirement",
    'category': 'Business Requirements Management',
    'version': '12.0.1.0.0',
    'depends': ['business_requirement_deliverable_project_task_categ'],
    'data': [
        'wizard/create_gap_task.xml',
        'views/business_requirement_gap_analysis_task.xml',
        'views/res_config.xml',
    ],
    'demo': ['data/gap_analysis_task_demo.xml',
             'data/business_requirement_demo.xml'],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
