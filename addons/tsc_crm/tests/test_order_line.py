from odoo.tests.common import TransactionCase


class TestTscOrderLine(TransactionCase):

    def setUp(self):
        super().setUp()
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
            'tsc_order_id': 'ORD-TEST-001',
        })
        self.service = self.env['tsc.service'].create({
            'name': 'Test Service',
            'code': 'TS',
            'service_type': 'direct',
        })
        self.package = self.env['tsc.package'].create({
            'name': 'Test Package',
            'code': 'TP',
            'service_id': self.service.id,
            'package_type': 'cycle',
        })

    def test_order_line_total_computation(self):
        line = self.env['tsc.order.line'].create({
            'lead_id': self.lead.id,
            'service_id': self.service.id,
            'package_id': self.package.id,
            'quantity': 2,
            'unit_price': 1000.0,
            'discount_amount': 100.0,
        })
        self.assertEqual(line.total_price, 1900.0)

    def test_order_line_zero_quantity(self):
        line = self.env['tsc.order.line'].create({
            'lead_id': self.lead.id,
            'service_id': self.service.id,
            'package_id': self.package.id,
            'quantity': 0,
            'unit_price': 1000.0,
            'discount_amount': 0,
        })
        self.assertEqual(line.total_price, 0.0)
