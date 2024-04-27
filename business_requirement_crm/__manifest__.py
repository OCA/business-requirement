# Copyright 2019 Tecnativa - Victor M.M. Torres
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Business Requirement CRM",
    "category": "Business Requirements Management",
    "summary": "Convert Leads to Business Requirement",
    "version": "16.0.1.0.1",
    "website": "https://github.com/OCA/business-requirement",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "depends": ["crm", "business_requirement"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/crm_lead_convert_to_requirement_views.xml",
        "views/crm_lead_views.xml",
        "views/business_requirement_views.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
