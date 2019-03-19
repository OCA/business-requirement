What is a Deliverable Line?
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

Resources Lines (RL) are the different tasks or procurements needed to achieve one deliverable:

* Service tasks (Development, consultant etc.)
* Procurement of other physical goods (server, etc.)
* Procurement of other virtual goods (templates, sub-contracting, etc.)

RL depends on the DL or directly on BR

..  figure:: ../static/img/bus_req_resource.png
   :width: 600 px
   :alt: Business Requirement Resources lines

What is the difference between Deliverable and Resources?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
