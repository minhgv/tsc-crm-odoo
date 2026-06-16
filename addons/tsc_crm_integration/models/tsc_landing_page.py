from odoo import _, fields, models


class TscLandingPage(models.Model):
    _name = 'tsc.landing.page'
    _description = _('Landing Page Configuration')

    name = fields.Char(required=True)
    logo = fields.Image()
    slogan = fields.Char()
    banner = fields.Image()
    service_ids = fields.Many2many('tsc.service', string=_('Services'))
    seo_title = fields.Char(string=_('SEO Title'))
    seo_description = fields.Text(string=_('SEO Description'))
    active = fields.Boolean(default=True)
