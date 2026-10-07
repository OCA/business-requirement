# Copyright 2026 Binhex
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Business Requirement Deliverable - Project",
    "category": "Business Requirements Management",
    "summary": "Create project tasks from the deliverables of approved requirements",
    "version": "18.0.1.0.0",
    "website": "https://github.com/OCA/business-requirement",
    "author": "Binhex, Odoo Community Association (OCA)",
    "maintainers": ["oliverg09"],
    "depends": ["business_requirement_deliverable", "project"],
    "data": [
        "views/business_requirement_views.xml",
        "views/project_task_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
