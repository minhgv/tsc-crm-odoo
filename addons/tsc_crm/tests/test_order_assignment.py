from odoo.tests.common import TransactionCase


class TestOrderAssignment(TransactionCase):

    def setUp(self):
        super().setUp()
        self.region = self.env['tsc.region'].create({
            'name': 'Vientiane',
            'code': 'VT',
        })
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
        })
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'tsc_role': 'staff',
            'tsc_group_type': 'business',
        })

    def test_assignment_creation(self):
        assignment = self.env['tsc.order.assignment'].create({
            'lead_id': self.lead.id,
            'assigned_to': self.employee.id,
            'reason': 'auto',
        })
        self.assertEqual(assignment.lead_id, self.lead)
        self.assertEqual(assignment.assigned_to, self.employee)
        self.assertEqual(assignment.reason, 'auto')

    def test_assignment_with_notes(self):
        assignment = self.env['tsc.order.assignment'].create({
            'lead_id': self.lead.id,
            'assigned_to': self.employee.id,
            'reason': 'manual',
            'notes': 'Assigned by admin',
        })
        self.assertEqual(assignment.notes, 'Assigned by admin')

    def test_assignment_lead_relation(self):
        self.env['tsc.order.assignment'].create({
            'lead_id': self.lead.id,
            'assigned_to': self.employee.id,
            'reason': 'auto',
        })
        self.assertEqual(len(self.lead.tsc_assignment_ids), 1)
