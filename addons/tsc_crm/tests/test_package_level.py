from odoo.tests.common import TransactionCase


class TestTscPackageLevel(TransactionCase):

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
        })
        self.level = self.env['tsc.package.level'].create({
            'name': 'HDD',
            'package_id': self.package.id,
            'price': 160000.0,
        })

    def test_level_creation(self):
        self.assertEqual(self.level.name, 'HDD')
        self.assertEqual(self.level.package_id, self.package)
        self.assertEqual(self.level.price, 160000.0)
        self.assertTrue(self.level.active)

    def test_level_sequence_default(self):
        self.assertEqual(self.level.sequence, 10)

    def test_multiple_levels(self):
        self.env['tsc.package.level'].create({
            'name': 'SSD',
            'package_id': self.package.id,
            'price': 190000.0,
        })
        self.assertEqual(len(self.package.level_ids), 2)
