from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscCustomerRegistration(models.TransientModel):
    _name = 'tsc.customer.registration'
    _description = _('Customer Registration')

    name = fields.Char(required=True)
    phone = fields.Char(required=True)
    email = fields.Char()
    password = fields.Char(required=True)
    otp_code = fields.Char(required=True, string=_('OTP Code'))

    def action_register(self):
        self.ensure_one()
        otp_model = self.env['tsc.otp.code']
        if not otp_model._verify_otp(self.phone, self.otp_code, 'register'):
            raise ValidationError(_('Invalid or expired OTP code'))
        partner = self.env['res.partner'].create({
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
        })
        self.env['res.users'].create({
            'login': self.phone,
            'name': self.name,
            'partner_id': partner.id,
            'password': self.password,
            'tsc_user_type': 'customer',
            'tsc_phone': self.phone,
            'groups_id': [(4, self.env.ref('base.group_user').id)],
        })
        return {'type': 'ir.actions.act_window_close'}
