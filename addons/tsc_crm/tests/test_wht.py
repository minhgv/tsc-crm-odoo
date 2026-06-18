from datetime import date

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestTscWht(TransactionCase):

    def setUp(self):
        super().setUp()
        self.wht = self.env['tsc.wht'].create({
            'name': 'Standard WHT 1%',
            'rate': 1.0,
            'date_from': date(2024, 1, 1),
            'date_to': date(2024, 12, 31),
        })

    def test_wht_creation(self):
        self.assertEqual(self.wht.name, 'Standard WHT 1%')
        self.assertEqual(self.wht.rate, 1.0)
        self.assertTrue(self.wht.active)

    def test_wht_rate_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.wht'].create({
                'name': 'Invalid WHT',
                'rate': -1.0,
                'date_from': date(2024, 1, 1),
            })

    def test_wht_date_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.wht'].create({
                'name': 'Invalid Dates',
                'rate': 1.0,
                'date_from': date(2024, 12, 31),
                'date_to': date(2024, 1, 1),
            })

    def test_get_current_rate(self):
        rate = self.env['tsc.wht']._get_current_rate(date(2024, 6, 15))
        self.assertEqual(rate, 1.0)

    def test_get_current_rate_no_active(self):
        self.wht.active = False
        rate = self.env['tsc.wht']._get_current_rate(date(2024, 6, 15))
        self.assertEqual(rate, 0.0)
