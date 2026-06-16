from odoo import _, api, fields, models


class TscCombo(models.Model):
    _name = 'tsc.combo'
    _description = _('Combo')
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    description = fields.Html(translate=True)
    line_ids = fields.One2many('tsc.combo.line', 'combo_id', string=_('Lines'))
    total_price = fields.Float(string=_('Total Price'), compute='_compute_total_price', store=True)
    active = fields.Boolean(default=True)

    @api.depends('line_ids.price')
    def _compute_total_price(self):
        for combo in self:
            combo.total_price = sum(combo.line_ids.mapped('price'))


class TscComboLine(models.Model):
    _name = 'tsc.combo.line'
    _description = _('Combo Line')

    combo_id = fields.Many2one('tsc.combo', string=_('Combo'), required=True, ondelete='cascade')
    service_id = fields.Many2one('tsc.service', string=_('Service'), required=True)
    package_id = fields.Many2one('tsc.package', string=_('Package'), required=True)
    quantity = fields.Integer(default=1)
    price = fields.Float(string=_('Price'))
