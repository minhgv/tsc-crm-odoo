from odoo.tests.common import TransactionCase


class TestTscOrderLine(TransactionCase):

    def setUp(self):
        super().setUp()
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
            'tsc_order_id': 'ORD-TEST-001',
        })

    def test_order_line_total_computation(self):
        line = self.env['tsc.order.line'].create({
            'lead_id': self.lead.id,
            'service_id': self.env.ref('base.module_sale').id,  # placeholder
            'package_id': self.env.ref('base.module_sale').id,  # placeholder
            'quantity': 2,
            'unit_price': 1000.0,
            'discount_amount': 100.0,
        })
        self.assertEqual(line.total_price, 1900.0)

    def test_order_line_zero_quantity(self):
        line = self.env['tsc.order.line'].create({
            'lead_id': self.lead.id,
            'service_id': self.env.ref('base.module_sale').id,
            'package_id': self.env.ref('base.module_sale').id,
            'quantity': 0,
            'unit_price': 1000.0,
            'discount_amount': 0,
        })
        self.assertEqual(line.total_price, 0.0)
