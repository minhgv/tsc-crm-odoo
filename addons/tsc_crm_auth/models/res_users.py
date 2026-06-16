from odoo import _, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    tsc_user_type = fields.Selection([
        ('backend', _('Backend User')),
        ('customer', _('Customer')),
        ('employee', _('Employee')),
    ], default='backend', string=_('User Type'))
    tsc_phone = fields.Char(string=_('Phone'))
    tsc_lao_id = fields.Char(string=_('LaoID'))
    tsc_is_active = fields.Boolean(default=True, string=_('TSC Active'))
    tsc_last_login = fields.Datetime(string=_('Last Login'))
    tsc_login_count = fields.Integer(default=0, string=_('Login Count'))
