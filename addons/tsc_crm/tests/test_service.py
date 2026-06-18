from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestTscService(TransactionCase):

    def setUp(self):
        super().setUp()
        self.service = self.env['tsc.service'].create({
            'name': 'Cloud Server',
            'code': 'CS',
            'service_type': 'direct',
            'description': 'Public cloud server service',
        })

    def test_service_creation(self):
        self.assertEqual(self.service.name, 'Cloud Server')
        self.assertEqual(self.service.code, 'CS')
        self.assertEqual(self.service.service_type, 'direct')
        self.assertTrue(self.service.active)

    def test_service_sequence_default(self):
        self.assertEqual(self.service.sequence, 10)

    def test_service_unique_code(self):
        with self.assertRaises(Exception):
            self.env['tsc.service'].create({
                'name': 'Duplicate Service',
                'code': 'CS',
            })

    def test_service_code_too_short(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.service'].create({
                'name': 'Bad Service',
                'code': 'X',
            })

    def test_service_packages_relation(self):
        package = self.env['tsc.package'].create({
            'name': 'CS1 HDD',
            'code': 'CS1-HDD',
            'service_id': self.service.id,
            'package_type': 'cycle',
        })
        self.assertEqual(len(self.service.package_ids), 1)
        self.assertEqual(self.service.package_ids[0].name, 'CS1 HDD')

    def test_service_total_packages_compute(self):
        self.assertEqual(self.service.total_packages, 0)
        self.env['tsc.package'].create({
            'name': 'Package 1',
            'code': 'P1',
            'service_id': self.service.id,
            'package_type': 'cycle',
        })
        self.env['tsc.package'].create({
            'name': 'Package 2',
            'code': 'P2',
            'service_id': self.service.id,
            'package_type': 'one_time',
        })
        self.service.invalidate_recordset(['total_packages'])
        self.assertEqual(self.service.total_packages, 2)

    def test_service_archive(self):
        self.service.active = False
        self.assertFalse(self.service.active)
