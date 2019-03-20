# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Business Requirement Deliverable - CRM',
    'category': 'Business Requirements Management',
    'summary': 'Create your sales quotations directly from the'
            ' Business Requirements deliverables',
    'version': '12.0.1.0.0',
    'maturity': 'stable',
    'website': 'https://github.com/OCA/business-requirement',
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
    'demo': ['data/business_requirement_deliverable_crm_demo.xml'],
    'license': 'LGPL-3',
    'installable': True,
}
