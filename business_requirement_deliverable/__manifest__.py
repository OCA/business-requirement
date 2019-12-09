# Copyright 2016-2019 Elico Corp (https://www.elico-corp.com).
# Copyright 2019 Tecnativa - Alexandre Díaz
# Copyright 2019 Tecnativa - Víctor M.M. Torres
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Deliverable',
    'category': 'Business Requirements Management',
    'summary': 'Manage the Business Requirement Deliverables \
                for your customers',
    'version': '12.0.1.2.0',
    'website': 'https://github.com/OCA/business-requirement',
    "author": "Elico Corp, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    'depends': [
        'account',
        'business_requirement',
    ],
    'data': [
        'data/business_data.xml',
        'data/mail_message_subtype_data.xml',
        'security/business_requirement_deliverable_security.xml',
        'security/ir.model.access.csv',
        'views/business_view.xml',
        'views/brd_section.xml',
        'views/res_partner.xml',
        'views/br_report.xml',
        'views/brd_portal_templates.xml',
        'views/assets.xml',
    ],
    'image': [
        'static/description/icon.png',
        'static/img/bus_req_deliverable.png',
        'static/img/bus_req_deliverable2.png',
        'static/img/bus_req_report1.png',
        'static/img/bus_req_report2.png',
        'static/img/bus_req_report3.png',

    ],
    'demo': ['data/business_requirement_deliverable_demo.xml'],
    'license': 'AGPL-3',
    'installable': True,
}
