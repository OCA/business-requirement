import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-business-requirement",
    description="Meta package for oca-business-requirement Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-business_requirement',
        'odoo8-addon-business_requirement_deliverable',
        'odoo8-addon-business_requirement_deliverable_categ',
        'odoo8-addon-business_requirement_deliverable_cost',
        'odoo8-addon-business_requirement_deliverable_crm',
        'odoo8-addon-business_requirement_deliverable_project',
        'odoo8-addon-business_requirement_deliverable_project_categ',
        'odoo8-addon-business_requirement_deliverable_project_task_categ',
        'odoo8-addon-business_requirement_deliverable_report',
        'odoo8-addon-business_requirement_deliverable_resource_template',
        'odoo8-addon-business_requirement_deliverable_resource_template_categ',
        'odoo8-addon-business_requirement_earned_value',
        'odoo8-addon-business_requirement_etherpad',
        'odoo8-addon-business_requirement_from_support',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
