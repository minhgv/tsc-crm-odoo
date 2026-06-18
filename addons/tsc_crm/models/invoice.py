from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscInvoice(models.Model):
    _name = 'tsc.invoice'
    _description = _('TSC Invoice')
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(string=_('Invoice Number'), readonly=True, copy=False, default='New')
    contract_id = fields.Many2one('tsc.contract', string=_('Contract'), required=True, ondelete='cascade')
    lead_id = fields.Many2one('crm.lead', string=_('Order'))
    partner_id = fields.Many2one('res.partner', string=_('Customer'))
    invoice_date = fields.Date(string=_('Invoice Date'), default=fields.Date.context_today)
    due_date = fields.Date(string=_('Due Date'))
    state = fields.Selection([
        ('draft', _('Draft')),
        ('posted', _('Posted')),
        ('paid', _('Paid')),
        ('cancelled', _('Cancelled')),
        ('refund', _('Refunded')),
    ], string=_('Status'), default='draft', tracking=True)
    invoice_line_ids = fields.One2many('tsc.invoice.line', 'invoice_id', string=_('Invoice Lines'))
    payment_ids = fields.One2many('tsc.payment', 'invoice_id', string=_('Payments'))
    amount_untaxed = fields.Float(string=_('Untaxed Amount'), compute='_compute_amounts', store=True)
    vat_rate = fields.Float(string=_('VAT Rate (%)'), default=7.0)
    vat_amount = fields.Float(string=_('VAT Amount'), compute='_compute_amounts', store=True)
    wht_rate = fields.Float(string=_('WHT Rate (%)'), default=0.0)
    wht_amount = fields.Float(string=_('WHT Amount'), compute='_compute_amounts', store=True)
    amount_total = fields.Float(string=_('Total'), compute='_compute_amounts', store=True)
    amount_paid = fields.Float(string=_('Amount Paid'), compute='_compute_amount_paid', store=True)
    currency_id = fields.Many2one('res.currency', string=_('Currency'), default=lambda self: self.env.company.currency_id)
    notes = fields.Text(string=_('Notes'))
    payment_method = fields.Selection([
        ('unipay', _('Unipay')),
        ('umoney', _('uMoney')),
        ('cash', _('Cash')),
        ('bank_transfer', _('Bank Transfer')),
    ], string=_('Payment Method'))

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', _('Invoice number must be unique!')),
    ]

    @api.depends('invoice_line_ids.amount', 'vat_rate', 'wht_rate')
    def _compute_amounts(self):
        for invoice in self:
            untaxed = sum(invoice.invoice_line_ids.mapped('amount'))
            vat_amount = untaxed * (invoice.vat_rate / 100.0)
            wht_amount = untaxed * (invoice.wht_rate / 100.0)
            invoice.amount_untaxed = untaxed
            invoice.vat_amount = vat_amount
            invoice.wht_amount = wht_amount
            invoice.amount_total = untaxed + vat_amount - wht_amount

    @api.depends('payment_ids.amount', 'payment_ids.state')
    def _compute_amount_paid(self):
        for invoice in self:
            invoice.amount_paid = sum(
                invoice.payment_ids.filtered(lambda p: p.state == 'confirmed').mapped('amount')
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tsc.invoice') or 'New'
            if vals.get('contract_id') and not vals.get('lead_id'):
                contract = self.env['tsc.contract'].browse(vals['contract_id'])
                vals['lead_id'] = contract.lead_id.id
                vals['partner_id'] = contract.partner_id.id
        return super().create(vals_list)

    def action_post(self):
        self.ensure_one()
        if self.state != 'draft':
            raise ValidationError(_('Only draft invoices can be posted'))
        if not self.invoice_line_ids:
            raise ValidationError(_('Cannot post invoice without lines'))
        self.write({'state': 'posted'})
        self.message_post(body=_('Invoice posted'))

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'paid':
            raise ValidationError(_('Paid invoices cannot be cancelled'))
        self.write({'state': 'cancelled'})
        self.message_post(body=_('Invoice cancelled'))

    def action_draft(self):
        self.ensure_one()
        if self.state != 'cancelled':
            raise ValidationError(_('Only cancelled invoices can be reset to draft'))
        self.write({'state': 'draft'})
        self.message_post(body=_('Invoice reset to draft'))

    def action_refund(self):
        self.ensure_one()
        if self.state not in ('posted', 'paid'):
            raise ValidationError(_('Only posted or paid invoices can be refunded'))
        self.write({'state': 'refund'})
        self.message_post(body=_('Invoice refunded'))

    def action_view_contract(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Contract'),
            'res_model': 'tsc.contract',
            'res_id': self.contract_id.id,
            'view_mode': 'form',
        }

    def action_view_payments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments'),
            'res_model': 'tsc.payment',
            'view_mode': 'list,form',
            'domain': [('invoice_id', '=', self.id)],
            'context': {'default_invoice_id': self.id},
        }
