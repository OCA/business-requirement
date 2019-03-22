# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Business Requirement Etherpad',
    'category': 'Business Requirements Management',
    'summary': 'Manage the Business Requirements Notes via Etherpad',
    'version': '12.0.1.0.0',
    'website': 'https://github.com/OCA/business-requirement',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'pad',
        'business_requirement',
    ],
    'data': [
        'views/business_view.xml',
    ],
    'demo': [
        'data/pad_demo.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
}
