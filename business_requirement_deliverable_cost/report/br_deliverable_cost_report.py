# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import tools
from openerp import fields, models


class DeliverableCostReport(models.Model):
    _name = "deliverable.cost.report"
    _description = "Deliverable Cost Report"
    _auto = False

    name = fields.Char('Name', readonly=True)
    description = fields.Char('Description', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', readonly=True)
    project_id = fields.Many2one('project.project', 'Master Project',
                                 readonly=True)
    change_request = fields.Boolean('Change Request?', readonly=True)
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'),
                                 ('2', 'High')], 'Priority', readonly=True)
    dlv_product = fields.Many2one('product.product', 'Dlv Product',
                                  readonly=True)
    dlv_description = fields.Text('Deliverable Description', readonly=True)
    res_product = fields.Many2one('product.product', 'Res Product',
                                  readonly=True)
    res_description = fields.Text('Resource Description', readonly=True)
    br_count = fields.Integer('BR Count', readonly=True)
    dlv_count = fields.Integer('Deliverable Count', readonly=True)
    res_count = fields.Integer('Resource Count', readonly=True)
    dlv_qty = fields.Float('Deliverable Qty', readonly=True)
    res_qty = fields.Float('Resource Qty', readonly=True)
    sale_price = fields.Float('Sale Price', readonly=True)
    total_revenue = fields.Float('Total Revenue', readonly=True)
    cost_price = fields.Float('Cost price', readonly=True)
    total_cost = fields.Float('Total cost', readonly=True)

    def init(self, cr):
            tools.drop_view_if_exists(cr, 'deliverable_cost_report')
            cr.execute("""
                CREATE VIEW deliverable_cost_report AS (
                    SELECT
                    br.id,
                    br.name,
                    br.description,
                    br.partner_id,
                    br.project_id,
                    br.change_request,
                    br.priority,
                    dlv.product_id as dlv_product,
                    dlv.name as dlv_description,
                    res.product_id as res_product,
                    res.name as res_description,
                    count(distinct br.id) as br_count,
                    count(distinct dlv.id) as dlv_count,
                    count(distinct res.id) as res_count,
                    res.qty as res_qty,
                    dlv.qty as dlv_qty,
                    dlv.unit_price as sale_price,
                    (dlv.unit_price * dlv.qty) as total_revenue,
                    res.unit_price as cost_price,
                    (res.unit_price * res.qty) as total_cost
                    FROM business_requirement br
                    FULL OUTER JOIN business_requirement_deliverable dlv
                    ON br.id = dlv.business_requirement_id
                    FULL OUTER JOIN business_requirement_resource res
                    ON res.business_requirement_deliverable_id = dlv.id
                    Group By dlv.id, br.id, res.id
                    )""")
