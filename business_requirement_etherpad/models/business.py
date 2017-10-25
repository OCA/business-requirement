# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class BusinessRequirement(models.Model):
    _name = "business.requirement"
    _inherit = ["business.requirement", 'pad.common']

    notes = fields.Char('Notes', pad_content_field='notes')
