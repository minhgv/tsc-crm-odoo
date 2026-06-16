from odoo import _, api, fields, models


class TscPayment(models.Model):
    _name = 'tsc.payment'
    _description = _('Payment')
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(required=True, readonly=True, default='New')
    invoice_id = fields.Many2one('tsc.invoice', string=_('Invoice'), required=True, ondelete='cascade')
    amount = fields.Float(required=True)
    payment_method = fields.Selection([
        ('unipay_wallet', _('Unipay Wallet')),
        ('unipay_bank', _('Unipay Bank Transfer')),
        ('qr', _('QR Payment')),
        ('mobile', _('Mobile Balance')),
        ('umoney', _('uMoney')),
        ('cash', _('Cash')),
    ], required=True)
    payment_date = fields.Datetime(default=fields.Datetime.now)
    state = fields.Selection([
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('failed', _('Failed')),
    ], default='pending', tracking=True)
    transaction_id = fields.Char(string=_('Transaction ID'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tsc.payment') or 'New'
        return super().create(vals_list)

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        self.invoice_id.action_pay()

    def action_fail(self):
        self.write({'state': 'failed'})
