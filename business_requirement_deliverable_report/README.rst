.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================================
Business Requirement Deliverable Report Module
==============================================

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

|image7|

.. |image7| image:: business_requirement_deliverable_report/static/img/bus_req_tree.png
   :width: 800 px
   :alt: Business Requirement List view

The following diagram gives a simplified view of the universe:

|image11|

.. |image11| image:: business_requirement_deliverable_report/static/img/bus_req_module_diag.png
   :width: 800 px
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

These modules were originally designed for the service/IT industry but the 
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

This module adds multiple printouts to the deliverable modules:

* Basic Business requirement printout: including header, Customer story, 
  scenario and gap analysis

|image3|

.. |image3| image:: business_requirement_deliverable_report/static/img/bus_req_report1.png
   :width: 800 px
   :alt: Basic Business requirement printout 

* Deliverable printout: above printout including the deliverable lines at 
  sales price

|image4|

.. |image4| image:: business_requirement_deliverable_report/static/img/bus_req_report2.png
   :width: 800 px
   :alt: Deliverable printout (details)

* Resource Printout: above printout including the resource lines with 
  expected quantity

|image5|

.. |image5| image:: business_requirement_deliverable_report/static/img/bus_req_report3.png
   :width: 800 px
   :alt: Resource Printout (details)


Installation
============

No specific installation required

Configuration
=============

No specific configuration required

Usage
=====

Select the BR and print desired report

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/140/8.0


Known issues / Roadmap
======================

* add currency and multiple formatting improvements

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/business-requirement/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Evan Li li.aiwen@elico-corp.com


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
