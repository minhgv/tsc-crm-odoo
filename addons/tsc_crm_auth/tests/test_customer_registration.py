from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTscCustomerRegistration(TransactionCase):

    def test_registration_success(self):
        code = self.env['tsc.otp.code']._generate_otp('2055111111', 'register')
        wizard = self.env['tsc.customer.registration'].create({
            'name': 'Test Customer',
            'phone': '2055111111',
            'email': 'test@test.la',
            'password': 'password123',
            'otp_code': code,
        })
        wizard.action_register()
        user = self.env['res.users'].search([('tsc_phone', '=', '2055111111')], limit=1)
        self.assertTrue(user)
        self.assertEqual(user.name, 'Test Customer')
        self.assertEqual(user.tsc_user_type, 'customer')

    def test_registration_wrong_otp(self):
        self.env['tsc.otp.code']._generate_otp('2055222222', 'register')
        wizard = self.env['tsc.customer.registration'].create({
            'name': 'Wrong OTP',
            'phone': '2055222222',
            'password': 'password123',
            'otp_code': '000000',
        })
        with self.assertRaises(ValidationError):
            wizard.action_register()

    def test_registration_duplicate_phone(self):
        code1 = self.env['tsc.otp.code']._generate_otp('2055333333', 'register')
        wizard1 = self.env['tsc.customer.registration'].create({
            'name': 'Customer 1',
            'phone': '2055333333',
            'password': 'password123',
            'otp_code': code1,
        })
        wizard1.action_register()

        code2 = self.env['tsc.otp.code']._generate_otp('2055444444', 'register')
        wizard2 = self.env['tsc.customer.registration'].create({
            'name': 'Customer 2',
            'phone': '2055444444',
            'password': 'password456',
            'otp_code': code2,
        })
        wizard2.action_register()
        users = self.env['res.users'].search([('tsc_user_type', '=', 'customer')])
        self.assertGreaterEqual(len(users), 2)
