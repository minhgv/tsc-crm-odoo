from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestTscVat(TransactionCase):

    def setUp(self):
        super().setUp()
        self.vat = self.env['tsc.vat'].create({
            'name': 'Standard VAT 7%',
            'rate': 7.0,
            'date_from': date(2024, 1, 1),
            'date_to': date(2024, 4, 30),
        })

    def test_vat_creation(self):
        self.assertEqual(self.vat.name, 'Standard VAT 7%')
        self.assertEqual(self.vat.rate, 7.0)
        self.assertTrue(self.vat.active)

    def test_vat_rate_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.vat'].create({
                'name': 'Invalid VAT',
                'rate': -5.0,
                'date_from': date(2024, 1, 1),
            })

    def test_vat_date_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.vat'].create({
                'name': 'Invalid Dates',
                'rate': 7.0,
                'date_from': date(2024, 5, 1),
                'date_to': date(2024, 1, 1),
            })

    def test_get_current_rate(self):
        # Create another VAT for later period
        self.env['tsc.vat'].create({
            'name': 'VAT 10%',
            'rate': 10.0,
            'date_from': date(2024, 5, 1),
        })
        # Test getting rate for different dates
        rate_jan = self.env['tsc.vat']._get_current_rate(date(2024, 1, 15))
        rate_may = self.env['tsc.vat']._get_current_rate(date(2024, 5, 15))
        self.assertEqual(rate_jan, 7.0)
        self.assertEqual(rate_may, 10.0)

    def test_get_current_rate_fallback(self):
        # Create a VAT without end date (open-ended)
        self.env['tsc.vat'].create({
            'name': 'VAT 7% Open',
            'rate': 7.0,
            'date_from': date(2024, 1, 1),
        })
        # Test fallback to nearest previous rate
        rate = self.env['tsc.vat']._get_current_rate(date(2024, 6, 1))
        self.assertEqual(rate, 7.0)
