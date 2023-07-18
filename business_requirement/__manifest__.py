# Copyright 2017-2019 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Business Requirement",
    "category": "Business Requirements Management",
    "summary": "Manage the Business Requirements (stories, scenarios, gaps\
        and test cases) for your customers",
    "version": "15.0.1.0.1",
    "website": "https://github.com/OCA/business-requirement",
    "author": "Elico Corp, Tecnativa, Odoo Community Association (OCA)",
    "depends": ["product", "portal"],
    "data": [
        "data/business_data.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/business_view.xml",
        "views/br_report.xml",
        "views/br_portal_templates.xml",
        "report/report.xml",
    ],
    "image": [
        "static/description/icon.png",
        "static/img/bus_req.png",
        "static/img/bus_req_alias.png",
        "static/img/bus_req_approved.png",
        "static/img/bus_req_cancel.png",
        "static/img/bus_req_confirmed.png",
        "static/img/bus_req_cust_story.png",
        "static/img/bus_req_done.png",
        "static/img/bus_req_drop.png",
        "static/img/bus_req_tags.png",
        "static/img/bus_req_tags2.png",
        "static/img/bus_req_tree.png",
        "static/img/bus_req_workflow.png",
    ],
    "assets": {
        "web.assets_tests": [
            "/business_requirement/static/src/js/business_requirement_portal_tour.js",
        ],
    },
    "demo": ["data/business_requirement_demo.xml"],
    "license": "AGPL-3",
    "installable": True,
    "application": True,
}
