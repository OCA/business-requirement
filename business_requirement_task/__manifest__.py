# Copyright 2026 Jarsa Sistemas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Business Requirement Project Tasks",
    "category": "Business Requirements Management",
    "summary": "Link business requirements to project tasks",
    "version": "17.0.1.0.0",
    "website": "https://github.com/OCA/business-requirement",
    "author": "Jarsa Sistemas, Odoo Community Association (OCA)",
    "depends": ["business_requirement", "project"],
    "data": [
        "views/business_requirement_views.xml",
        "views/project_task_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
