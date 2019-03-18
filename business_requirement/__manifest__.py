# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Business Requirement',
    'category': 'Business Requirements Management',
    'summary': 'Manage the Business Requirements (stories, scenarios, gaps\
        and test cases) for your customers',
    'version': '12.0.1.0.0',
    'maturity': 'stable',
    'website': 'https://github.com/OCA/business-requirement',
    "author": "Elico Corp, Odoo Community Association (OCA)",
    'depends': [
        'hr_timesheet',
        'product',
        'project',
    ],
    'data': [
        'data/business_data.xml',
        'data/br_report_paperformat.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/report_business_requirement.xml',
        'views/business_view.xml',
        'views/project.xml',
        'report/report.xml'
    ],
    'image': [
        'static/description/icon.png',
        'static/img/bus_req.png',
        'static/img/bus_req_alias.png',
        'static/img/bus_req_approved.png',
        'static/img/bus_req_cancel.png',
        'static/img/bus_req_confirmed.png',
        'static/img/bus_req_cust_story.png',
        'static/img/bus_req_done.png',
        'static/img/bus_req_drop.png',
        'static/img/bus_req_tags.png',
        'static/img/bus_req_tags2.png',
        'static/img/bus_req_tree.png',
        'static/img/bus_req_workflow.png'
    ],
    'demo': ['data/business_requirement_demo.xml'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}
