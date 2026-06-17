from datetime import date
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTscPromotion(TransactionCase):

    def test_promotion_fixed(self):
        promo = self.env['tsc.promotion'].create({
            'name': '100K Off',
            'promo_type': 'fixed',
            'value': 100000,
            'scope': 'order_line',
            'date_from': date(2024, 1, 1),
            'date_to': date(2024, 12, 31),
        })
        self.assertEqual(promo.value, 100000)
        self.assertTrue(promo.active)

    def test_promotion_percentage(self):
        promo = self.env['tsc.promotion'].create({
            'name': '10% Off',
            'promo_type': 'percentage',
            'value': 10.0,
            'scope': 'package',
            'date_from': date(2024, 1, 1),
            'date_to': date(2024, 6, 30),
        })
        self.assertEqual(promo.promo_type, 'percentage')

    def test_promotion_date_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.promotion'].create({
                'name': 'Bad Dates',
                'promo_type': 'fixed',
                'value': 1000,
                'scope': 'service',
                'date_from': date(2024, 12, 31),
                'date_to': date(2024, 1, 1),
            })

    def test_promotion_percentage_over_100(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.promotion'].create({
                'name': 'Over 100%',
                'promo_type': 'percentage',
                'value': 150.0,
                'scope': 'order_line',
                'date_from': date(2024, 1, 1),
                'date_to': date(2024, 12, 31),
            })

    def test_promotion_negative_value(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.promotion'].create({
                'name': 'Negative',
                'promo_type': 'fixed',
                'value': -100,
                'scope': 'order_line',
                'date_from': date(2024, 1, 1),
                'date_to': date(2024, 12, 31),
            })
