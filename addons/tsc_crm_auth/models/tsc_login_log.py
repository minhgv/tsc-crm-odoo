from odoo import _, fields, models


class TscLoginLog(models.Model):
    _name = 'tsc.login.log'
    _description = _('Login Log')
    _order = 'login_date desc'

    user_id = fields.Many2one('res.users', string=_('User'))
    login_type = fields.Selection([
        ('backend', _('Backend')),
        ('otp', _('OTP')),
        ('laoid', _('LaoID')),
    ], required=True)
    state = fields.Selection([
        ('success', _('Success')),
        ('failed', _('Failed')),
    ], required=True)
    ip_address = fields.Char()
    user_agent = fields.Char()
    login_date = fields.Datetime(default=fields.Datetime.now)
    failure_reason = fields.Char()
