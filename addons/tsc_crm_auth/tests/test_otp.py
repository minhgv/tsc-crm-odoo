from odoo.tests.common import TransactionCase


class TestTscOtp(TransactionCase):

    def test_otp_generation(self):
        otp = self.env['tsc.otp.code']._generate_otp('2055123456', 'login')
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())

    def test_otp_verify_correct(self):
        code = self.env['tsc.otp.code']._generate_otp('2055123456', 'login')
        result = self.env['tsc.otp.code']._verify_otp('2055123456', code, 'login')
        self.assertTrue(result)

    def test_otp_verify_wrong_code(self):
        self.env['tsc.otp.code']._generate_otp('2055123456', 'login')
        result = self.env['tsc.otp.code']._verify_otp('2055123456', '000000', 'login')
        self.assertFalse(result)

    def test_otp_verify_wrong_phone(self):
        code = self.env['tsc.otp.code']._generate_otp('2055123456', 'login')
        result = self.env['tsc.otp.code']._verify_otp('2055999999', code, 'login')
        self.assertFalse(result)

    def test_otp_verify_wrong_purpose(self):
        code = self.env['tsc.otp.code']._generate_otp('2055123456', 'login')
        result = self.env['tsc.otp.code']._verify_otp('2055123456', code, 'register')
        self.assertFalse(result)

    def test_otp_max_attempts(self):
        code = self.env['tsc.otp.code']._generate_otp('2055123456', 'login')
        for i in range(3):
            self.env['tsc.otp.code']._verify_otp('2055123456', '000000', 'login')
        result = self.env['tsc.otp.code']._verify_otp('2055123456', code, 'login')
        self.assertFalse(result)

    def test_otp_multiple_purposes(self):
        code_login = self.env['tsc.otp.code']._generate_otp('2055123456', 'login')
        code_register = self.env['tsc.otp.code']._generate_otp('2055123456', 'register')
        self.assertTrue(self.env['tsc.otp.code']._verify_otp('2055123456', code_login, 'login'))
        self.assertTrue(self.env['tsc.otp.code']._verify_otp('2055123456', code_register, 'register'))
