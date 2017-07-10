# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import tools
from openerp import fields, models


class BusinessRequirementDeliverableCostReport(models.Model):
    _name = "business.requirement.deliverable.cost.report"
    _description = "Deliverable Cost Report"
    _auto = False

    br_name = fields.Char('Bus. Requirement', readonly=True)
    responsible_id = fields.Many2one('res.users', 'Responsible', readonly=True)
    partner_id = fields.Many2one('res.partner',
                                 'Customer',
                                 readonly=True)
    project_id = fields.Many2one('project.project',
                                 'Master Project',
                                 readonly=True)
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'),
                                 ('2', 'High')],
                                'Priority',
                                readonly=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('approved', 'Approved'),
         ('stakeholder_approval', 'Stakeholder Approval'),
         ('in_progress', 'In progress'),
         ('done', 'Done'),
         ('cancel', 'Cancel'),
         ('drop', 'Drop'),
         ],
        'Status',
        readonly=True,
    )
    dlv_description = fields.Text('Deliverable Description', readonly=True)
    dlv_product = fields.Many2one('product.product',
                                  'Deliverable Product',
                                  readonly=True)
    res_description = fields.Text('Resource Description', readonly=True)
    res_product = fields.Many2one('product.product',
                                  'Resource Product',
                                  readonly=True)
    br_count = fields.Integer('BR Count', readonly=True)
    dlv_count = fields.Integer('Deliverable Count', readonly=True)
    res_count = fields.Integer('Resource Count', readonly=True)
    dlv_qty = fields.Float('Deliverable Qty', readonly=True)
    res_qty = fields.Float('Resource Qty', readonly=True)
    sale_price = fields.Float('Sale Price', readonly=True)
    total_revenue = fields.Float('Total Revenue', readonly=True)
    cost_price = fields.Float('Cost price', readonly=True)
    total_cost = fields.Float('Total cost', readonly=True)
    gross_profit = fields.Float('Gross Profit', readonly=True)

    def _select(self):
        select_str = """
            SELECT
                br.id,
                (select CONCAT('[',name,']', description) from
                business_requirement where id=br.id) AS br_name,
                br.responsible_id,
                br.partner_id,
                br.project_id,
                br.priority,
                br.state,
                dlv.product_id as dlv_product,
                dlv.name as dlv_description,
                (select business_requirement_deliverable_id from
                business_requirement_resource where id=dlv.id) as res_product,
                res.name as res_description,
                count(distinct br.id) as br_count,
                count(distinct dlv.id) as dlv_count,
                count(distinct res.id) as res_count,
                res.qty as res_qty,
                dlv.qty as dlv_qty,
                dlv.unit_price as sale_price,
                (dlv.unit_price * dlv.qty) as total_revenue,
                res.unit_price as cost_price,
                (res.unit_price * res.qty) as total_cost,
                ((dlv.unit_price * dlv.qty) - (res.unit_price * res.qty))
                as gross_profit
        """
        return select_str

    def _from(self):
        from_str = """
            business_requirement br
            FULL OUTER JOIN business_requirement_deliverable dlv
                ON br.id = dlv.business_requirement_id
            FULL OUTER JOIN business_requirement_resource res
                ON res.business_requirement_deliverable_id = dlv.id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                dlv.id, br.id, res.id
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(),
                    self._group_by()))
