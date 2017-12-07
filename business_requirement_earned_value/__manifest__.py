# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Business Requirement Earned Value",
    "summary": "Follow-up project completion (estimated / consumed)",
    "version": "10.0.1.0.0",
    "category": "Project",
    'website': 'https://github.com/OCA/business-requirement/',
    'support': 'support@elico-corp.com',
    "author": "Elico Corp",
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    "depends": [
        "project_timesheet",
        "project_issue_sheet",
        "project_project_category",
        "business_requirement_deliverable_project",
    ],
    "data": [
        "report/project_completion_report_view.xml",
        "security/ir.model.access.csv",
    ],
}
