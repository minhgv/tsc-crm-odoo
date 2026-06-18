from odoo import _, fields, models


class TscPackage(models.Model):
    _name = 'tsc.package'
    _description = _('TSC Package')
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name, id'
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, size=30)
    service_id = fields.Many2one('tsc.service', string=_('Service'), required=True, ondelete='cascade')
    package_type = fields.Selection([
        ('one_time', _('One Time')),
        ('cycle', _('Cycle')),
    ], string=_('Package Type'), required=True, default='cycle')
    trial_days = fields.Integer(string=_('Trial Days'), default=0)
    validity_days = fields.Integer(string=_('Validity Days'), default=30)
    setup_fee = fields.Float(string=_('Setup Fee'), default=0.0)
    description = fields.Text(string=_('Description'), translate=True)
    logo = fields.Image(string=_('Logo'), max_width=256, max_height=256)
    image_ids = fields.One2many('ir.attachment', 'res_id', string=_('Images'),
                                domain=[('res_model', '=', 'tsc.package')])
    notes = fields.Text(string=_('Notes'), translate=True)
    level_ids = fields.One2many('tsc.package.level', 'package_id', string=_('Price Levels'))
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    is_combo = fields.Boolean(string=_('Combo Package'), default=False)
    combo_service_ids = fields.Many2many('tsc.service', string=_('Combo Services'))

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', _('Package code must be unique!')),
    ]
