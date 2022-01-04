import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-business-requirement",
    description="Meta package for oca-business-requirement Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-business_requirement',
        'odoo14-addon-business_requirement_crm',
        'odoo14-addon-business_requirement_deliverable',
        'odoo14-addon-business_requirement_sale',
        'odoo14-addon-business_requirement_sale_timesheet',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
