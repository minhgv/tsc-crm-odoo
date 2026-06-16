from odoo import http
from odoo.http import request


class TscAuthController(http.Controller):

    @http.route('/api/auth/otp/send', type='json', auth='public', methods=['POST'])
    def send_otp(self, **kwargs):
        phone = kwargs.get('phone')
        if not phone:
            return {'error': 'Phone number required'}
        code = request.env['tsc.otp.code']._generate_otp(phone, 'login')
        # TODO: integrate SMS gateway
        return {'success': True, 'message': 'OTP sent'}

    @http.route('/api/auth/otp/verify', type='json', auth='public', methods=['POST'])
    def verify_otp(self, **kwargs):
        phone = kwargs.get('phone')
        code = kwargs.get('code')
        if not phone or not code:
            return {'error': 'Phone and code required'}
        verified = request.env['tsc.otp.code']._verify_otp(phone, code, 'login')
        if not verified:
            return {'error': 'Invalid or expired OTP'}
        user = request.env['res.users'].sudo().search([('tsc_phone', '=', phone)], limit=1)
        if not user:
            return {'error': 'User not found'}
        # TODO: create session/token
        return {'success': True, 'user_id': user.id, 'name': user.name}

    @http.route('/api/auth/register', type='json', auth='public', methods=['POST'])
    def register(self, **kwargs):
        name = kwargs.get('name')
        phone = kwargs.get('phone')
        email = kwargs.get('email')
        password = kwargs.get('password')
        otp_code = kwargs.get('otp_code')
        if not all([name, phone, password, otp_code]):
            return {'error': 'Missing required fields'}
        wizard = request.env['tsc.customer.registration'].sudo().create({
            'name': name,
            'phone': phone,
            'email': email,
            'password': password,
            'otp_code': otp_code,
        })
        try:
            wizard.action_register()
        except Exception as e:
            return {'error': str(e)}
        return {'success': True, 'message': 'Registration successful'}
