# Copyright 2019 Tecnativa Victor M.M. Torres>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Business Requirement Sale",
    'category': 'Business Requirements Management',
    'summary': 'Convert Business Requirement into \
                Sale Orders',
    "version": "11.0.1.0.0",
    "development_status": "Alpha",
    "website": "https://github.com/OCA/business-requirement",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "business_requirement_deliverable",
        "sale_management",
    ],
    "data": [
        'security/ir.model.access.csv',
        'wizard/convert_requirement_sale.xml',
        'views/sale_order_views.xml',
        'views/business_requirement_views.xml',
    ],
}
