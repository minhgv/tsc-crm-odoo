from odoo.tests.common import TransactionCase


class TestTscDiscount(TransactionCase):

    def setUp(self):
        super().setUp()
        self.service = self.env['tsc.service'].create({
            'name': 'Cloud Server',
            'code': 'CS',
            'service_type': 'direct',
        })

    def test_discount_line_type(self):
        discount = self.env['tsc.discount'].create({
            'name': 'Line Discount 10%',
            'discount_type': 'line_discount',
            'service_id': self.service.id,
            'percentage': 10.0,
        })
        self.assertEqual(discount.discount_type, 'line_discount')
        self.assertEqual(discount.percentage, 10.0)

    def test_discount_promotion_type(self):
        discount = self.env['tsc.discount'].create({
            'name': 'Promotion 50000 off',
            'discount_type': 'promotion',
            'service_id': self.service.id,
            'amount': 50000.0,
        })
        self.assertEqual(discount.discount_type, 'promotion')
        self.assertEqual(discount.amount, 50000.0)

    def test_discount_commission_type(self):
        discount = self.env['tsc.discount'].create({
            'name': 'Commission 5%',
            'discount_type': 'commission',
            'service_id': self.service.id,
            'percentage': 5.0,
        })
        self.assertEqual(discount.discount_type, 'commission')

    def test_discount_date_range(self):
        from datetime import date
        discount = self.env['tsc.discount'].create({
            'name': 'Seasonal Discount',
            'discount_type': 'promotion',
            'service_id': self.service.id,
            'percentage': 15.0,
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 12, 31),
        })
        self.assertEqual(discount.start_date, date(2024, 1, 1))
        self.assertEqual(discount.end_date, date(2024, 12, 31))
