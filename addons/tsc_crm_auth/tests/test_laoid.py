from odoo.tests.common import TransactionCase


class TestTscLaoID(TransactionCase):

    def test_laoid_config_params_exist(self):
        ICP = self.env['ir.config_parameter'].sudo()
        params = [
            'tsc.laoid.environment',
            'tsc.laoid.base_url',
            'tsc.laoid.client_id',
            'tsc.laoid.client_secret',
            'tsc.laoid.callback_url',
        ]
        for param in params:
            value = ICP.get_param(param)
            self.assertIsNotNone(value, f"Missing config parameter: {param}")

    def test_laoid_find_or_create_new_user(self):
        laoid = self.env['tsc.laoid'].sudo()
        profile = {
            'id': '99999',
            'firstName': 'Test',
            'lastName': 'User',
            'phoneNumber': '2055999999',
            'email': [{'email': 'test@laoid.la', 'primary': True}],
        }
        user = laoid.find_or_create_user(profile)
        self.assertTrue(user)
        self.assertEqual(user.tsc_lao_id, '99999')
        self.assertEqual(user.tsc_user_type, 'employee')
        self.assertEqual(user.login, 'laoid_99999')

    def test_laoid_find_existing_user(self):
        laoid = self.env['tsc.laoid'].sudo()
        profile = {
            'id': '88888',
            'firstName': 'Existing',
            'lastName': 'User',
            'phoneNumber': '2055888888',
            'email': [],
        }
        user1 = laoid.find_or_create_user(profile)
        user2 = laoid.find_or_create_user(profile)
        self.assertEqual(user1.id, user2.id)

    def test_laoid_user_name_fallback(self):
        laoid = self.env['tsc.laoid'].sudo()
        profile = {
            'id': '77777',
            'firstName': '',
            'lastName': '',
            'username': 'fallback_user',
        }
        user = laoid.find_or_create_user(profile)
        self.assertEqual(user.name, 'fallback_user')

    def test_laoid_login_log(self):
        laoid = self.env['tsc.laoid'].sudo()
        user = self.env['res.users'].create({
            'login': 'laoid_log_test',
            'name': 'Log Test',
        })
        laoid.log_login(user, 'laoid', 'success', ip_address='127.0.0.1')
        log = self.env['tsc.login.log'].search([('user_id', '=', user.id)], limit=1)
        self.assertTrue(log)
        self.assertEqual(log.login_type, 'laoid')
        self.assertEqual(log.state, 'success')
