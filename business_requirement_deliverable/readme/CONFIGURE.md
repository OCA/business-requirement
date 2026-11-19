## Users

Only the users with the *Estimation* access of the *Business
Requirement Cost* privilege can see the pricelist, the sales prices and
the revenue of the business requirements and their deliverables. To
give it to a user, go to *Settings > Users & Companies > Users*, open
the user and, in the *Access Rights* tab, set *Business Requirement
Cost* to *Estimation*.

## Master project

You can define a master project linked to the business requirement.
Default Customer from the project will be used to populate the BR. The
customer can be changed if necessary.

## Valuation of the Deliverable and Resources lines

When writing a BR the user has the possibility to add Deliverable and
Resources lines. To value the Deliverable lines, you can specify an
estimation price list in the customer, which will be used in 2 main
places:

- In Deliverable lines if the deliverable product is in pricelist
- In Resource lines if you want to value your deliverable from the
  resources

NB: Here is the way Odoo will get a price in Deliverable and Resources
Lines:

1.  If the Estimation Pricelist field is not empty use the Estimation
    pricelist
2.  If empty, use the standard customer pricelist field
3.  If no pricelist available (for example no customer defined in the
    project), use the product Sales price.
