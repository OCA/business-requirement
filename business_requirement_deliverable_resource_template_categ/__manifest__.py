# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Deliverable Resource Template Category',
    'category': 'Business Requirements Management',
    'summary': """Manage default resource lines categories in your
               deliverable templates""",
    'version': '10.0.1.1.0',
    'website': 'https://www.elico-corp.com/',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'business_requirement_deliverable_project_task_categ',
        'business_requirement_deliverable_resource_template',
    ],
    'image': [
        'static/description/icon.png',
        'static/img/bus_req_default.png',
        'static/img/bus_req_default2.png'
    ],
    'data': [
        "views/business_requirement_resource_template.xml",
    ],
    'demo': [
        "data/"
        "business_requirement_deliverable_resource_template_categ_demo.xml",
    ],
    'license': 'AGPL-3',
    'installable': True,
}
