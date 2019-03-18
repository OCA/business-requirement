What is a Business Requirement?
-------------------------------

A **Business requirement** (BR) is the expression of a business need by a customer
or internal project user.

A BR contains multiple different parts to explain the stakeholder need and how to
meet his/her requirements:

* **Customer Story**: this is the requirement as expressed by the customer
* **Scenario**: How/where the current solution can provide a suitable scenario to
  answer the customer story
* **Gap**: For the uncovered part of the scenario, elaborate the gap/need for specific
  developments/setup
* **Test case**: A set of conditions under which a tester will determine whether the application, software system or
  one of its features is working as it was originally established for it to do.
* **Deliverables** to be provided to the customer/user
* **Resources** necessary to achieve the deliverables
* **Additional** information (approval, cost control etc.)

This set of modules was originally designed for the service/IT industry but the
requirement management design has been kept as generic as possible so that it can
apply to many other cases/industries (customer or internal projects):

* Construction
* Trading (New product development)
* Business Consultancy
* Web or IT development
* R&D projects
* etc.

More information about business requirements management:

* `Wikipedia <https://en.wikipedia.org/wiki/Business_requirements>`_
* `Six Sigma <https://www.isixsigma.com/implementation/project-selection-tracking/business-requirements-document-high-level-review/>`_

Business Requirement set of modules
-----------------------------------

This module is part of a set (`Business Requirements repo <https://github.com/OCA/business-requirement/tree/10.0>`_).

The base Business Requirements module creates the basic objects and
can be used as a standalone module.

.. figure:: ../business_requirement/static/img/bus_req_tree.png
   :width: 600 px
   :alt: Business Requirement List view

Multiple modules integrate the BR with other business areas, such as Sales,
Procurement, Project or Analytic Accounting. For example:

* Sales Quotation can have an estimation supported by a BR analysis
* Project Tasks can be related to the BRs they implement or support
* Procurement and purchase can be generated out of the BR

.. figure:: ../business_requirement/static/img/bus_req_module_diag.png
   :width: 600 px
   :alt: Business Requirement modules diagram

The following workflow explains the business workflow between the BR modules and other applications in Odoo:

.. figure:: ../business_requirement/static/img/bus_req_workflow.png
   :width: 600 px
   :alt: Business Requirement integration in Odoo


How to use this module?
-----------------------

This module only contains the standard base models for business requirement:

* BR model definition
* Standard setup and views
* Standard Workflow

.. figure:: ../business_requirement/static/img/bus_req.png
   :width: 600 px
   :alt: Business Requirement Form

How to install the modules in Odoo
==================================
If you already have an Odoo instance up and running, your preferred way to install
addons will work with `Business Requirement`.

A reasonable knowledge of Odoo technical management is necessary to be able to
install and run this modules. The
`standard installation how-to <https://www.odoo.com/documentation/12.0/setup/install.html>`_
should be able to get you started.

Using git
---------
The most common way to install the module is to clone the git repository in your
server and add the directory to your `odoo.conf` file:

#. Clone the git repository

   .. code-block:: sh

      cd your-addons-path
      git clone https://github.com/OCA/business-requirement
      cd business-requirement
      git checkout 12.0 #for the version 12.0

#. Update the addon path of `odoo.conf`
#. Restart Odoo
#. Update the addons list in your database (Menu `Apps > Update Apps List` in developer mode)
#. Install the `Business Requirements` modules in menu `Apps`.

Using pip
---------
An easy way to install it with all its dependencies is using pip:

#. Recover the code from pip repository

   .. code-block:: sh

      pip install odoo10-addon-business_requirement odoo-autodiscover

#. Restart Odoo
#. Update the addons list in your database (Menu `Apps > Update Apps List` in developer mode)
#. Install the `Business Requirements` modules in menu `Apps`.

Fresh install with Docker
-------------------------
If you do not have any Odoo server installed, you can start your own Odoo in few
minutes via Docker in command line.

Here is the basic how-to (based on https://github.com/Elico-Corp/odoo-docker), valid
for Ubuntu OS but could also easily be replicated in MacOS or Windows:

#. Install docker and docker-compose in your system
#. Create the directory structure (assuming the base directory is `odoo`)

   .. code-block:: sh

      mkdir odoo && cd odoo
      mkdir -p ./volumes/postgres ./volumes/odoo/addons ./volumes/odoo/filestore \
      ./volumes/odoo/sessions

#. Create a `docker-compose.yml` file in `odoo` directory with following content:

   .. code-block:: xml

       version: '3.3'
       services:

         postgres:
           image: postgres:9.5
           volumes:
             - ./volumes/postgres:/var/lib/postgresql/data
           environment:
             - POSTGRES_USER=odoo

         odoo:
           image: elicocorp/odoo:12.0
           command: start
           ports:
             - 127.0.0.1:8069:8069
           volumes:
             - ./volumes/odoo/addons:/opt/odoo/additional_addons
             - ./volumes/odoo/filestore:/opt/odoo/data/filestore
             - ./volumes/odoo/sessions:/opt/odoo/data/sessions
           links:
             - postgres:db
           environment:
             - ADDONS_REPO=https://github.com/OCA/business-requirement.git
             - ODOO_DB_USER=odoo

#. Fire up your container (in `odoo` directory)

   .. code-block:: sh

      docker-compose up -d odoo

#. Open a web browser and navigate the URL you have set up in your `docker-compose.yml`
   file (http://127.0.0.1:8069 in this particular example)
#. Create a new database
#. Update the addons list in your database (Menu `Apps > Update Apps List` in developer mode)
#. Install the `Business Requirements` modules in menu `Apps`.

You can improve your new Odoo docker environment (add parameters, change default
passwords etc.) following this `documentation <https://github.com/Elico-Corp/odoo-docker>`_

Now what?
---------
Check the `Official Documentation <https://www.odoo.com/documentation/12.0>`_ to start using Odoo and developing your own modules.
