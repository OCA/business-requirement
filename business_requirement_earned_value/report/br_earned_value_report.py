# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import tools
from openerp import fields, models


class BusinessRequirementEarnedValueReport(models.Model):
    _name = "business.requirement.earned.value.report"
    _description = "Earned Value Report"
    _auto = False

    name = fields.Char('Name', readonly=True)
    description = fields.Char('Description', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer',
                                 readonly=True)
    project_id = fields.Many2one('project.project', 'Master Project',
                                 readonly=True)
    res_product = fields.Many2one('product.product', 'Res Product',
                                  readonly=True)
    hr_timesheet_product = fields.Many2one('product.product',
                                           'HR Timesheet Product',
                                           readonly=True)
    planned_time_in_rl = fields.Float('Planned time in RL', readonly=True)
    product_cost_from_rl = fields.Float('Product Cost from RL', readonly=True)
    planned_value = fields.Float('Planned Value', readonly=True)
    actual_time_in_timesheet = fields.Float('Actual time in Timesheet',
                                            readonly=True)
    product_cost_from_timesheet_product =\
        fields.Float('Product Cost from Timesheet product',
                     readonly=True)
    actual_cost = fields.Float('Actual Cost', readonly=True)
    variance = fields.Float('Variance', readonly=True)
    per_variances = fields.Float('% Variance', readonly=True)
    remaining_hours = fields.Float('Remaining time', readonly=True)
    total_expected_time = fields.Float('Total expected time', readonly=True)
    project_completion = fields.Float('Project Completion', readonly=True)
    earned_value = fields.Float('Earned Value', readonly=True)

    def init(self, cr):
        tools.drop_view_if_exists(cr,
                                  'business_requirement_earned_value_report')
        cr.execute("""
            CREATE VIEW business_requirement_earned_value_report AS (
            SELECT 
                br.id,
                br.name as name,
                br.description as description,
                br.partner_id as partner_id,
                br.project_id as project_id,
                ptm.id as hr_timesheet_product,
                sum(res.qty) as planned_time_in_rl,
                sum(res.unit_price) as product_cost_from_rl,
                (sum(res.qty) * sum(res.unit_price)) as planned_value,
                (pt.effective_hours) as actual_time_in_timesheet,
                (ptm.list_price) as product_cost_from_timesheet_product,
                (pt.effective_hours * ptm.list_price)
                as actual_cost,
                abs((pt.effective_hours * ptm.list_price
                ) - (sum(res.qty) * sum(res.unit_price)))
                as variance,
                (abs((pt.effective_hours * ptm.list_price
                ) - (sum(res.qty) * sum(res.unit_price))) /
                sum(res.unit_price)) as per_variances,
                pt.remaining_hours as remaining_hours,
                (pt.effective_hours + pt.remaining_hours)
                as total_expected_time,
                CASE WHEN (pt.remaining_hours) > 0 THEN
                (pt.effective_hours / (pt.effective_hours + pt.remaining_hours
                ))
                ElSE 0.0 END as project_completion,
                CASE WHEN (pt.remaining_hours) > 0 THEN
                (((sum(res.qty) * (sum(res.unit_price) * sum(res.qty))
                ) * (pt.effective_hours /
                pt.effective_hours + pt.remaining_hours))) ElSE 0.0 END
                as earned_value
            From    
                business_requirement br
                LEFT JOIN business_requirement_deliverable dlv
                ON dlv.business_requirement_id = br.id
                LEFT JOIN business_requirement_resource res
                ON res.business_requirement_deliverable_id = dlv.id
                LEFT JOIN  project_task pt 
                ON pt.business_requirement_id = br.id 
                JOIN product_template as ptm ON ptm.id = res.product_id
            group by 
                br.id,pt.id,ptm.id
            )""")
