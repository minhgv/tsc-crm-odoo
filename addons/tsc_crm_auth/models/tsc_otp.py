from odoo import _, api, fields, models


class TscOtpCode(models.Model):
    _name = 'tsc.otp.code'
    _description = _('OTP Code')
    _order = 'id desc'

    phone = fields.Char(required=True, index=True)
    code = fields.Char(required=True)
    purpose = fields.Selection([
        ('login', _('Login')),
        ('register', _('Register')),
        ('reset_password', _('Reset Password')),
    ], required=True)
    state = fields.Selection([
        ('pending', _('Pending')),
        ('verified', _('Verified')),
        ('expired', _('Expired')),
    ], default='pending', required=True)
    expires_at = fields.Datetime(required=True)
    ip_address = fields.Char()
    attempts = fields.Integer(default=0)

    @api.model
    def _generate_otp(self, phone, purpose, ip_address=None):
        from datetime import timedelta
        import random
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        expires = fields.Datetime.now() + timedelta(minutes=5)
        self.create({
            'phone': phone,
            'code': code,
            'purpose': purpose,
            'expires_at': expires,
            'ip_address': ip_address,
        })
        return code

    def _verify_otp(self, phone, code, purpose):
        record = self.search([
            ('phone', '=', phone),
            ('purpose', '=', purpose),
            ('state', '=', 'pending'),
        ], order='id desc', limit=1)
        if not record:
            return False
        if record.expires_at < fields.Datetime.now():
            record.write({'state': 'expired'})
            return False
        if record.attempts >= 3:
            record.write({'state': 'expired'})
            return False
        if record.code != code:
            record.write({'attempts': record.attempts + 1})
            return False
        record.write({'state': 'verified'})
        return True
