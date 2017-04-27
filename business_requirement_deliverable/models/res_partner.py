# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_product_estimation_pricelist = fields.Many2one(
        string='Estimation Pricelist',
        comodel_name='product.pricelist',
        company_dependent=True,
        help="""Pricelist used for the estimation of the Business Requirements
        Deliverables linked to this Customer.
        Currency of the Deliverables will be the one from the pricelist.""")

    def _commercial_fields(self, cr, uid, context=None):
        return super(
            ResPartner,
            self
        )._commercial_fields(
            cr,
            uid,
            context=context
        ) + ['property_product_estimation_pricelist']
