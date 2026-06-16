from odoo import _, fields, models


class TscIntegrationConfig(models.Model):
    _name = 'tsc.integration.config'
    _description = _('Integration Configuration')

    name = fields.Char(required=True)
    system = fields.Selection([
        ('unipay', _('Unipay')),
        ('bccs3', _('BCCS3')),
        ('datalake', _('Datalake')),
        ('voffice', _('Voffice')),
        ('sms', _('SMS Gateway')),
    ], required=True)
    api_url = fields.Char(string=_('API URL'))
    api_key = fields.Char(string=_('API Key'))
    active = fields.Boolean(default=True)


class TscIntegrationLog(models.Model):
    _name = 'tsc.integration.log'
    _description = _('Integration Log')
    _order = 'id desc'

    config_id = fields.Many2one('tsc.integration.config', string=_('Config'))
    direction = fields.Selection([
        ('inbound', _('Inbound')),
        ('outbound', _('Outbound')),
    ])
    request_data = fields.Text()
    response_data = fields.Text()
    state = fields.Selection([
        ('success', _('Success')),
        ('failed', _('Failed')),
    ])
    error_message = fields.Text()
    created_date = fields.Datetime(default=fields.Datetime.now)
