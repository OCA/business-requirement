# Copyright 2016-2019 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_product_estimation_pricelist = fields.Many2one(
        string='Estimation Pricelist',
        comodel_name='product.pricelist',
        company_dependent=True,
        help="""Pricelist used for the estimation of the Business Requirements
        Deliverables linked to this Customer.
        Currency of the Deliverables will be the one from the pricelist.""")

    @api.model
    def _commercial_fields(self):
        return super(ResPartner, self)._commercial_fields() + \
            ['property_product_estimation_pricelist']
