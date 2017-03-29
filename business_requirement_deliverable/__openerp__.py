# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Deliverable',
    'category': 'Business Requirements Management',
    'summary': 'Manage the Business Requirement Deliverables and \
                Resources for your customers',
    'version': '8.0.4.0.0',
    'website': 'https://www.elico-corp.com/',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'account',
        'business_requirement',
    ],
    'data': [
        'security/business_requirement_deliverable_security.xml',
        'security/ir.model.access.csv',
        'views/business_view.xml',
    ],
    'image': [
        'static/description/icon.png',
        'static/img/bus_req_deliverable.png',
        'static/img/bus_req_deliverable2.png',
        'static/img/bus_req_resource.png'
    ],
    'license': 'AGPL-3',
    'installable': True,
}
