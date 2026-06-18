from odoo import _, fields, models


class TscPackageLevel(models.Model):
    _name = 'tsc.package.level'
    _description = _('TSC Package Level')
    _order = 'sequence, name, id'
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    package_id = fields.Many2one('tsc.package', string=_('Package'), required=True, ondelete='cascade')
    price = fields.Float(string=_('Price (Kip/month)'), required=True, default=0.0)
    description = fields.Text(string=_('Description'), translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
