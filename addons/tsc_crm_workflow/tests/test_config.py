from odoo.tests.common import TransactionCase


class TestTscConfig(TransactionCase):

    def test_vat_config(self):
        from datetime import date
        vat = self.env['tsc.vat.config'].create({
            'name': 'VAT 7%',
            'rate': 7.0,
            'date_from': date(2024, 1, 1),
            'date_to': date(2024, 4, 30),
        })
        self.assertEqual(vat.rate, 7.0)
        self.assertTrue(vat.active)

    def test_vat_config_10_percent(self):
        from datetime import date
        vat = self.env['tsc.vat.config'].create({
            'name': 'VAT 10%',
            'rate': 10.0,
            'date_from': date(2024, 5, 1),
            'date_to': date(2024, 11, 30),
        })
        self.assertEqual(vat.rate, 10.0)

    def test_wht_config(self):
        from datetime import date
        wht = self.env['tsc.wht.config'].create({
            'name': 'WHT 5%',
            'rate': 5.0,
            'date_from': date(2024, 1, 1),
            'date_to': date(2024, 12, 31),
        })
        self.assertEqual(wht.rate, 5.0)

    def test_exchange_rate(self):
        from datetime import date
        rate = self.env['tsc.exchange.rate'].create({
            'date': date(2024, 6, 15),
            'buy_rate': 24500.0,
            'sell_rate': 25000.0,
            'source': 'BCEL',
        })
        self.assertEqual(rate.buy_rate, 24500.0)
        self.assertEqual(rate.sell_rate, 25000.0)

    def test_sla_config(self):
        sla = self.env['tsc.sla.config'].create({
            'name': 'Order Acceptance',
            'stage': 'assignment',
            'unit': 'hours',
            'value': 24,
            'apply_type': '24h',
        })
        self.assertEqual(sla.stage, 'assignment')
        self.assertEqual(sla.value, 24)

    def test_sla_config_working_hours(self):
        sla = self.env['tsc.sla.config'].create({
            'name': 'Contract Signing',
            'stage': 'contract',
            'unit': 'days',
            'value': 3,
            'apply_type': 'working_hours',
            'working_hours_from': 8.0,
            'working_hours_to': 17.0,
        })
        self.assertEqual(sla.apply_type, 'working_hours')
        self.assertEqual(sla.working_hours_from, 8.0)
