# Copyright 2026 Binhex - Oliver García
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Business Requirement Project",
    "category": "Business Requirements Management",
    "summary": "Link project tasks to business requirements",
    "version": "18.0.1.0.0",
    "website": "https://github.com/OCA/business-requirement",
    "author": "Binhex, Odoo Community Association (OCA)",
    "maintainers": ["oliverg09"],
    "depends": ["business_requirement", "project"],
    "data": [
        "views/project_task_views.xml",
        "views/business_requirement_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
