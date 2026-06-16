from odoo import _, fields, models


class TscCommissionRule(models.Model):
    _name = 'tsc.commission.rule'
    _description = _('Commission Rule')
    _rec_name = 'name'

    name = fields.Char(required=True)
    service_id = fields.Many2one('tsc.service', string=_('Service'))
    package_id = fields.Many2one('tsc.package', string=_('Package'))
    agency_id = fields.Many2one('tsc.agency', string=_('Agency'))
    commission_type = fields.Selection([
        ('percentage', _('Percentage')),
        ('fixed', _('Fixed Amount')),
    ], required=True)
    rate = fields.Float(required=True)
    min_revenue = fields.Float(string=_('Min Revenue'))
    max_revenue = fields.Float(string=_('Max Revenue'))
    target_group = fields.Selection([
        ('am', _('AM Province')),
        ('agency', _('Agency')),
        ('staff', _('Staff')),
        ('management', _('Management')),
    ], required=True)
    active = fields.Boolean(default=True)
