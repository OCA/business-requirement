# Copyright 2019 Tecnativa - Victor M.M. Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Business Requirement Sale Timesheet",
    'category': 'Business Requirements Management',
    "version": "12.0.1.0.0",
    "website": "https://github.com/OCA/business-requirement",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "business_requirement_sale",
        "sale_timesheet",
    ],
    "data": [
        'views/project_task.xml',
    ],
}
