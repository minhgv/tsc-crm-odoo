from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscDiscountPolicy(models.Model):
    _name = 'tsc.discount.policy'
    _description = _('Discount Policy')
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    discount_type = fields.Selection([
        ('revenue', _('By Revenue')),
        ('order_count', _('By Order Count')),
    ], required=True, string=_('Discount Type'))
    discount_mode = fields.Selection([
        ('fixed', _('Fixed Amount')),
        ('percentage', _('Percentage')),
    ], required=True, string=_('Discount Mode'))
    value = fields.Float(required=True, string=_('Value'))
    scope = fields.Selection([
        ('all_agents', _('All Agents')),
        ('specific_agent', _('Specific Agent')),
    ], required=True, string=_('Scope'))
    agency_ids = fields.Many2many('tsc.agency', string=_('Agencies'))
    date_from = fields.Date(string=_('Start Date'))
    date_to = fields.Date(string=_('End Date'))
    active = fields.Boolean(default=True)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for policy in self:
            if policy.date_from and policy.date_to and policy.date_from > policy.date_to:
                raise ValidationError(_('Start date must be before end date'))

    @api.constrains('value')
    def _check_value(self):
        for policy in self:
            if policy.value < 0:
                raise ValidationError(_('Value cannot be negative'))
            if policy.discount_mode == 'percentage' and policy.value > 100:
                raise ValidationError(_('Percentage cannot exceed 100'))

    @api.constrains('scope', 'agency_ids')
    def _check_scope_agency(self):
        for policy in self:
            if policy.scope == 'specific_agent' and not policy.agency_ids:
                raise ValidationError(_('Please select at least one agency'))
