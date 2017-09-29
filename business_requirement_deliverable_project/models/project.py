# -*- coding: utf-8 -*-
# © 2016-2017 Elico Corp (https://www.elico-corp.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class Project(models.Model):
    _inherit = "project.project"

    origin = fields.Char('Source Document')

    business_requirement_id = fields.Many2one(
        'business.requirement',
        string='Business Requirement',
        help='Link the Project and the business requirement',
    )

    business_requirement_deliverable_id = fields.Many2one(
        comodel_name='business.requirement.deliverable',
        string='Business Requirement Deliverable',
        help='Link the Project and the business requirement deliverable',
    )

    @api.multi
    def generate_project_wizard(self):
        br_ids = self.env.context.get('br_ids', False)
        from_project = False
        if not br_ids:
            br_ids = self.br_ids
            from_project = True
        default_uom = self.env.user and self.env.user.company_id \
            and self.env.user.company_id.project_time_mode_id.id
        if not default_uom:
            raise ValidationError(
                _("""Please set working time default unit in project
                    config settings"""))
        lines = self.env['business.requirement.resource']
        for br in br_ids:
            if br.state not in ['stakeholder_approval', 'cancel', 'done']:
                raise ValidationError(
                    _("All business requirements of the project should "
                      "be stakeholder_approval/canceled/done"))
            for deliverables in br.deliverable_lines:
                for line in deliverables.resource_ids:
                    if line.resource_type != 'task':
                        continue
                    generated = self.env['project.task'].search(
                        [('br_resource_id', '=', line.id)],
                        limit=1)

                    if generated:
                        continue
                    lines |= line
            for resource_line in br.resource_lines.filtered(
                    lambda resource: resource.resource_type == 'task'):
                generated = self.env['project.task'].search(
                    [('br_resource_id', '=', resource_line.id)],
                    limit=1)
                if generated:
                    continue
                lines |= resource_line
            for subbr in br.business_requirement_ids:
                for dl in subbr.deliverable_lines:
                    for line in dl.resource_ids:
                        if line.resource_type != 'task':
                            continue
                        generated = self.env['project.task'].search(
                            [('br_resource_id', '=', line.id)],
                            limit=1)
                        if generated:
                            continue
                        lines |= line
        if not lines and not br.project_ids:
            raise ValidationError(
                _("""There is no available business requirement resource line
                    to generate task"""))
        if from_project:
            br_ids.filtered(lambda br_id: not br_id.parent_id)
        vals = {
            'partner_id': self.partner_id.id,
            'project_id': self.id,
            'br_ids': [(6, 0, br_ids.ids)]
        }
        wizard_obj = self.env['br.generate.projects']
        wizard = wizard_obj.with_context(
            default_uom=default_uom, br_ids=False).create(vals)
        action = wizard.wizard_view()
        return action


class ProjectTask(models.Model):
    _inherit = "project.task"

    business_requirement_id = fields.Many2one(
        'business.requirement',
        string='Business Requirement',
        help='Link the task and the business requirement',
    )

    br_resource_id = fields.Many2one(
        comodel_name='business.requirement.resource',
        string='Business Requirement Resource',
        ondelete='set null'
    )
