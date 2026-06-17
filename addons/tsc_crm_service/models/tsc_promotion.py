from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscPromotion(models.Model):
    _name = 'tsc.promotion'
    _description = _('Promotion')
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    promo_type = fields.Selection([
        ('fixed', _('Fixed Amount')),
        ('percentage', _('Percentage')),
    ], required=True, string=_('Promotion Type'))
    value = fields.Float(required=True, string=_('Value'))
    scope = fields.Selection([
        ('order_line', _('Per Order Line')),
        ('package', _('Per Package')),
        ('service', _('Per Service')),
    ], required=True, string=_('Scope'))
    service_id = fields.Many2one('tsc.service', string=_('Service'))
    package_id = fields.Many2one('tsc.package', string=_('Package'))
    date_from = fields.Date(required=True, string=_('Start Date'))
    date_to = fields.Date(required=True, string=_('End Date'))
    active = fields.Boolean(default=True)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for promo in self:
            if promo.date_from and promo.date_to and promo.date_from > promo.date_to:
                raise ValidationError(_('Start date must be before end date'))

    @api.constrains('value')
    def _check_value(self):
        for promo in self:
            if promo.value < 0:
                raise ValidationError(_('Value cannot be negative'))
            if promo.promo_type == 'percentage' and promo.value > 100:
                raise ValidationError(_('Percentage cannot exceed 100'))
