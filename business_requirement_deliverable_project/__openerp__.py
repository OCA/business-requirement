# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Deliverable - Project',
    'category': 'Business Requirements Management',
    'summary': 'Create projects and tasks directly from'
            ' the Business Requirement and Resources lines',
    'version': '8.0.4.0.4',
    'website': 'https://www.elico-corp.com/',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'business_requirement_deliverable',
        'project',
    ],
    'data': [
        'views/business_view.xml',
        'wizard/generate_projects_view.xml',
    ],
    'image': [
        'static/description/icon.png',
        'static/img/bus_req_project.png'
    ],
    'license': 'AGPL-3',
    'installable': True,
}
