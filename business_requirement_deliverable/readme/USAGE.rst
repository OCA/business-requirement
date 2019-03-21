What are Deliverable Lines?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deliverable Lines (DL) contains products and services that will be delivered to the
customer. They are **customer oriented** and can be either physical or service products:

* Servers and procured goods
* Gap analysis services
* Module development services
* Training etc.

These are the products that will appear in the SO and that the customer/stakeholder will receive.

.. figure:: ../static/img/bus_req_deliverable.png
   :width: 600 px
   :alt: Business Requirement Deliverable lines

What are Resources Lines?
~~~~~~~~~~~~~~~~~~~~~~~~~

Resources Lines (RL) are the different services or physical goods needed to achieve one deliverable:

* Service tasks (Development, consultant etc.)
* Procurement of other physical goods (server, etc.)
* Procurement of other virtual goods (templates, sub-contracting, etc.)

RL depends on the DL or directly on BR (when a task is not linked to a specific deliverable such
as project management)

..  figure:: ../static/img/bus_req_resource.png
   :width: 600 px
   :alt: Business Requirement Resources lines

What is the difference between Deliverable and Resources?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

=========== ======================================================== ========================================================
Concept     Deliverable is:                                          Resources are:
=========== ======================================================== ========================================================
Target      Provided to the customer (“Functioning Website”)         Executed internally (“Server+CSS modifications”)
Valuation   Valued at Customer Sales Price                           Valued at Cost Price
Usage       Used in Sales Quotations                                 Used in tasks for Projects or procurement management
=========== ======================================================== ========================================================

Business Requirement contains Deliverable lines and Deliverable line contains Resource lines.

Example of a structure:

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

Adding Deliverable lines to the business Requirement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#. In the BR, you can add as many deliverable lines as necessary. Price of the deliverable
   lines will depend on the pricelist(s) in customer.
#. Once the deliverable lines are created you can create as many resources lines as necessary
   in each DL.
#. in RL you can already assign the responsible of the task if necessary

.. figure:: ../static/img/bus_req_deliverable2.png
   :width: 600 px
   :alt: Inputing the deliverables and resources lines


Valuation of Business Requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Value of the BR is the sum of the value of all deliverable lines.

Deliverable in the BR are valued based on the BR pricelist or product sales price:

#. If the Estimation Pricelist field is not empty in partner prefill the BR with
   the Estimation pricelist
#. If empty, prefill the BR with the standard customer pricelist field
#. If no pricelist available (for example no customer defined in the project or BR), use
   the product Sales price.