# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Document Printout',
    'summary': 'Print the Business Requirement Document for your customers',
    'version': '8.0.5.0.1',
    'category': 'Business Requirements Management',
    'website': 'https://www.elico-corp.com',
    'author': 'Elico Corp, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'business_requirement_deliverable',
    ],
    'data': [
        'views/report_business_requirement.xml',
        'views/report_business_requirement_deliverable.xml',
        'views/report_business_requirement_deliverable_resource.xml',
        'report/report.xml'
    ],
    'image': [
        'static/img/bus_req_report1.png',
        'static/img/bus_req_report2.png',
        'static/img/bus_req_report3.png',
    ],
}
