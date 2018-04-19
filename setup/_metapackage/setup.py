import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-business-requirement",
    description="Meta package for oca-business-requirement Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-business_requirement',
        'odoo10-addon-business_requirement_deliverable',
        'odoo10-addon-business_requirement_deliverable_cost',
        'odoo10-addon-business_requirement_deliverable_crm',
        'odoo10-addon-business_requirement_deliverable_project',
        'odoo10-addon-business_requirement_deliverable_project_task_categ',
        'odoo10-addon-business_requirement_deliverable_resource_template',
        'odoo10-addon-business_requirement_deliverable_resource_template_categ',
        'odoo10-addon-business_requirement_etherpad',
        'odoo10-addon-business_requirement_gap_analysis_task',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
