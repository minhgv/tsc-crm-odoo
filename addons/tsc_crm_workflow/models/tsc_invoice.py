from odoo import _, api, fields, models


class TscInvoice(models.Model):
    _name = 'tsc.invoice'
    _description = _('Invoice')
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(required=True, readonly=True, default='New')
    lead_id = fields.Many2one('crm.lead', string=_('Order'), required=True, ondelete='cascade')
    contract_id = fields.Many2one('tsc.contract', string=_('Contract'))
    partner_id = fields.Many2one('res.partner', related='lead_id.partner_id', string=_('Customer'))
    state = fields.Selection([
        ('draft', _('Draft')),
        ('posted', _('Posted')),
        ('paid', _('Paid')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    ], default='draft', tracking=True)
    invoice_date = fields.Date(string=_('Invoice Date'), default=fields.Date.today)
    due_date = fields.Date(string=_('Due Date'))
    subtotal = fields.Float(string=_('Subtotal'))
    vat_rate = fields.Float(string=_('VAT Rate'))
    vat_amount = fields.Float(string=_('VAT Amount'), compute='_compute_vat', store=True)
    wht_rate = fields.Float(string=_('WHT Rate'))
    wht_amount = fields.Float(string=_('WHT Amount'), compute='_compute_wht', store=True)
    total = fields.Float(string=_('Total'), compute='_compute_total', store=True)
    currency_id = fields.Many2one('res.currency', string=_('Currency'))
    exchange_rate = fields.Float(string=_('Exchange Rate'))
    exchange_rate_date = fields.Date(string=_('Exchange Rate Date'))
    payment_ids = fields.One2many('tsc.payment', 'invoice_id', string=_('Payments'))
    line_ids = fields.One2many('tsc.invoice.line', 'invoice_id', string=_('Lines'))

    @api.depends('subtotal', 'vat_rate')
    def _compute_vat(self):
        for inv in self:
            inv.vat_amount = inv.subtotal * inv.vat_rate / 100

    @api.depends('subtotal', 'wht_rate')
    def _compute_wht(self):
        for inv in self:
            inv.wht_amount = inv.subtotal * inv.wht_rate / 100

    @api.depends('subtotal', 'vat_amount', 'wht_amount')
    def _compute_total(self):
        for inv in self:
            inv.total = inv.subtotal + inv.vat_amount - inv.wht_amount

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tsc.invoice') or 'New'
        return super().create(vals_list)

    def action_post(self):
        self.write({'state': 'posted'})

    def action_pay(self):
        self.write({'state': 'paid'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_refund(self):
        self.write({'state': 'refunded'})


class TscInvoiceLine(models.Model):
    _name = 'tsc.invoice.line'
    _description = _('Invoice Line')

    invoice_id = fields.Many2one('tsc.invoice', string=_('Invoice'), required=True, ondelete='cascade')
    description = fields.Char(required=True)
    quantity = fields.Float(default=1.0)
    unit_price = fields.Float(required=True)
    amount = fields.Float(string=_('Amount'), compute='_compute_amount', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.unit_price
