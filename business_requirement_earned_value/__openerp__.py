# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Earned Value Management',
    'category': 'Business Requirements Management',
    'summary': 'Manage the Earned Value for your customers',
    'version': '8.0.1.0.0',
    'website': 'https://www.elico-corp.com/',
    'author': 'Elico Corp, Odoo Community Association (OCA)',
    'depends': [
        'hr_timesheet',
        'project_timesheet',
        'business_requirement_deliverable_cost',
        'business_requirement_deliverable_project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/br_earned_value_report_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
}
