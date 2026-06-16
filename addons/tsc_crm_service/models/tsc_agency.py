from odoo import _, fields, models


class TscAgency(models.Model):
    _name = 'tsc.agency'
    _description = _('Agency')
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, unique=True)
    contact_name = fields.Char(string=_('Contact Name'))
    phone = fields.Char()
    email = fields.Char()
    address = fields.Text()
    revenue_tier = fields.Selection([
        ('tier1', _('Tier 1')),
        ('tier2', _('Tier 2')),
        ('tier3', _('Tier 3')),
    ], string=_('Revenue Tier'))
    active = fields.Boolean(default=True)
