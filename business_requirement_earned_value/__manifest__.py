# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Business Requirement Earned Value",
    "summary": "Follow-up project completion (estimated / consumed)",
    "version": "12.0.1.0.0",
    "category": "Project",
    'website': 'https://github.com/OCA/business-requirement/',
    'support': 'support@elico-corp.com',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "hr_timesheet",
        "project_issue_sheet",
        "project_task_category",
        "business_requirement_deliverable_project",
    ],
    "data": [
        "report/project_completion_report_view.xml",
        "security/ir.model.access.csv",
        'views/br_and_project_inherit_view.xml',
    ],
    'demo': [
        'demo/project_completion_report_demo.xml'
    ]
}
