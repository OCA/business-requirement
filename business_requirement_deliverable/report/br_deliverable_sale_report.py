# -*- coding: utf-8 -*-
# © 2016 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import tools
from openerp import fields, models


class BusinessRequirementDeliverableSaleReport(models.Model):
    _name = "business.requirement.deliverable.sale.report"
    _description = "Deliverable Sales Report"
    _auto = False

    br_name = fields.Char('Bus. Requirement', readonly=True)
    responsible_id = fields.Many2one('res.users', 'Responsible', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', readonly=True)
    project_id = fields.Many2one('project.project', 'Master Project',
                                 readonly=True)
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High')],
                                'Priority', readonly=True)
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
    dlv_product = fields.Many2one('product.product', 'Deliverable Product',
                                  readonly=True)
    res_description = fields.Text('Resource Description', readonly=True)
    res_product = fields.Many2one('product.product', 'Resource Product',
                                  readonly=True)
    br_count = fields.Integer('BR Count', readonly=True)
    dlv_count = fields.Integer('Deliverable Count', readonly=True)
    res_count = fields.Integer('Resource Count', readonly=True)
    dlv_qty = fields.Float('Deliverable Qty', readonly=True)
    res_qty = fields.Float('Resource Qty', readonly=True)
    sale_price = fields.Float('Sale Price', readonly=True)
    total_revenue = fields.Float('Total Revenue', readonly=True)

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
                (select name from business_requirement_deliverable dlv where
                id = br.id) as dlv_description,
                (select product_id from business_requirement_deliverable dlv
                where id = br.id) as dlv_product,
                (select product_id from business_requirement_resource where id
                = br.id) as res_product,
                (select name from business_requirement_resource where id =
                br.id) as res_description,
                (select count(id) from business_requirement) as br_count,
                (select count(id) from business_requirement_deliverable)
                as dlv_count,
                (select count(*) from business_requirement_resource res
                where res.business_requirement_id = br.id) as res_count,
                (select sum(qty) from business_requirement_resource)
                as res_qty,
                dlv.qty as dlv_qty,
                (select sale_price_unit from business_requirement_deliverable
                where id = br.id) as sale_price,
                ((select sale_price_unit from business_requirement_deliverable
                where id = br.id) * dlv.qty) as total_revenue
        """
        return select_str

    def _from(self):
        from_str = """
            FROM
            business_requirement br,
            business_requirement_deliverable dlv,
            business_requirement_resource res
            where br.id = dlv.business_requirement_id and
                    br.id = res.business_requirement_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                br.id,dlv.qty
        """
        return group_by_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s %s %s
            )""" % (self._table, self._select(), self._from(),
                    self._group_by()))
