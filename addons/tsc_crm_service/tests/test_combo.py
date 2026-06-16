from odoo.tests.common import TransactionCase


class TestTscCombo(TransactionCase):

    def setUp(self):
        super().setUp()
        self.service1 = self.env['tsc.service'].create({
            'name': 'Cloud Server',
            'code': 'CS',
            'service_type': 'direct',
        })
        self.service2 = self.env['tsc.service'].create({
            'name': 'Cloud Camera',
            'code': 'CC',
            'service_type': 'direct',
        })
        self.pkg1 = self.env['tsc.package'].create({
            'name': 'CS1',
            'service_id': self.service1.id,
            'package_type': 'cycle',
        })
        self.pkg2 = self.env['tsc.package'].create({
            'name': 'CC1',
            'service_id': self.service2.id,
            'package_type': 'cycle',
        })

    def test_combo_creation(self):
        combo = self.env['tsc.combo'].create({
            'name': 'Cloud Bundle',
            'line_ids': [
                (0, 0, {
                    'service_id': self.service1.id,
                    'package_id': self.pkg1.id,
                    'quantity': 1,
                    'price': 160000.0,
                }),
                (0, 0, {
                    'service_id': self.service2.id,
                    'package_id': self.pkg2.id,
                    'quantity': 1,
                    'price': 69000.0,
                }),
            ],
        })
        self.assertEqual(combo.name, 'Cloud Bundle')
        self.assertEqual(len(combo.line_ids), 2)

    def test_combo_total_price(self):
        combo = self.env['tsc.combo'].create({
            'name': 'Bundle Package',
            'line_ids': [
                (0, 0, {
                    'service_id': self.service1.id,
                    'package_id': self.pkg1.id,
                    'quantity': 1,
                    'price': 160000.0,
                }),
                (0, 0, {
                    'service_id': self.service2.id,
                    'package_id': self.pkg2.id,
                    'quantity': 1,
                    'price': 69000.0,
                }),
            ],
        })
        self.assertEqual(combo.total_price, 229000.0)

    def test_combo_empty_lines(self):
        combo = self.env['tsc.combo'].create({
            'name': 'Empty Combo',
        })
        self.assertEqual(combo.total_price, 0.0)
