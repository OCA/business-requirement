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
    partner_id = fields.Many2one('res.partner', 'Customer',
                                 readonly=True)
    project_id = fields.Many2one('project.project', 'Master Project',
                                 readonly=True)
    res_product = fields.Many2one('product.product', 'Res Product',
                                  readonly=True)
    hr_timesheet_product = fields.Many2one('product.product',
                                           'HR Timesheet Product',
                                           readonly=True)
    planned_time_in_rl = fields.Float('Planned Time', readonly=True)
    product_cost_from_rl = fields.Float('Unit Cost', readonly=True)
    planned_value = fields.Float('Planned Value', readonly=True)
    actual_time_in_timesheet = fields.Float('Actual Time',
                                            readonly=True)
    product_cost_from_timesheet_product =\
        fields.Float('Act. Unit Cost',
                     readonly=True)
    actual_cost = fields.Float('Actual Cost', readonly=True)
    variance = fields.Float('Variance', readonly=True)
    per_variances = fields.Float('% Variance', readonly=True)
    remaining_hours = fields.Float('Remaining time', readonly=True)
    total_expected_time = fields.Float('Total Exp. time', readonly=True)
    project_completion = fields.Float('% Completion', readonly=True)
    earned_value = fields.Float('Earned Value', readonly=True)

    def _select(self):
        select_str = """
            SELECT
                br.id,
                CONCAT(br.name,'[',br.description,']') as name,
                br.state AS state,
                br.partner_id AS partner_id,
                br.project_id AS project_id,
                ptm.id AS hr_timesheet_product,
                SUM(res.qty) AS planned_time_in_rl,
                SUM(res.unit_price) AS product_cost_from_rl,
                (SUM(res.qty) * SUM(res.unit_price)) AS planned_value,
                (SELECT
                     SUM(pt.effective_hours)
                 FROM
                     project_task pt
                 WHERE
                     pt.business_requirement_id = br.id)
                AS actual_time_in_timesheet,
                (ptm.list_price) AS product_cost_from_timesheet_product,
                ((SELECT
                      SUM(pt.effective_hours)
                  FROM
                      project_task pt
                  WHERE
                      pt.business_requirement_id = br.id) * ptm.list_price)
                AS actual_cost,
                CASE
                    WHEN (SELECT
                              SUM(pt.effective_hours)
                          FROM
                              project_task pt
                          WHERE
                              pt.business_requirement_id = br.id) > 0
                    THEN
                        (((SELECT
                               SUM(pt.effective_hours)
                           FROM
                               project_task pt
                           WHERE
                               pt.business_requirement_id = br.id
                           ) * ptm.list_price) - (SUM(res.qty
                           ) * SUM(res.unit_price)))
                ElSE 0.0 END AS variance,
                CASE
                    WHEN
                        (SELECT
                            SUM(pt.effective_hours)
                         FROM
                             project_task pt
                         WHERE
                             pt.business_requirement_id = br.id) > 0
                    THEN
                        CASE
                            WHEN
                              SUM(res.unit_price) <> 0
                            THEN
                                abs(((SELECT SUM(pt.effective_hours)
                                FROM
                                    project_task pt
                                WHERE
                                    pt.business_requirement_id = br.id
                                ) * ptm.list_price) - (SUM(res.qty
                                ) * SUM(res.unit_price))) /
                                SUM(res.unit_price)
                            ELSE
                                0.0
                            END
                ElSE 0.0 END AS per_variances,
                CASE
                    WHEN
                        (SELECT
                            SUM(pt.effective_hours)
                         FROM
                             project_task pt
                         WHERE
                             pt.business_requirement_id = br.id) > 0
                    THEN
                        (SELECT
                            SUM(pt.remaining_hours)
                         FROM
                             project_task pt
                        WHERE pt.business_requirement_id = br.id)
                ElSE 0.0 END AS remaining_hours,
                CASE
                    WHEN
                        (SELECT
                            SUM(pt.effective_hours)
                         FROM
                             project_task pt
                         WHERE
                             pt.business_requirement_id = br.id) > 0
                    THEN
                        ((SELECT
                            SUM(pt.effective_hours)
                          FROM
                              project_task pt
                          WHERE
                              pt.business_requirement_id = br.id
                          ) + (SELECT
                                   SUM(pt.remaining_hours)
                               FROM
                                   project_task pt
                               WHERE
                                   pt.business_requirement_id = br.id))
                ElSE 0.0 END AS total_expected_time,
                CASE
                    WHEN ((SELECT
                               SUM(pt.remaining_hours)
                           FROM
                               project_task pt
                           WHERE
                               pt.business_requirement_id = br.id)) > 0
                    THEN
                        CASE
                            WHEN
                                (SELECT
                                    SUM(pt.effective_hours)
                                 FROM
                                     project_task pt
                                 WHERE
                                     pt.business_requirement_id = br.id) > 0
                            THEN
                                ((SELECT
                                    SUM(pt.effective_hours)
                                 FROM
                                    project_task pt
                                 WHERE
                                    pt.business_requirement_id = br.id
                                  ) / ((SELECT
                                      SUM(pt.effective_hours)
                                  FROM
                                      project_task pt
                                  WHERE
                                      pt.business_requirement_id = br.id
                                 ) + (SELECT
                                          SUM(pt.remaining_hours)
                                      FROM
                                          project_task pt
                                      WHERE
                                          pt.business_requirement_id = br.id)
                                ) * 100) ELSE 0.0 END
                ElSE 0.0 END AS project_completion,
                CASE
                    WHEN
                        (SELECT
                             SUM(pt.remaining_hours)
                         FROM
                             project_task pt
                         WHERE
                             pt.business_requirement_id = br.id) > 0
                    THEN
                        CASE
                            WHEN
                                (SELECT
                                    SUM(pt.effective_hours)
                                 FROM
                                     project_task pt
                                 WHERE
                                     pt.business_requirement_id = br.id) > 0
                            THEN
                                ((SUM(res.qty) * SUM(res.unit_price)
                                ) * ((SELECT
                                          SUM(pt.effective_hours)
                                      FROM
                                          project_task pt
                                      WHERE
                                          pt.business_requirement_id = br.id
                                ) / ((SELECT
                                          SUM(pt.effective_hours)
                                      FROM
                                          project_task pt
                                      WHERE
                                          pt.business_requirement_id = br.id
                                ) + (SELECT
                                        SUM(pt.remaining_hours)
                                    FROM
                                        project_task pt
                                    WHERE
                                        pt.business_requirement_id = br.id))))
                            ElSE 0.0 END
                ElSE 0.0 END AS earned_value
        """
        return select_str

    def _from(self):
        from_str = """
            business_requirement br
                LEFT JOIN business_requirement_deliverable dlv
                    ON dlv.business_requirement_id = br.id
                LEFT JOIN business_requirement_resource res
                    ON res.business_requirement_deliverable_id = dlv.id
                    JOIN product_template as ptm
                        ON ptm.id = res.product_id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                br.id,ptm.id
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
