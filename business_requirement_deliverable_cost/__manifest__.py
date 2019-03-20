# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Business Requirement Deliverable Cost Control',
    'summary': 'Control the cost of your Business Requirements',
    'version': '12.0.1.0.0',
    'maturity': 'stable',
    'category': 'Business Requirements Management',
    'website': 'https://github.com/OCA/business-requirement',
    'author': 'Elico Corp, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'business_requirement_deliverable',
    ],
    'image': [
        'static/description/icon.png',
        'static/img/bus_req_acl1.png',
        'static/img/bus_req_acl2.png',
        'static/img/bus_req_acl3.png',
        'static/img/bus_req_control.png'
    ],
    'data': [
        'data/business_data.xml',
        'security/business_requirement_deliverable_security.xml',
        'security/ir.model.access.csv',
        'views/business.xml',
        'report/br_deliverable_cost_report_view.xml',
        'views/report_business_requirement_other_resources_report.xml',
        'report/report.xml',

    ],
    'demo': ['data/business_requirement_deliverable_cost_demo.xml'],
}
