import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-business-requirement",
    description="Meta package for oca-business-requirement Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-business_requirement>=16.0dev,<16.1dev',
        'odoo-addon-business_requirement_crm>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
