import logging
import secrets
import requests
from odoo import api, models

_logger = logging.getLogger(__name__)

LAOID_BASE_URL = {
    'production': 'https://sso.laoid.net',
    'uat': 'https://uatcrm.laoid.net',
}


class TscLaoID(models.AbstractModel):
    _name = 'tsc.laoid'
    _description = 'LaoID SSO API Helper'

    @api.model
    def _get_base_url(self):
        ICP = self.env['ir.config_parameter'].sudo()
        env_type = ICP.get_param('tsc.laoid.environment', 'production')
        return LAOID_BASE_URL.get(env_type, LAOID_BASE_URL['production'])

    @api.model
    def _get_client_id(self):
        return self.env['ir.config_parameter'].sudo().get_param('tsc.laoid.client_id', '')

    @api.model
    def _get_client_secret(self):
        return self.env['ir.config_parameter'].sudo().get_param('tsc.laoid.client_secret', '')

    @api.model
    def get_access_token(self, authorization_code):
        base_url = self._get_base_url()
        url = f"{base_url}/api/v1/third-party/verify"
        payload = {
            'code': authorization_code,
            'clientId': self._get_client_id(),
            'clientSecret': self._get_client_secret(),
        }
        try:
            resp = requests.post(url, json=payload, timeout=30, verify=False)
            resp.raise_for_status()
            data = resp.json()
            if data.get('success'):
                return data['data']['accessToken']
            _logger.warning("LaoID verify failed: %s", data)
        except Exception:
            _logger.exception("LaoID get_access_token error")
        return None

    @api.model
    def get_user_profile(self, access_token):
        base_url = self._get_base_url()
        url = f"{base_url}/api/v1/third-party/me"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'x-api-key': self._get_client_id(),
        }
        try:
            resp = requests.get(url, headers=headers, timeout=30, verify=False)
            resp.raise_for_status()
            data = resp.json()
            if data.get('success'):
                return data['data']
            _logger.warning("LaoID get profile failed: %s", data)
        except Exception:
            _logger.exception("LaoID get_user_profile error")
        return None

    @api.model
    def find_or_create_user(self, profile):
        User = self.env['res.users'].sudo()
        laoid_id = str(profile.get('id', ''))

        user = User.search([('tsc_lao_id', '=', laoid_id)], limit=1)

        first_name = profile.get('firstName', '') or ''
        last_name = profile.get('lastName', '') or ''
        name = f"{first_name} {last_name}".strip()
        if not name:
            name = profile.get('username', laoid_id)

        emails = profile.get('email', [])
        email = ''
        if emails:
            for e in emails:
                if e.get('primary'):
                    email = e['email']
                    break
            if not email and emails:
                email = emails[0].get('email', '')

        phone = profile.get('phoneNumber', '')

        if user:
            vals = {'name': name}
            if email and not user.email:
                vals['email'] = email
            if phone and not user.tsc_phone:
                vals['tsc_phone'] = phone
            user.write(vals)
            return user

        login = f"laoid_{laoid_id}"
        random_password = secrets.token_urlsafe(16)
        partner = self.env['res.partner'].create({
            'name': name,
            'email': email,
            'phone': phone,
        })
        user = User.create({
            'login': login,
            'name': name,
            'email': email,
            'partner_id': partner.id,
            'tsc_user_type': 'employee',
            'tsc_lao_id': laoid_id,
            'tsc_phone': phone,
            'groups_id': [(4, self.env.ref('base.group_user').id)],
        })
        user._set_password(random_password)
        return user

    @api.model
    def log_login(self, user, login_type, state, ip_address=None, user_agent=None, failure_reason=None):
        self.env['tsc.login.log'].sudo().create({
            'user_id': user.id if user else False,
            'login_type': login_type,
            'state': state,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'failure_reason': failure_reason,
        })
