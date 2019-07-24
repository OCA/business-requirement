# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.business_requirement_sale.tests.\
    test_business_requirement_sale import TestBusinessRequirementSaleBase


class TestBusinessRequirementSaleTimesheet(TestBusinessRequirementSaleBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product1.write({
            'type': 'service',
            'service_tracking': 'task_new_project',
        })

    def test_button(self):
        self.wizard.deliverable_ids = self.deliverable1
        self.wizard.button_create()
        so = self.business_requirement.sale_order_ids
        so.action_confirm()
        action = so.tasks_ids.action_view_deliverable()
        action['res_id'] = self.deliverable1.id
