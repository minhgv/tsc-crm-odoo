from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestTscPayment(TransactionCase):

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
        self.invoice = self.env['tsc.invoice'].create({
            'contract_id': self.contract.id,
        })
        self.env['tsc.invoice.line'].create({
            'invoice_id': self.invoice.id,
            'description': 'Test Item',
            'quantity': 1,
            'unit_price': 100000.0,
        })
        self.invoice.action_post()
        self.payment = self.env['tsc.payment'].create({
            'invoice_id': self.invoice.id,
            'amount': 100000.0,
            'payment_method': 'cash',
        })

    def test_payment_creation(self):
        self.assertEqual(self.payment.state, 'draft')
        self.assertEqual(self.payment.invoice_id, self.invoice)
        self.assertTrue(self.payment.name)
        self.assertNotEqual(self.payment.name, 'New')

    def test_payment_workflow(self):
        self.assertEqual(self.payment.state, 'draft')
        self.payment.action_submit()
        self.assertEqual(self.payment.state, 'pending')
        self.payment.action_confirm()
        self.assertEqual(self.payment.state, 'confirmed')

    def test_payment_fail(self):
        self.payment.action_submit()
        self.payment.action_fail()
        self.assertEqual(self.payment.state, 'failed')

    def test_payment_refund(self):
        self.payment.action_submit()
        self.payment.action_confirm()
        self.payment.action_refund()
        self.assertEqual(self.payment.state, 'refunded')

    def test_payment_refund_not_confirmed(self):
        self.payment.action_submit()
        with self.assertRaises(ValidationError):
            self.payment.action_refund()

    def test_invoice_paid_status(self):
        self.payment.action_submit()
        self.payment.action_confirm()
        self.assertEqual(self.payment.state, 'confirmed')
        # Verify invoice amount_paid is computed
        self.invoice.invalidate_recordset(['amount_paid'])
        self.assertAlmostEqual(self.invoice.amount_paid, 100000.0, places=2)
