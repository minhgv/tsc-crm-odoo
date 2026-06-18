from odoo.tests.common import TransactionCase


class TestTscPackage(TransactionCase):

    def setUp(self):
        super().setUp()
        self.service = self.env['tsc.service'].create({
            'name': 'Cloud Server',
            'code': 'CS',
            'service_type': 'direct',
        })
        self.package = self.env['tsc.package'].create({
            'name': 'CS1 HDD',
            'code': 'CS1-HDD',
            'service_id': self.service.id,
            'package_type': 'cycle',
            'validity_days': 30,
            'setup_fee': 50000.0,
        })

    def test_package_creation(self):
        self.assertEqual(self.package.name, 'CS1 HDD')
        self.assertEqual(self.package.code, 'CS1-HDD')
        self.assertEqual(self.package.service_id, self.service)
        self.assertEqual(self.package.package_type, 'cycle')
        self.assertTrue(self.package.active)

    def test_package_unique_code(self):
        with self.assertRaises(Exception):
            self.env['tsc.package'].create({
                'name': 'Duplicate Package',
                'code': 'CS1-HDD',
                'service_id': self.service.id,
                'package_type': 'cycle',
            })

    def test_package_levels_relation(self):
        level = self.env['tsc.package.level'].create({
            'name': 'HDD',
            'package_id': self.package.id,
            'price': 160000.0,
        })
        self.assertEqual(len(self.package.level_ids), 1)
        self.assertEqual(self.package.level_ids[0].price, 160000.0)

    def test_package_combo_services(self):
        service2 = self.env['tsc.service'].create({
            'name': 'Cloud Camera',
            'code': 'CC',
            'service_type': 'direct',
        })
        self.package.is_combo = True
        self.package.combo_service_ids = [(6, 0, [self.service.id, service2.id])]
        self.assertEqual(len(self.package.combo_service_ids), 2)

    def test_package_archive(self):
        self.package.active = False
        self.assertFalse(self.package.active)
