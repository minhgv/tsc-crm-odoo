from odoo.tests.common import TransactionCase


class TestTscPackage(TransactionCase):

    def setUp(self):
        super().setUp()
        self.service = self.env['tsc.service'].create({
            'name': 'Cloud Server',
            'code': 'CS',
            'service_type': 'direct',
        })

    def test_package_creation(self):
        pkg = self.env['tsc.package'].create({
            'name': 'CS1',
            'service_id': self.service.id,
            'package_type': 'cycle',
            'validity_days': 30,
            'deployment_fee': 100000.0,
        })
        self.assertEqual(pkg.name, 'CS1')
        self.assertEqual(pkg.package_type, 'cycle')
        self.assertEqual(pkg.validity_days, 30)

    def test_package_per_use_type(self):
        pkg = self.env['tsc.package'].create({
            'name': 'SMS Package',
            'service_id': self.service.id,
            'package_type': 'per_use',
        })
        self.assertEqual(pkg.package_type, 'per_use')

    def test_package_levels(self):
        pkg = self.env['tsc.package'].create({
            'name': 'CS2',
            'service_id': self.service.id,
            'package_type': 'cycle',
        })
        level1 = self.env['tsc.package.level'].create({
            'name': 'HDD',
            'package_id': pkg.id,
            'price': 160000.0,
        })
        level2 = self.env['tsc.package.level'].create({
            'name': 'SSD',
            'package_id': pkg.id,
            'price': 190000.0,
        })
        self.assertEqual(len(pkg.level_ids), 2)
        self.assertIn(level1, pkg.level_ids)
        self.assertIn(level2, pkg.level_ids)

    def test_package_trial_days(self):
        pkg = self.env['tsc.package'].create({
            'name': 'Trial Package',
            'service_id': self.service.id,
            'package_type': 'cycle',
            'trial_days': 7,
            'validity_days': 30,
        })
        self.assertEqual(pkg.trial_days, 7)
