from odoo import _, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tsc_customer_code = fields.Char(string=_('Customer Code'), unique=True, readonly=True)
    tsc_customer_type = fields.Selection([
        ('individual', _('Individual/Household')),
        ('business', _('Business')),
        ('government', _('Government')),
    ], string=_('Customer Type'))
