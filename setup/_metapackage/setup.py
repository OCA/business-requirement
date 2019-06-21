import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-business-requirement",
    description="Meta package for oca-business-requirement Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-business_requirement',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
