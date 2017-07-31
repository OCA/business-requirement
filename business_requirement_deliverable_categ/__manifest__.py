# -*- coding: utf-8 -*-
# © 2017 Elico Corp (www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Business Requirement Resources Task Categories",
    'category': 'Business Requirements Management',
    'summary': 'Adds Task Categories to your Business Requirement Resources',
    "version": "10.0.1.0.0",
    "website": "https://www.elico-corp.com/",
    "author": "Elico Corp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": False,
    "depends": [
        "project_categ",
        "business_requirement_deliverable"
    ],
    'image': [
        'static/description/icon.png',
        'static/img/bus_req_category.png'
    ],
    "data": [
        "views/business_requirement_deliverable_categ.xml",
    ],
}
