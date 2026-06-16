from odoo import _, fields, models


class TscVatConfig(models.Model):
    _name = 'tsc.vat.config'
    _description = _('VAT Configuration')

    name = fields.Char(required=True)
    rate = fields.Float(required=True)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    active = fields.Boolean(default=True)


class TscWhtConfig(models.Model):
    _name = 'tsc.wht.config'
    _description = _('WHT Configuration')

    name = fields.Char(required=True)
    rate = fields.Float(required=True)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    active = fields.Boolean(default=True)


class TscExchangeRate(models.Model):
    _name = 'tsc.exchange.rate'
    _description = _('Exchange Rate')

    date = fields.Date(required=True, unique=True)
    buy_rate = fields.Float(required=True, string=_('Buy Rate'))
    sell_rate = fields.Float(required=True, string=_('Sell Rate'))
    source = fields.Char(default='BCEL')


class TscSlaConfig(models.Model):
    _name = 'tsc.sla.config'
    _description = _('SLA Configuration')

    name = fields.Char(required=True)
    stage = fields.Selection([
        ('assignment', _('Assignment')),
        ('survey', _('Survey')),
        ('contract', _('Contract')),
        ('payment', _('Payment')),
    ], required=True)
    unit = fields.Selection([
        ('minutes', _('Minutes')),
        ('hours', _('Hours')),
        ('days', _('Days')),
    ], required=True)
    value = fields.Integer(required=True)
    apply_type = fields.Selection([
        ('24h', _('24 Hours')),
        ('working_hours', _('Working Hours')),
    ], required=True)
    working_hours_from = fields.Float(string=_('Working Hours From'))
    working_hours_to = fields.Float(string=_('Working Hours To'))
