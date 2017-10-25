# -*- coding: utf-8 -*-
# © 2016-2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Business Requirement Deliverable - Project',
    'category': 'Business Requirements Management',
    'summary': 'Create projects and tasks directly from'
            ' the Business Requirement and Resources lines',
    'version': '10.0.1.0.0',
    'website': 'https://www.elico-corp.com/',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'business_requirement_deliverable',
        'project',
        'hr_timesheet',
        'project_parent'
    ],
    'data': [
        'views/business_view.xml',
        'views/project.xml',
        'wizard/generate_projects_view.xml',
    ],
    'image': [
        'static/description/icon.png',
        'static/img/bus_req_project.png'
    ],
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
}
