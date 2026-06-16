from odoo import _, fields, models


class TscService(models.Model):
    _name = 'tsc.service'
    _description = _('Service')
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name, id'
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, unique=True)
    sequence = fields.Integer(default=10)
    logo = fields.Image()
    icon = fields.Image()
    slogan = fields.Text(translate=True)
    description = fields.Html(translate=True)
    banner = fields.Image()
    video_url = fields.Char(string=_('Video URL'))
    target_customer = fields.Selection([
        ('individual', _('Individual')),
        ('business', _('Business')),
        ('government', _('Government')),
    ], string=_('Target Customer'))
    value_proposition = fields.Text(translate=True)
    policy = fields.Html(translate=True)
    distribution_channel = fields.Selection([
        ('online', _('Online')),
        ('offline', _('Offline')),
        ('both', _('Both')),
    ], string=_('Distribution Channel'))
    service_type = fields.Selection([
        ('direct', _('Direct Sale')),
        ('project', _('Project')),
    ], required=True, default='direct')
    active = fields.Boolean(default=True)
    package_ids = fields.One2many('tsc.package', 'service_id', string=_('Packages'))
    combo_line_ids = fields.One2many('tsc.combo.line', 'service_id', string=_('Combo Lines'))
