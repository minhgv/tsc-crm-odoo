from odoo.tests.common import TransactionCase


class TestTscSlaViolation(TransactionCase):

    def setUp(self):
        super().setUp()
        try:
            self.sla_config = self.env['tsc.sla.config'].search([], limit=1)
            if not self.sla_config:
                self.skipTest('No tsc.sla.config records available')
        except KeyError:
            self.skipTest('tsc.sla.config model not available')
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
            'tsc_order_id': 'ORD-TEST-001',
        })
        self.violation = self.env['tsc.sla.violation'].create({
            'lead_id': self.lead.id,
            'sla_config_id': self.sla_config.id,
            'stage_key': 'created',
        })

    def test_violation_creation(self):
        self.assertEqual(self.violation.lead_id, self.lead)
        self.assertEqual(self.violation.sla_config_id, self.sla_config)
        self.assertFalse(self.violation.resolved)

    def test_violation_name_computation(self):
        self.assertIn(self.lead.name, self.violation.name)

    def test_violation_resolve(self):
        self.violation.action_resolve()
        self.assertTrue(self.violation.resolved)
        self.assertTrue(self.violation.resolved_date)

    def test_violation_reopen(self):
        self.violation.action_resolve()
        self.violation.action_reopen()
        self.assertFalse(self.violation.resolved)
        self.assertFalse(self.violation.resolved_date)
