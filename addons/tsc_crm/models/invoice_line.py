from odoo import _, api, fields, models


class TscInvoiceLine(models.Model):
    _name = 'tsc.invoice.line'
    _description = _('TSC Invoice Line')
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    invoice_id = fields.Many2one('tsc.invoice', string=_('Invoice'), required=True, ondelete='cascade')
    order_line_id = fields.Many2one('tsc.order.line', string=_('Order Line'))
    description = fields.Char(string=_('Description'), required=True)
    quantity = fields.Float(string=_('Quantity'), default=1.0, required=True)
    unit_price = fields.Float(string=_('Unit Price'), required=True)
    discount = fields.Float(string=_('Discount (%)'), default=0.0)
    amount = fields.Float(string=_('Amount'), compute='_compute_amount', store=True)

    @api.depends('quantity', 'unit_price', 'discount')
    def _compute_amount(self):
        for line in self:
            subtotal = line.quantity * line.unit_price
            line.amount = subtotal * (1 - line.discount / 100.0)
