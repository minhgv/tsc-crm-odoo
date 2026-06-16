from odoo import _, fields, models


class TscNotificationTemplate(models.Model):
    _name = 'tsc.notification.template'
    _description = _('Notification Template')

    name = fields.Char(required=True)
    notification_type = fields.Selection([
        ('sms', _('SMS')),
        ('email', _('Email')),
        ('push', _('Push Notification')),
    ], required=True)
    trigger_event = fields.Selection([
        ('new_order', _('New Order')),
        ('order_assigned', _('Order Assigned')),
        ('order_transferred', _('Order Transferred')),
        ('order_overdue', _('Order Overdue')),
        ('contract_signed', _('Contract Signed')),
        ('invoice_created', _('Invoice Created')),
        ('payment_received', _('Payment Received')),
    ], required=True)
    subject = fields.Char(string=_('Subject'))
    body = fields.Text(required=True)
    active = fields.Boolean(default=True)


class TscNotificationLog(models.Model):
    _name = 'tsc.notification.log'
    _description = _('Notification Log')
    _order = 'id desc'

    template_id = fields.Many2one('tsc.notification.template', string=_('Template'))
    recipient = fields.Char(required=True)
    notification_type = fields.Selection([
        ('sms', _('SMS')),
        ('email', _('Email')),
        ('push', _('Push Notification')),
    ])
    body = fields.Text()
    state = fields.Selection([
        ('pending', _('Pending')),
        ('sent', _('Sent')),
        ('failed', _('Failed')),
    ], default='pending')
    sent_date = fields.Datetime()
    error_message = fields.Text()
