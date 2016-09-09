.. figure:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3


====================
Business Requirement
====================

Introduction
^^^^^^^^^^^^

This module is part of a set ("Business Requirement").
The Business Requirements features start as independent entities, and can be 
used as standalone.

Additional modules integrate them with other business areas, such as Sales, 
Procurement, Project or Analytic Accounting. For example:

* Sales Quotation can have an estimation supported by a BR analysis
* Project Tasks can be related to the BRs they implement or support
* Procurement and purchase can be generated out of the BR

.. figure:: static/img/bus_req_tree.png
   :width: 600 px
   :alt: Business Requirement List view

The following diagram gives a simplified view of the universe:

.. figure:: static/img/bus_req_module_diag.png
   :width: 600 px
   :alt: Business Requirement modules diagram

What is a Business Requirement?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Business requirement (BR) is the expression of a business need by a customer 
or internal project user. 
A BR can contain multiple different parts depending on the company needs:

* Customer Story: this is the requirement as expressed by the customer
* Scenario: How/where the current solution can provide a suitable scenario to 
  answer the customer story
* Gap: For the uncovered part of the scenario, elaborate the gap/need for specific 
  developments/setup
* Deliverables to be provided to the customer/user
* Resources necessary to achieve the deliverables
* Additional information (approval, cost control etc.)

These modules were originally design for the service/IT industry but the 
requirement management is generic and can apply to many cases/industries (customer 
or internal projects):

* Construction
* Trading (New product development)
* Business Consultancy
* IT development

What is the difference between a BR and CRM lead?

* CRM leads are sales oriented
* BR are project and workload estimation oriented

How to use this module?
^^^^^^^^^^^^^^^^^^^^^^^

This module adds the following features to the deliverable modules:

* Possibility to create default resource lines for a given product. This allows
  the user to have standard resource lines uploaded in the BR for deliverable 
  packages.

Installation
============

No specific steps required

Configuration
=============

Users
^^^^^

No special ACL set up

Default resources in Deliverable Product
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can create Deliverable products and add in them standard resource lines
expected to be added in the Business requirement by default.
Depending on the modules you are using for the business requirements, the 
content of the resources lines will reflect the expected resources lines in the 
BR.

.. figure:: static/img/bus_req_default.png
   :width: 600 px
   :alt: Set up your default resources lines.


Usage
=====

#. Prepare your deliverables in the Product menu and add the expected RL

#. Create a new BR and add the deliverable product in the deliverable line

#. Adapt the resources lines if necessary

.. figure:: static/img/bus_req_default2.png
   :width: 600 px
   :alt: The default resource lines are automatically added to your BR


.. figure:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/222/8.0

On product_template view add a new tab "Resources" with the resource lines management (You could add, delete or create new resources).

Known issues / Roadmap
======================

* Currently prices are not updated when the resource lines are uploaded in the 
  BR. => Add a button to recalculate Sales estimation prices in the Deliverable 
  line


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/
project/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Eric Caudal <eric.caudal@elico-corp.com>
* Victor M. Martin <victor.martin@elico-corp.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
