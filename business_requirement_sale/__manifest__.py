# Copyright 2019 Tecnativa - Victor M.M. Torres
# Copyright 2021 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Business Requirement Sale",
    "category": "Business Requirements Management",
    "summary": "Convert Business Requirement into Sales Orders",
    "version": "14.0.1.0.0",
    "website": "https://github.com/OCA/business-requirement",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["business_requirement_deliverable", "sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/business_requirement_create_sale_views.xml",
        "views/sale_order_views.xml",
        "views/business_requirement_views.xml",
    ],
}
