.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Business Requirement Deliverable CRM
====================================
Introduction
============

This module is part of a set of modules 
(`Business Requirements <https://github.com/OCA/business-requirement/blob/10.0/README.md>`_)

This module adds integration between the CRM and Business Requirement model:

* Possibility to link a CRM opportunity to a Master project
* Possibility to create a Sales Quotation based on the BR from a Master Project

Configuration
=============

Button to create the SQ in the opportunity is available for sales user or manager

Usage
=====

#. Link your master project in the CRM lead
#. Create one or several BR with deliverable lines in the master project.
#. Click on the button "Generate Quotation from Business Requirement" in the
   Opportunity
#. Select update existing or create new one
#. A quotation is created/updated based on the deliverable lines from all the 
   BR related to the master project

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/222/10.0


Known issues / Roadmap
======================

* Integration with online quotation: add the quotation template in the wizard
  (currently a workaround is to generate first the quotation, add the template
  and then regerenate the quotation)

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
* Alex Duan <alex.duan@elico-corp.com>
* Xie XiaoPeng <xie.xiaopeng@elico-corp.com>
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
