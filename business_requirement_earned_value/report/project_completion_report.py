# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, tools


class ProjectCompletionReport(models.Model):
    """
        Project Completion Report
    """
    _name = "project.completion.report"
    _auto = False
    _description = "Project Completion Report"
    _rec_name = 'activity_name'

    id = fields.Integer('ID', readonly=True)
    partner_id = fields.Many2one(
        'res.partner', 'Stakeholder', readonly=True)
    br_id = fields.Many2one(
        'business.requirement', 'Bus. Req.',
        readonly=True, help="Business Requirement")
    master_project_id = fields.Many2one(
        'project.project', 'Master Project', readonly=True,
        help="Master Project of the Business Requirement")
    project_id = fields.Many2one(
        'project.project', 'Project', readonly=True)
    account_id = fields.Many2one(
        'account.analytic.account', 'Analytic Account', readonly=True)
    activity_type = fields.Selection(
        [
            ('task', 'Task'),
            ('issue', 'Issue'),
        ], 'Type', readonly=True,
        help="Type is used to separate Tasks and Issues")
    activity_id = fields.Char(
        'Activity ID', readonly=True, help="Task ID or Issue ID")
    activity_name = fields.Char(
        'Activity Name', readonly=True, help="Task name or Issue name")
    user_id = fields.Many2one(
        'res.users',
        'Assignee',
        readonly=True,
        help="Assignee is not necessarily the one who input the Timesheets")
    activity_stage_id = fields.Many2one(
        'project.task.type', 'Activity stage',
        readonly=True, help="Activity Stage")
    # FIXME if BR resource UoM is not hours, `qty` needs to be converted
    estimated_hours = fields.Float(
        'Est. time', digits=(16, 2), readonly=True,
        help="Estimated time (from BR)")
    planned_hours = fields.Float(
        'Init. time', digits=(16, 2), readonly=True,
        help="Initial time (from Task)")
    total_tms = fields.Float(
        'Time spent', digits=(16, 2), readonly=True,
        help="Time spent on timesheet")
    remaining_hours = fields.Float(
        'Remain. time', digits=(16, 2), readonly=True,
        help="Remaining time")
    total_hours = fields.Float('Total time', digits=(16, 2), readonly=True)
    variance = fields.Float(
        'Variance', digits=(16, 2), readonly=True,
        help="Variance between Estimated time (from BR) and Total time"
    )
    br_status = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('approved', 'Approved'),
         ('stakeholder_approval', 'Stakeholder Approval'),
         ('in_progress', 'In progress'),
         ('done', 'Done'),
         ('cancel', 'Cancel'),
         ('drop', 'Drop')],
        string='BR status',
    )
    task_category_id = fields.Many2one(
        'project.category', string='Task Category'
    )
    project_state = fields.Char(
        'Project state', readonly=True, help="Project State")
    br_kanban_state = fields.Selection(
        [
            ('normal', 'In Progress'),
            ('on_hold', 'On Hold'),
            ('done', 'Ready for next stage')
        ],
        'BR Kanban State',
        required=False,
        default='normal'
    )
    task_kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready for next stage'),
        ('blocked', 'Blocked')
    ], string='Activity Kanban State',
    )
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'),
                                 ('2', 'High')],
                                'Priority', readonly=True)
    date_deadline = fields.Date(string='Deadline')

    @api.model_cr
    def init(self):
        """
            Project Completion Report
        """
        tools.drop_view_if_exists(self._cr, 'project_completion_report')
        self._cr.execute("""
                CREATE OR REPLACE VIEW project_completion_report AS (
                    -- Since Odoo requires a unique ID for each line and since
                    -- some issues and tasks might share the same ID, use the
                    -- row number to ensure each row has a unique ID
                    SELECT
                        row_number() OVER (ORDER BY q.activity_id) AS id, q.*
                    FROM
                    (
                        (
                            SELECT
                                a.partner_id,
                                b.project_id AS master_project_id,
                                b.id AS br_id,
                                b.state AS br_status,
                                t.categ_id AS task_category_id,
                                CASE WHEN p.active = True THEN 'Active'
                                WHEN p.active=False THEN 'Archived'
                                END AS project_state,
                                p.id AS project_id,
                                a.id AS account_id,
                                'task' AS activity_type,
                                t.id AS activity_id,
                                t.name AS activity_name,
                                t.user_id,
                                t.stage_id AS activity_stage_id,
                                CASE WHEN r.uom_id=(
                                select res_id from ir_model_data
                                where name='product_uom_hour')
                                THEN COALESCE(r.qty, 0)
                                WHEN r.uom_id=(
                                select res_id from ir_model_data where
                                name='product_uom_day')
                                 THEN COALESCE(r.qty*8, 0)
                                END AS estimated_hours,
                                t.planned_hours,
                                COALESCE(SUM(tw.unit_amount), 0) AS total_tms,
                                t.remaining_hours,
                                b.kanban_state as br_kanban_state,
                                t.kanban_state as task_kanban_state,
                                t.priority as priority,
                                t.date_deadline as date_deadline,
                                COALESCE(SUM(tw.unit_amount), 0)
                                    + t.remaining_hours AS total_hours,
                                CASE WHEN r.uom_id=(
                                select res_id from ir_model_data
                                where name='product_uom_hour')
                                THEN COALESCE(SUM(tw.unit_amount), 0)
                                    + t.remaining_hours - COALESCE(r.qty, 0)
                                WHEN r.uom_id=(
                                select res_id from ir_model_data where
                                name='product_uom_day')
                                THEN COALESCE(SUM(tw.unit_amount), 0)
                                    + t.remaining_hours - COALESCE(r.qty*8, 0)
                                END AS variance
                            FROM
                                project_project p
                                -- Link with the analytic account
                                INNER JOIN account_analytic_account a
                                    ON a.id = p.analytic_account_id
                                -- Link with the task
                                INNER JOIN project_task t
                                ON t.project_id = p.id
                                -- Link with the timesheet
                                LEFT OUTER JOIN account_analytic_line tw
                                    ON tw.task_id = t.id
                                LEFT OUTER JOIN business_requirement b
                                    ON b.id = p.business_requirement_id
                                -- Link with the BR resource
                                INNER JOIN business_requirement_resource r
                                    ON r.business_requirement_id = b.id
                                    -- AND r.id = t.br_resource_id
                            WHERE
                                t.name = r.name
                            GROUP BY
                                t.id, p.id, a.id, b.id, r.id
                        )
                        UNION
                        (
                            SELECT
                                a.partner_id,
                                b.project_id AS master_project_id,
                                b.id AS br_id,
                                b.state AS br_status,
                                null as task_category_id,
                                CASE WHEN p.active = True THEN 'Active'
                                WHEN p.active=False THEN 'Archived'
                                END AS project_state,
                                p.id AS project_id,
                                a.id AS account_id,
                                'issue' AS activity_type,
                                i.id AS activity_id,
                                i.name AS activity_name,
                                i.user_id,
                                i.stage_id AS activity_stage_id,
                                0 AS estimated_hours,
                                0 AS planned_hours,
                                SUM(al.unit_amount) AS total_tms,
                                0 AS remaining_hours,
                                b.kanban_state as br_kanban_state,
                                null as task_kanban_state,
                                i.priority as priority,
                                null as date_deadline,
                                SUM(al.unit_amount) AS total_hours,
                                SUM(al.unit_amount) AS variance
                            FROM
                                project_project p
                                -- Link with the analytic account
                                INNER JOIN account_analytic_account a
                                    ON a.id = p.analytic_account_id
                                -- Link with the issue
                                INNER JOIN project_issue i
                                ON i.project_id = p.id
                                -- Link with the timesheet
                                LEFT OUTER JOIN account_analytic_line ts
                                    ON ts.issue_id = i.id
                                LEFT OUTER JOIN account_analytic_line al
                                    ON al.id = ts.sheet_id
                                -- Link with the BR
                                LEFT OUTER JOIN business_requirement b
                                    ON b.id = p.business_requirement_id
                            GROUP BY
                                i.id, p.id, a.id, b.id
                        )
                    ) AS q)""")
