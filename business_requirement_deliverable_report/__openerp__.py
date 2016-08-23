# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Deliverable Report Module',
    'sumarry': 'Business Requirement Deliverable Report Module',
    'version': '8.0.5.0.1',
    'category': 'report',
    'website': 'https://www.elico-corp.com',
    'author': 'Elico Corp',
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
}
