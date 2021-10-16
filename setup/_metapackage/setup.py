import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-business-requirement",
    description="Meta package for oca-business-requirement Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-business_requirement',
        'odoo12-addon-business_requirement_crm',
        'odoo12-addon-business_requirement_deliverable',
        'odoo12-addon-business_requirement_sale',
        'odoo12-addon-business_requirement_sale_timesheet',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)
