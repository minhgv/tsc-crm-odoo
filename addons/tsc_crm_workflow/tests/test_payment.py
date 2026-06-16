from odoo.tests.common import TransactionCase


class TestTscPayment(TransactionCase):

    def setUp(self):
        super().setUp()
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
            'tsc_order_id': 'ORD-PAY-001',
        })
        self.invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 500000.0,
        })

    def test_payment_creation(self):
        payment = self.env['tsc.payment'].create({
            'invoice_id': self.invoice.id,
            'amount': 500000.0,
            'payment_method': 'unipay_wallet',
        })
        self.assertEqual(payment.state, 'pending')
        self.assertTrue(payment.name.startswith('PAY'))

    def test_payment_confirm(self):
        payment = self.env['tsc.payment'].create({
            'invoice_id': self.invoice.id,
            'amount': 500000.0,
            'payment_method': 'unipay_bank',
        })
        payment.action_confirm()
        self.assertEqual(payment.state, 'confirmed')
        self.assertEqual(self.invoice.state, 'paid')

    def test_payment_fail(self):
        payment = self.env['tsc.payment'].create({
            'invoice_id': self.invoice.id,
            'amount': 500000.0,
            'payment_method': 'qr',
        })
        payment.action_fail()
        self.assertEqual(payment.state, 'failed')
        self.assertEqual(self.invoice.state, 'draft')

    def test_payment_methods(self):
        methods = ['unipay_wallet', 'unipay_bank', 'qr', 'mobile', 'umoney', 'cash']
        for method in methods:
            payment = self.env['tsc.payment'].create({
                'invoice_id': self.invoice.id,
                'amount': 100000.0,
                'payment_method': method,
            })
            self.assertEqual(payment.payment_method, method)

    def test_payment_partial(self):
        payment1 = self.env['tsc.payment'].create({
            'invoice_id': self.invoice.id,
            'amount': 300000.0,
            'payment_method': 'cash',
        })
        payment1.action_confirm()
        self.assertEqual(self.invoice.state, 'paid')
        self.assertEqual(len(self.invoice.payment_ids), 1)
