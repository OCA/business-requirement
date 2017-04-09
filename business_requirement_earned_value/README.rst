.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3


===============================
Earned Value Management Report
===============================

Introduction
============

This module is part of a set of modules (`Business Requirements <https://github.com/OCA/business-requirement/blob/8.0/README.md>`_).


This module introduces **Earned Value Management report** based on the information 
from the Business Requirements Resources and Deliverable lines. You can check the 
following resources for more information about EVM:

* `[RFC] Earned Value Management Report <https://github.com/OCA/business-requirement/issues/81>`_
* `Earned Value Management introduction <https://www.humphreys-assoc.com/evms/basic-concepts-earned-value-management-evm-ta-a-74.html>`_
* `Wikipedia Entry <https://en.wikipedia.org/wiki/Earned_value_management>`_

Configuration
=============

To fully be able to use the report, the following information must be properly maintained:

* Cost price in the products associated to resources
* Resources lines should contain valid cost and total cost.
* Employees should contain a valid resource product (comparable to the one in the Resource lines)
* The time spent on Timesheets should be properly recorded

Usage
=====

#. In the Business requirement, you add Deliverable Lines as necessary,with the
   corresponding Resources lines. 
#. When the BR is validated the project should be created so that the users can
   manage their tasks.
#. When the users spend time on a given task they should input their timesheets
   accordingly in the task.

.. note::
  When creating new tasks, the related BR should be set up properly in the task in 
  order to be properly accounted
  
.. figure:: static/img/bus_req_category.png
   :width: 600 px
   :alt: Inputing the deliverables and resources lines


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/222/8.0

Known issues / Roadmap
======================

* Needs timesheets on the tasks related to BR. In the future we might think of a way
  to input TS on project directly


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/business-requirement/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Eric Caudal <eric.caudal@elico-corp.com>

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
