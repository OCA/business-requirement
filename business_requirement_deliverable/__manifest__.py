# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Deliverable',
    'category': 'Business Requirements Management',
    'summary': 'Manage the Business Requirement Deliverables \
                for your customers',
    'version': '11.0.1.0.0',
    'website': 'https://www.elico-corp.com/',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'account',
        'business_requirement',
    ],
    'data': [
        'data/business_data.xml',
        'data/brd_report_paperformat.xml',
        'security/business_requirement_deliverable_security.xml',
        'security/ir.model.access.csv',
        'views/business_view.xml',
        'views/res_partner.xml',
        'views/report_business_requirement_deliverable.xml',
        'views/brd_portal_templates.xml',
        'views/assets.xml',
        'report/report.xml',
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
