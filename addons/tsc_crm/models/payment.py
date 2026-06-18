from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscPayment(models.Model):
    _name = 'tsc.payment'
    _description = _('TSC Payment')
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(string=_('Payment Reference'), readonly=True, copy=False, default='New')
    invoice_id = fields.Many2one('tsc.invoice', string=_('Invoice'), required=True, ondelete='cascade')
    contract_id = fields.Many2one('tsc.contract', string=_('Contract'))
    partner_id = fields.Many2one('res.partner', string=_('Customer'))
    amount = fields.Float(string=_('Amount'), required=True)
    payment_method = fields.Selection([
        ('unipay', _('Unipay')),
        ('umoney', _('uMoney')),
        ('cash', _('Cash')),
        ('bank_transfer', _('Bank Transfer')),
    ], string=_('Payment Method'), required=True)
    payment_date = fields.Datetime(string=_('Payment Date'), default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', _('Draft')),
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    ], string=_('Status'), default='draft', tracking=True)
    transaction_id = fields.Char(string=_('Transaction ID'))
    currency_id = fields.Many2one('res.currency', string=_('Currency'), default=lambda self: self.env.company.currency_id)
    notes = fields.Text(string=_('Notes'))
    error_message = fields.Text(string=_('Error Message'))

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', _('Payment reference must be unique!')),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tsc.payment') or 'New'
            if vals.get('invoice_id') and not vals.get('contract_id'):
                invoice = self.env['tsc.invoice'].browse(vals['invoice_id'])
                vals['contract_id'] = invoice.contract_id.id
                vals['partner_id'] = invoice.partner_id.id
        return super().create(vals_list)

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'pending':
            raise ValidationError(_('Only pending payments can be confirmed'))
        self.write({'state': 'confirmed'})
        self.message_post(body=_('Payment confirmed'))
        self._update_invoice_status()

    def action_fail(self):
        self.ensure_one()
        self.write({'state': 'failed'})
        self.message_post(body=_('Payment failed'))

    def action_refund(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise ValidationError(_('Only confirmed payments can be refunded'))
        self.write({'state': 'refunded'})
        self.message_post(body=_('Payment refunded'))
        self._update_invoice_status()

    def action_submit(self):
        self.ensure_one()
        if self.state != 'draft':
            raise ValidationError(_('Only draft payments can be submitted'))
        self.write({'state': 'pending'})
        self.message_post(body=_('Payment submitted for processing'))

    def _update_invoice_status(self):
        self.ensure_one()
        invoice = self.invoice_id
        invoice.invalidate_recordset(['amount_paid'])
        total_paid = sum(
            invoice.payment_ids.filtered(lambda p: p.state == 'confirmed').mapped('amount')
        )
        if total_paid >= invoice.amount_total:
            invoice.write({'state': 'paid'})
        elif total_paid > 0:
            invoice.message_post(body=_('Partial payment received'))

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'res_model': 'tsc.invoice',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
        }
