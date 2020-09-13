# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Business Requirement Deliverable Resource Template Category',
    'category': 'Business Requirements Management',
    'summary': """Manage default resource lines categories in your
               deliverable templates""",
    'version': '12.0.1.1.0',
    'website': 'https://github.com/OCA/business-requirement',
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
    'license': 'LGPL-3',
    'installable': True,
}
