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
        readonly=True
    )
    dlv_description = fields.Text('Deliverable Description', readonly=True)
    dlv_product = fields.Many2one('product.product',
                                  'Deliverable Product',
                                  readonly=True)
    res_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='UoM',
        readonly=True
    )
    res_description = fields.Text('Resource Description', readonly=True)
    res_product = fields.Many2one('product.product',
                                  'Resource Product',
                                  readonly=True)
    resource_type = fields.Selection(
        [('task', 'Task'), ('procurement', 'Procurement')], 'Resource Type',
        readonly=True
    )
    br_count = fields.Integer('BR Count', readonly=True)
    dlv_count = fields.Integer('Deliverable Count', readonly=True)
    res_count = fields.Integer('Resource Count', readonly=True)
    dlv_qty = fields.Float('Deliverable Qty', readonly=True)
    res_qty = fields.Float('Resource Qty', readonly=True)
    sale_price = fields.Float('Sale Price', readonly=True)
    total_revenue = fields.Float('Total Revenue', readonly=True)
    avg_price = fields.Float('Avg Price', readonly=True)
    total_cost = fields.Float('Total Cost', readonly=True)
    gross_profit = fields.Float('Gross Profit', readonly=True)

    def _select(self):
        select_str = """SELECT ROW_NUMBER() OVER (ORDER BY brd.id) AS id,
            CONCAT('[',br.name,']', br.description) AS br_name,
            br.responsible_id,
            br.partner_id,
            br.project_id,
            br.priority,
            br.state,
            brs.resource_type,
            brd.name AS dlv_description,
            brd.product_id AS dlv_product,
            brs.product_id AS res_product,
            brs.uom_id AS res_uom_id,
            COUNT(br.id) AS br_count,
            COUNT(brd.id) AS dlv_count,
            COUNT(brs.id) AS res_count,
            SUM(brs.qty) AS res_qty,
            SUM(brd.qty) AS dlv_qty,
            SUM((brd.sale_price_unit * brd.qty) / brd.qty) AS sale_price,
            SUM(brd.sale_price_unit * brd.qty) AS total_revenue,
            SUM((brs.unit_price * brs.qty) / brd.qty) AS avg_price,
            SUM(brs.unit_price * brs.qty) AS total_cost,
            SUM((brd.sale_price_unit * brd.qty) - (brs.unit_price * brs.qty))
                AS gross_profit
        """
        return select_str

    def _from(self):
        from_str = """FROM business_requirement_resource brs
            LEFT JOIN business_requirement br ON
                br.id=brs.business_requirement_id
            LEFT JOIN business_requirement_deliverable brd ON
            brd.id=brs.business_requirement_deliverable_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """GROUP BY
                brd.id,
                br_name,
                dlv_description,
                res_product,
                dlv_product,
                br.responsible_id,
                br.partner_id,
                br.project_id,
                br.priority,
                br.state,
                brs.resource_type,
                res_uom_id
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s AS (
            %s %s %s
            )""" % (self._table, self._select(), self._from(),
                    self._group_by()))
