from odoo.tests.common import TransactionCase


class TestTscInvoice(TransactionCase):

    def setUp(self):
        super().setUp()
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
            'tsc_order_id': 'ORD-INV-001',
        })

    def test_invoice_creation(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 1000000.0,
            'vat_rate': 7.0,
        })
        self.assertEqual(invoice.state, 'draft')
        self.assertTrue(invoice.name.startswith('INV'))

    def test_invoice_vat_calculation(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 1000000.0,
            'vat_rate': 7.0,
        })
        self.assertEqual(invoice.vat_amount, 70000.0)

    def test_invoice_wht_calculation(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 1000000.0,
            'wht_rate': 5.0,
        })
        self.assertEqual(invoice.wht_amount, 50000.0)

    def test_invoice_total_calculation(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 1000000.0,
            'vat_rate': 7.0,
            'wht_rate': 5.0,
        })
        # total = subtotal + vat - wht = 1000000 + 70000 - 50000 = 1020000
        self.assertEqual(invoice.total, 1020000.0)

    def test_invoice_post(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 500000.0,
        })
        invoice.action_post()
        self.assertEqual(invoice.state, 'posted')

    def test_invoice_pay(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 500000.0,
        })
        invoice.action_post()
        invoice.action_pay()
        self.assertEqual(invoice.state, 'paid')

    def test_invoice_cancel(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 500000.0,
        })
        invoice.action_cancel()
        self.assertEqual(invoice.state, 'cancelled')

    def test_invoice_refund(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 500000.0,
        })
        invoice.action_refund()
        self.assertEqual(invoice.state, 'refunded')

    def test_invoice_lines(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
        })
        line1 = self.env['tsc.invoice.line'].create({
            'invoice_id': invoice.id,
            'description': 'Cloud Server CS1',
            'quantity': 1,
            'unit_price': 160000.0,
        })
        line2 = self.env['tsc.invoice.line'].create({
            'invoice_id': invoice.id,
            'description': 'Cloud Camera CC1',
            'quantity': 2,
            'unit_price': 69000.0,
        })
        self.assertEqual(line1.amount, 160000.0)
        self.assertEqual(line2.amount, 138000.0)
        self.assertEqual(len(invoice.line_ids), 2)

    def test_invoice_vat_10_percent(self):
        invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 2000000.0,
            'vat_rate': 10.0,
        })
        self.assertEqual(invoice.vat_amount, 200000.0)
