import logging
import secrets
from werkzeug.utils import redirect
from odoo import fields, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class TscAuthController(http.Controller):

    @http.route('/auth/laoid', type='http', auth='none', methods=['GET'])
    def laoid_login(self, **kwargs):
        ICP = request.env['ir.config_parameter'].sudo()
        base_url = ICP.get_param('tsc.laoid.base_url', 'https://sso.laoid.net')
        client_id = ICP.get_param('tsc.laoid.client_id', '')
        callback_url = ICP.get_param('tsc.laoid.callback_url', '')

        if not client_id or not callback_url:
            _logger.error("LaoID SSO not configured: missing client_id or callback_url")
            return request.redirect('/web/login?error=laoid_not_configured')

        sso_url = (
            f"{base_url}/login"
            f"?client_id={client_id}"
            f"&redirect_uri={callback_url}"
            f"&use_callback_uri=true"
        )
        return redirect(sso_url)

    @http.route('/auth/laoid/callback', type='http', auth='none', methods=['GET'])
    def laoid_callback(self, **kwargs):
        authorization_code = kwargs.get('authorization_code')
        if not authorization_code:
            _logger.warning("LaoID callback: no authorization_code")
            return request.redirect('/web/login?error=no_auth_code')

        laoid = request.env['tsc.laoid'].sudo()
        access_token = laoid.get_access_token(authorization_code)
        if not access_token:
            _logger.warning("LaoID callback: token exchange failed")
            return request.redirect('/web/login?error=token_exchange_failed')

        profile = laoid.get_user_profile(access_token)
        if not profile:
            _logger.warning("LaoID callback: failed to get profile")
            return request.redirect('/web/login?error=profile_fetch_failed')

        user = laoid.find_or_create_user(profile)

        if not user.active or not user.tsc_is_active:
            _logger.warning("LaoID login: user %s is inactive", user.login)
            laoid.log_login(user, 'laoid', 'failed',
                            ip_address=http.request.httprequest.remote_addr,
                            user_agent=http.request.httprequest.user_agent.string,
                            failure_reason='User inactive')
            return request.redirect('/web/login?error=account_inactive')

        user.sudo().write({
            'tsc_last_login': fields.Datetime.now(),
        })
        self.env.cr.execute(
            "UPDATE res_users SET tsc_login_count = tsc_login_count + 1 WHERE id = %s",
            (user.id,),
        )

        laoid.log_login(user, 'laoid', 'success',
                        ip_address=http.request.httprequest.remote_addr,
                        user_agent=http.request.httprequest.user_agent.string)

        db = request.session.db or request.db
        new_password = secrets.token_urlsafe(16)
        user.sudo()._set_password(new_password)
        request.session.authenticate(db, user.login, new_password)
        request.session.login = 'laoid'
        return redirect('/web')

    @http.route('/api/auth/otp/send', type='json', auth='public', methods=['POST'])
    def send_otp(self, **kwargs):
        phone = kwargs.get('phone')
        if not phone:
            return {'error': 'Phone number required'}
        code = request.env['tsc.otp.code']._generate_otp(phone, 'login')
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
