from odoo import _, api, fields, models


class TscOrderLine(models.Model):
    _name = 'tsc.order.line'
    _description = _('Order Line')
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    lead_id = fields.Many2one('crm.lead', string=_('Order'), required=True, ondelete='cascade')
    service_id = fields.Many2one('tsc.service', string=_('Service'), required=True)
    package_id = fields.Many2one('tsc.package', string=_('Package'), required=True)
    package_level_id = fields.Many2one('tsc.package.level', string=_('Level'))
    quantity = fields.Integer(default=1, required=True)
    unit_price = fields.Float(string=_('Unit Price'))
    discount_amount = fields.Float(string=_('Discount'))
    total_price = fields.Float(string=_('Total'), compute='_compute_total', store=True)
    state = fields.Selection([
        ('draft', _('Draft')),
        ('confirmed', _('Confirmed')),
        ('delivered', _('Delivered')),
    ], default='draft', string=_('Status'))

    @api.depends('quantity', 'unit_price', 'discount_amount')
    def _compute_total(self):
        for line in self:
            line.total_price = (line.quantity * line.unit_price) - line.discount_amount
