from odoo import _, fields, models


class TscDiscount(models.Model):
    _name = 'tsc.discount'
    _description = _('Discount')
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    discount_type = fields.Selection([
        ('line_discount', _('Line Discount')),
        ('promotion', _('Promotion')),
        ('commission', _('Commission')),
    ], required=True)
    service_id = fields.Many2one('tsc.service', string=_('Service'))
    package_id = fields.Many2one('tsc.package', string=_('Package'))
    agency_id = fields.Many2one('tsc.agency', string=_('Agency'))
    percentage = fields.Float(string=_('Percentage'))
    amount = fields.Float(string=_('Fixed Amount'))
    start_date = fields.Date(string=_('Start Date'))
    end_date = fields.Date(string=_('End Date'))
    active = fields.Boolean(default=True)
