from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscVat(models.Model):
    _name = 'tsc.vat'
    _description = _('TSC VAT Configuration')
    _order = 'date_from desc'
    _rec_name = 'name'

    name = fields.Char(string=_('Description'), required=True)
    rate = fields.Float(string=_('VAT Rate (%)'), required=True)
    date_from = fields.Date(string=_('Valid From'), required=True)
    date_to = fields.Date(string=_('Valid To'))
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string=_('Company'), default=lambda self: self.env.company)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for vat in self:
            if vat.date_to and vat.date_from > vat.date_to:
                raise ValidationError(_('Valid From must be before Valid To'))

    @api.constrains('rate')
    def _check_rate(self):
        for vat in self:
            if vat.rate < 0 or vat.rate > 100:
                raise ValidationError(_('VAT rate must be between 0 and 100'))

    @api.model
    def _get_current_rate(self, date=None):
        """Get VAT rate applicable on a given date"""
        if not date:
            date = fields.Date.context_today(self)
        domain = [
            ('date_from', '<=', date),
            ('active', '=', True),
            '|',
            ('date_to', '>=', date),
            ('date_to', '=', False),
        ]
        vat = self.search(domain, order='date_from desc', limit=1)
        return vat.rate if vat else 0.0
