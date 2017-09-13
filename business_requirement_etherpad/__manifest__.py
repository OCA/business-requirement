# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Etherpad',
    'category': 'Business Requirements Management',
    'summary': 'Manage the Business Requirements Notes via Etherpad',
    'version': '10.0.1.0.0',
    'website': 'https://www.elico-corp.com/',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'pad',
        'business_requirement',
    ],
    'data': [
        'views/business_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
}
