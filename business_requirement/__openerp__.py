# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement',
    'category': 'Business Requirements Management',
    'summary': 'Manage the Business Requirements (stories, scenarios, gaps\
        and test cases) for your customers',
    'version': '8.0.5.1.2',
    'website': 'https://www.elico-corp.com/',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'product',
        'project',
    ],
    'data': [
        'data/business_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/business_view.xml',
        'views/project.xml',
    ],
    'image': [
        'static/description/icon.png',
        'static/img/bus_req.png',
        'static/img/bus_req_alias.png',
        'static/img/bus_req_approved.png',
        'static/img/bus_req_cancel.png',
        'static/img/bus_req_confirmed.png',
        'static/img/bus_req_cust_story.png',
        'static/img/bus_req_done.png',
        'static/img/bus_req_drop.png',
        'static/img/bus_req_tags.png',
        'static/img/bus_req_tags2.png',
        'static/img/bus_req_tree.png',
        'static/img/bus_req_workflow.png'
    ],
    'license': 'AGPL-3',
    'installable': True,
}
