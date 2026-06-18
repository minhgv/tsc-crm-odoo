from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestTscContract(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
        })
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
            'tsc_order_id': 'ORD-TEST-001',
            'partner_id': self.partner.id,
        })
        self.contract = self.env['tsc.contract'].create({
            'lead_id': self.lead.id,
            'partner_id': self.partner.id,
        })

    def test_contract_creation(self):
        self.assertEqual(self.contract.state, 'draft')
        self.assertEqual(self.contract.partner_id, self.partner)
        self.assertEqual(self.contract.lead_id, self.lead)
        self.assertTrue(self.contract.name)
        self.assertNotEqual(self.contract.name, 'New')

    def test_contract_workflow(self):
        self.assertEqual(self.contract.state, 'draft')
        self.contract.action_submit()
        self.assertEqual(self.contract.state, 'pending_sign')
        self.contract.action_sign()
        self.assertEqual(self.contract.state, 'signed')
        self.contract.action_activate()
        self.assertEqual(self.contract.state, 'active')
        self.assertTrue(self.contract.start_date)

    def test_contract_cancel_from_draft(self):
        self.contract.action_cancel()
        self.assertEqual(self.contract.state, 'cancelled')

    def test_contract_cancel_from_expired(self):
        self.contract.write({'state': 'expired'})
        with self.assertRaises(ValidationError):
            self.contract.action_cancel()

    def test_contract_reset_to_draft(self):
        self.contract.action_submit()
        self.assertEqual(self.contract.state, 'pending_sign')
        self.contract.action_reset_to_draft()
        self.assertEqual(self.contract.state, 'draft')

    def test_contract_amount_computation(self):
        service = self.env['tsc.service'].create({
            'name': 'Test Service',
            'code': 'TS',
            'service_type': 'direct',
        })
        package = self.env['tsc.package'].create({
            'name': 'Test Package',
            'code': 'TP',
            'service_id': service.id,
            'package_type': 'cycle',
        })
        self.env['tsc.order.line'].create({
            'lead_id': self.lead.id,
            'service_id': service.id,
            'package_id': package.id,
            'quantity': 2,
            'unit_price': 100000.0,
            'discount_amount': 10000.0,
        })
        self.contract.invalidate_recordset(['amount_total'])
        self.assertEqual(self.contract.amount_total, 190000.0)
