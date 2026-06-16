from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTscService(TransactionCase):

    def test_service_creation(self):
        service = self.env['tsc.service'].create({
            'name': 'Cloud Server',
            'code': 'CS',
            'service_type': 'direct',
            'target_customer': 'business',
            'distribution_channel': 'online',
        })
        self.assertEqual(service.name, 'Cloud Server')
        self.assertEqual(service.code, 'CS')
        self.assertTrue(service.active)

    def test_service_unique_code(self):
        s1 = self.env['tsc.service'].create({
            'name': 'Service 1',
            'code': 'UNIQUE',
            'service_type': 'direct',
        })
        self.assertTrue(s1)
        s2 = self.env['tsc.service'].search([('code', '=', 'UNIQUE')])
        self.assertEqual(len(s2), 1)

    def test_service_project_type(self):
        service = self.env['tsc.service'].create({
            'name': 'NamPaPar',
            'code': 'NPP',
            'service_type': 'project',
            'target_customer': 'government',
        })
        self.assertEqual(service.service_type, 'project')

    def test_service_with_packages(self):
        service = self.env['tsc.service'].create({
            'name': 'Cloud Camera',
            'code': 'CC',
            'service_type': 'direct',
        })
        pkg = self.env['tsc.package'].create({
            'name': 'CC1',
            'service_id': service.id,
            'package_type': 'cycle',
            'validity_days': 30,
        })
        self.assertIn(pkg, service.package_ids)
