from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestTscInvoice(TransactionCase):

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

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.state, 'draft')
        self.assertEqual(self.invoice.partner_id, self.partner)
        self.assertTrue(self.invoice.name)
        self.assertNotEqual(self.invoice.name, 'New')

    def test_invoice_post(self):
        self.env['tsc.invoice.line'].create({
            'invoice_id': self.invoice.id,
            'description': 'Test Item',
            'quantity': 1,
            'unit_price': 100000.0,
        })
        self.invoice.action_post()
        self.assertEqual(self.invoice.state, 'posted')

    def test_invoice_post_without_lines(self):
        with self.assertRaises(ValidationError):
            self.invoice.action_post()

    def test_invoice_cancel(self):
        self.invoice.action_cancel()
        self.assertEqual(self.invoice.state, 'cancelled')

    def test_invoice_cancel_paid(self):
        self.invoice.write({'state': 'paid'})
        with self.assertRaises(ValidationError):
            self.invoice.action_cancel()

    def test_invoice_refund(self):
        self.invoice.write({'state': 'posted'})
        self.invoice.action_refund()
        self.assertEqual(self.invoice.state, 'refund')

    def test_invoice_amount_computation(self):
        self.env['tsc.invoice.line'].create({
            'invoice_id': self.invoice.id,
            'description': 'Item 1',
            'quantity': 2,
            'unit_price': 100000.0,
            'discount': 10.0,
        })
        self.env['tsc.invoice.line'].create({
            'invoice_id': self.invoice.id,
            'description': 'Item 2',
            'quantity': 1,
            'unit_price': 50000.0,
        })
        self.invoice.invalidate_recordset(['amount_untaxed', 'vat_amount', 'amount_total'])
        # Item 1: 2 * 100000 * 0.9 = 180000
        # Item 2: 1 * 50000 = 50000
        # Untaxed: 230000
        # VAT 7%: 16100
        # Total: 246100
        self.assertAlmostEqual(self.invoice.amount_untaxed, 230000.0, places=2)
        self.assertAlmostEqual(self.invoice.vat_amount, 16100.0, places=2)
        self.assertAlmostEqual(self.invoice.amount_total, 246100.0, places=2)
