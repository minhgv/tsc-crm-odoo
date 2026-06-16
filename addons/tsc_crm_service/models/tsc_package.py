from odoo import _, api, fields, models


class TscPackage(models.Model):
    _name = 'tsc.package'
    _description = _('Package')
    _order = 'sequence, name, id'
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    service_id = fields.Many2one('tsc.service', string=_('Service'), required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    level_ids = fields.One2many('tsc.package.level', 'package_id', string=_('Levels'))
    deployment_fee = fields.Float(string=_('Deployment Fee'))
    package_type = fields.Selection([
        ('per_use', _('Per Use')),
        ('cycle', _('Cycle')),
    ], required=True, default='per_use')
    trial_days = fields.Integer(string=_('Trial Days'))
    validity_days = fields.Integer(string=_('Validity Days'))
    description = fields.Html(translate=True)
    logo = fields.Image()
    notes = fields.Text(translate=True)
    active = fields.Boolean(default=True)


class TscPackageLevel(models.Model):
    _name = 'tsc.package.level'
    _description = _('Package Level')
    _order = 'sequence, id'

    name = fields.Char(required=True, translate=True)
    package_id = fields.Many2one('tsc.package', string=_('Package'), required=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    price = fields.Float(required=True)
    currency_id = fields.Many2one('res.currency', string=_('Currency'))
    description = fields.Text(translate=True)
