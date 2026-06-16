from odoo.tests.common import TransactionCase


class TestTscVoffice(TransactionCase):

    def test_voffice_config_creation(self):
        config = self.env['tsc.voffice.config'].create({
            'name': 'Default',
            'api_url': 'https://crm.laoid.net/apis',
            'api_user': 'test_user',
            'api_password': 'test_pass',
        })
        self.assertEqual(config.api_url, 'https://crm.laoid.net/apis')
        self.assertTrue(config.active)

    def test_voffice_config_default_values(self):
        config = self.env['tsc.voffice.config'].create({
            'name': 'Test Config',
            'api_user': 'user',
            'api_password': 'pass',
        })
        self.assertEqual(config.api_url, 'https://crm.laoid.net/apis')
        self.assertEqual(config.default_type_id, 0)
        self.assertEqual(config.default_area_id, 0)
        self.assertEqual(config.default_place, 'Vientiane')

    def test_voffice_config_custom_defaults(self):
        config = self.env['tsc.voffice.config'].create({
            'name': 'Custom Config',
            'api_user': 'user',
            'api_password': 'pass',
            'default_type_id': 2,
            'default_area_id': 1,
            'default_place': 'Luang Prabang',
        })
        self.assertEqual(config.default_type_id, 2)
        self.assertEqual(config.default_area_id, 1)
        self.assertEqual(config.default_place, 'Luang Prabang')

    def test_voffice_sign_record(self):
        config = self.env['tsc.voffice.config'].create({
            'name': 'Test',
            'api_user': 'user',
            'api_password': 'pass',
        })
        lead = self.env['crm.lead'].create({
            'name': 'Test Lead',
            'tsc_order_id': 'ORD-VOF-001',
        })
        contract = self.env['tsc.contract'].create({
            'lead_id': lead.id,
        })
        sign = self.env['tsc.voffice.sign'].create({
            'contract_id': contract.id,
            'voffice_config_id': config.id,
        })
        self.assertEqual(sign.status, 'draft')
        self.assertEqual(sign.contract_id, contract)

    def test_voffice_contract_link(self):
        config = self.env['tsc.voffice.config'].create({
            'name': 'Test',
            'api_user': 'user',
            'api_password': 'pass',
        })
        lead = self.env['crm.lead'].create({
            'name': 'Test Lead',
            'tsc_order_id': 'ORD-VOF-002',
        })
        contract = self.env['tsc.contract'].create({
            'lead_id': lead.id,
            'voffice_config_id': config.id,
        })
        self.assertEqual(contract.voffice_config_id, config)
        self.assertEqual(contract.voffice_status, 'none')
