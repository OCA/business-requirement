.. figure:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
Business Requirement Deliverable
================================

Introduction
============

This module is part of a set of modules (`Business Requirements <https://github.com/OCA/business-requirement/blob/10.0/README.md>`_)

Two new concepts complement the main business requirements model:

* Deliverable lines
* Resource lines

A field for pricelist estimation is available in the partner to be used in Deliverable
and Resources lines valuation to customers.

What is a Deliverable Line?
---------------------------

Deliverable Lines (DL) contains products and services that will be delivered to the 
customer. They are **customer oriented** and can be either physical or service products:

* Servers and procured goods
* Gap analysis services
* Module development services
* Training etc.

These are the products that will appear in the SO and that the customer/stakeholder will receive.

.. figure:: ../business_requirement_deliverable/static/img/bus_req_deliverable.png
   :width: 600 px
   :alt: Business Requirement Deliverable lines


What are Resources Lines?
-------------------------

Resources Lines (RL) are the different tasks or procurements needed to achieve one deliverable:

* Service tasks (Development, consultant etc.)
* Procurement of other physical goods (server, etc.)
* Procurement of other virtual goods (templates, sub-contracting, etc.)

RL depends on the DL or directly on BR

..  figure:: ../business_requirement_deliverable/static/img/bus_req_resource.png
   :width: 600 px
   :alt: Business Requirement Resources lines

What is the difference between Deliverable and Resources?
---------------------------------------------------------

=========== ======================================================== ========================================================
Concept     Deliverables are:                                        Resources are:
=========== ======================================================== ========================================================
Target      Provided to the customer (“Functioning Website”)         Executed internally (“Server+CSS modifications”)
Valuation   Valued at Customer Sales Price                           Valued at Cost Price
Usage       Used in Sales Quotations                                 Used in Project management or procurement management
=========== ======================================================== ========================================================

Business Requirement contains Deliverable lines and Deliverable line contains Resource lines. Example of a structure:

::

    BR1
    |
    |- DL1
    |  |
    |  |- RL1
    |  |- RL2
    |  `- RL3
    |
    |- DL2
    |  |
    |  |- RL4
    |  |- RL5
    |  `- RL6
    |
    BR2
    |
    |- DL3
    |  |
    |  |- RL7
    |  `- RL8
    |
    |- DL4
    |  `- RL9



Installation
============

No specific steps required

Configuration
=============

Users
-----

Estimation Pricelist: user can see the Sales price and revenue of the BR.

Master project
--------------

You can define a master project linked to the business requirement. Default Customer 
from the project will be used to populate the BR. The customer can be changed if necessary.

Valuation of the Deliverable and Resources lines
------------------------------------------------
When writing a BR the user has the possibility to add Deliverable and Resources lines.
To value the Deliverable lines, you can specify an estimation price list in the customer,
which will be used in 2 main places:

* In Deliverable lines if the deliverable product is in pricelist
* In Resource lines if you want to value your deliverable from the resources

NB: Here is the way Odoo will get a price in Deliverable and Resources Lines:

#. If the Estimation Pricelist field is not empty use the Estimation pricelist 
#. If empty, use the standard customer pricelist field
#. If no pricelist available (for example no customer defined in the project), use
   the product Sales price.


Usage
=====

#. In the BR, you can add as many deliverable lines as necessary. Price of the deliverable 
   lines will depend on the pricelist(s) in customer.

#. Once the deliverable lines are created you can create as many resources lines as necessary
   in each DL. Cost price of the product will apply

#. in RL you can already assign the responsible of the task if necessary

.. figure:: ../business_requirement_deliverable/static/img/bus_req_deliverable2.png
   :width: 600 px
   :alt: Inputing the deliverables and resources lines


.. figure:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/222/10.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/business-requirement/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.

Known issues / Roadmap
======================
* As of version 10.0.1.0.0, the estimation pricelist has been moved from Project to
  Partner object. There is no migration script for the change and the data will 
  have to be migrated manually.
Credits
=======

Contributors
------------

* Eric Caudal <eric.caudal@elico-corp.com>
* Alex Duan <alex.duan@elico-corp.com>
* Xie XiaoPeng <xie.xiaopeng@elico-corp.com>
* Victor M. Martin <victor.martin@elico-corp.com>

Maintainer
----------

.. figure:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
