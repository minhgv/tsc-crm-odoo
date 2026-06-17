from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTechnicalTask(TransactionCase):

    def setUp(self):
        super().setUp()
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
        })
        self.employee = self.env['hr.employee'].create({
            'name': 'Tech Employee',
            'tsc_role': 'staff',
            'tsc_group_type': 'technical',
        })

    def test_task_creation(self):
        task = self.env['tsc.technical.task'].create({
            'name': 'Survey Task',
            'lead_id': self.lead.id,
            'task_type': 'survey',
            'assigned_to': self.employee.id,
        })
        self.assertEqual(task.state, 'draft')
        self.assertEqual(task.task_type, 'survey')

    def test_task_workflow(self):
        task = self.env['tsc.technical.task'].create({
            'name': 'Survey Task',
            'lead_id': self.lead.id,
            'task_type': 'survey',
            'assigned_to': self.employee.id,
        })
        task.action_assign()
        self.assertEqual(task.state, 'assigned')
        task.action_accept()
        self.assertEqual(task.state, 'accepted')
        task.action_start()
        self.assertEqual(task.state, 'in_progress')
        task.action_done()
        self.assertEqual(task.state, 'done')

    def test_task_cancel_and_reset(self):
        task = self.env['tsc.technical.task'].create({
            'name': 'Cancel Task',
            'lead_id': self.lead.id,
            'task_type': 'maintenance',
        })
        task.action_cancel()
        self.assertEqual(task.state, 'cancelled')
        task.action_reset()
        self.assertEqual(task.state, 'draft')

    def test_task_overdue(self):
        task = self.env['tsc.technical.task'].create({
            'name': 'Overdue Task',
            'lead_id': self.lead.id,
            'task_type': 'survey',
            'deadline': '2020-01-01 00:00:00',
        })
        self.assertTrue(task.is_overdue)

    def test_task_assign_requires_employee(self):
        task = self.env['tsc.technical.task'].create({
            'name': 'No Assignee Task',
            'lead_id': self.lead.id,
            'task_type': 'survey',
        })
        with self.assertRaises(ValidationError):
            task.action_assign()
