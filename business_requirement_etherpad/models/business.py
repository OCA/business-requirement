# © 2016-2019 Elico Corp (https://www.elico-corp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class BusinessRequirement(models.Model):
    _name = "business.requirement"
    _inherit = ["business.requirement", 'pad.common']

    notes = fields.Char('Notes', pad_content_field='notes')
