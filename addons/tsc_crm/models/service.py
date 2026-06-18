from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscService(models.Model):
    _name = 'tsc.service'
    _description = _('TSC Service')
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name, id'
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, size=20)
    service_type = fields.Selection([
        ('direct', _('Direct Sale')),
        ('project', _('Project')),
    ], string=_('Service Type'), required=True, default='direct')
    description = fields.Text(translate=True)
    logo = fields.Image(string=_('Logo'), max_width=256, max_height=256)
    banner = fields.Image(string=_('Banner'), max_width=1920, max_height=1080)
    video_url = fields.Char(string=_('Video URL'))
    target_customer = fields.Selection([
        ('individual', _('Individual')),
        ('business', _('Business')),
        ('government', _('Government')),
        ('all', _('All')),
    ], string=_('Target Customer'), default='all')
    value_proposition = fields.Text(string=_('Value Proposition'), translate=True)
    policies = fields.Text(string=_('Policies'), translate=True)
    channel = fields.Selection([
        ('online', _('Online')),
        ('offline', _('Offline')),
        ('both', _('Both')),
    ], string=_('Distribution Channel'), default='both')
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    package_ids = fields.One2many('tsc.package', 'service_id', string=_('Packages'))
    total_packages = fields.Integer(compute='_compute_total_packages', store=True)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', _('Service code must be unique!')),
    ]

    @api.depends('package_ids')
    def _compute_total_packages(self):
        for service in self:
            service.total_packages = len(service.package_ids)

    @api.constrains('code')
    def _check_code_length(self):
        for service in self:
            if service.code and len(service.code) < 2:
                raise ValidationError(_('Service code must be at least 2 characters'))

    def action_view_packages(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Packages'),
            'res_model': 'tsc.package',
            'view_mode': 'list,form',
            'domain': [('service_id', '=', self.id)],
            'context': {'default_service_id': self.id},
        }
