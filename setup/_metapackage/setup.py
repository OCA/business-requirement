import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-business-requirement",
    description="Meta package for oca-business-requirement Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-business_requirement',
        'odoo13-addon-business_requirement_crm',
        'odoo13-addon-business_requirement_deliverable',
        'odoo13-addon-business_requirement_sale',
        'odoo13-addon-business_requirement_sale_timesheet',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
