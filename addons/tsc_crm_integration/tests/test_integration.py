from odoo.tests.common import TransactionCase


class TestTscIntegrationConfig(TransactionCase):

    def test_config_creation(self):
        config = self.env['tsc.integration.config'].create({
            'name': 'BCCS3 Production',
            'system': 'bccs3',
            'api_url': 'https://api.bccs3.la',
            'api_key': 'test_key',
        })
        self.assertEqual(config.system, 'bccs3')
        self.assertTrue(config.active)

    def test_config_all_systems(self):
        for system in ['unipay', 'bccs3', 'datalake', 'voffice', 'sms']:
            config = self.env['tsc.integration.config'].create({
                'name': f'{system.upper()} Config',
                'system': system,
                'api_url': f'https://api.{system}.la',
            })
            self.assertEqual(config.system, system)


class TestTscIntegrationLog(TransactionCase):

    def setUp(self):
        super().setUp()
        self.config = self.env['tsc.integration.config'].create({
            'name': 'Test Config',
            'system': 'bccs3',
            'api_url': 'https://api.test.la',
        })

    def test_log_creation(self):
        log = self.env['tsc.integration.log'].create({
            'config_id': self.config.id,
            'direction': 'outbound',
            'request_data': '{"action": "push_invoice"}',
            'response_data': '{"status": "ok"}',
            'state': 'success',
        })
        self.assertEqual(log.state, 'success')
        self.assertEqual(log.direction, 'outbound')

    def test_log_failed(self):
        log = self.env['tsc.integration.log'].create({
            'config_id': self.config.id,
            'direction': 'inbound',
            'state': 'failed',
            'error_message': 'Connection timeout',
        })
        self.assertEqual(log.state, 'failed')
        self.assertEqual(log.error_message, 'Connection timeout')
