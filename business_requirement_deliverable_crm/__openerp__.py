# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Deliverable - CRM',
    'category': 'Business Requirements Management',
    'summary': 'Create your sales quotations directly from the'
            ' Business Requirements deliverables',
    'version': '8.0.1.0.1',
    'website': 'https://www.elico-corp.com/',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'business_requirement_deliverable',
        'crm',
        'sale_crm',
    ],
    'data': [
        'wizard/crm_make_sale_view.xml',
        'views/crm_view.xml',
    ],
    'image': [
        'static/description/icon.png'
    ],
    'license': 'AGPL-3',
    'installable': True,
}
