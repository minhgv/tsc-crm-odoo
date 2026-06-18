from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscWht(models.Model):
    _name = 'tsc.wht'
    _description = _('TSC WHT Configuration')
    _order = 'date_from desc'
    _rec_name = 'name'

    name = fields.Char(string=_('Description'), required=True)
    rate = fields.Float(string=_('WHT Rate (%)'), required=True)
    date_from = fields.Date(string=_('Valid From'), required=True)
    date_to = fields.Date(string=_('Valid To'))
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string=_('Company'), default=lambda self: self.env.company)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for wht in self:
            if wht.date_to and wht.date_from > wht.date_to:
                raise ValidationError(_('Valid From must be before Valid To'))

    @api.constrains('rate')
    def _check_rate(self):
        for wht in self:
            if wht.rate < 0 or wht.rate > 100:
                raise ValidationError(_('WHT rate must be between 0 and 100'))

    @api.model
    def _get_current_rate(self, date=None):
        """Get WHT rate applicable on a given date"""
        if not date:
            date = fields.Date.context_today(self)
        domain = [
            ('date_from', '<=', date),
            ('active', '=', True),
            '|',
            ('date_to', '>=', date),
            ('date_to', '=', False),
        ]
        wht = self.search(domain, order='date_from desc', limit=1)
        return wht.rate if wht else 0.0
