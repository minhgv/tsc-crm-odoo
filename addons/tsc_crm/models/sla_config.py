from odoo import _, fields, models


class TscSlaConfig(models.Model):
    _name = 'tsc.sla.config'
    _description = _('SLA Configuration')
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    stage = fields.Selection([
        ('assignment', _('Reception/Assignment')),
        ('survey', _('Survey/Consultation')),
        ('implementation', _('Implementation')),
        ('contract', _('Contract Signing')),
        ('payment', _('Payment')),
    ], required=True, string=_('Stage'))
    max_hours = fields.Integer(required=True, string=_('Max Hours'))
    warning_hours = fields.Integer(string=_('Warning Hours'))
    applies_to = fields.Selection([
        ('new_order', _('New Order')),
        ('renewal_reminder', _('Renewal Reminder')),
    ], string=_('Applies To'), default='new_order')
    active = fields.Boolean(default=True)
