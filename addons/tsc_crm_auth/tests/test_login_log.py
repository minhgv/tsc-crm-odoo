from odoo.tests.common import TransactionCase


class TestTscLoginLog(TransactionCase):

    def test_login_log_creation(self):
        user = self.env['res.users'].create({
            'login': 'log_test_user',
            'name': 'Log Test User',
        })
        log = self.env['tsc.login.log'].create({
            'user_id': user.id,
            'login_type': 'backend',
            'state': 'success',
            'ip_address': '192.168.1.1',
            'user_agent': 'Mozilla/5.0',
        })
        self.assertEqual(log.login_type, 'backend')
        self.assertEqual(log.state, 'success')
        self.assertEqual(log.ip_address, '192.168.1.1')

    def test_login_log_types(self):
        user = self.env['res.users'].create({
            'login': 'log_type_test',
            'name': 'Type Test',
        })
        for login_type in ['backend', 'otp', 'laoid']:
            log = self.env['tsc.login.log'].create({
                'user_id': user.id,
                'login_type': login_type,
                'state': 'success',
            })
            self.assertEqual(log.login_type, login_type)

    def test_login_log_failure(self):
        user = self.env['res.users'].create({
            'login': 'log_fail_test',
            'name': 'Fail Test',
        })
        log = self.env['tsc.login.log'].create({
            'user_id': user.id,
            'login_type': 'otp',
            'state': 'failed',
            'failure_reason': 'Invalid OTP',
        })
        self.assertEqual(log.state, 'failed')
        self.assertEqual(log.failure_reason, 'Invalid OTP')
