from odoo import _, api, fields, models


class TscCommission(models.Model):
    _name = 'tsc.commission'
    _description = _('Commission')
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(required=True, readonly=True, default='New')
    employee_id = fields.Many2one('hr.employee', string=_('Employee'))
    agency_id = fields.Many2one('tsc.agency', string=_('Agency'))
    lead_id = fields.Many2one('crm.lead', string=_('Order'))
    invoice_id = fields.Many2one('tsc.invoice', string=_('Invoice'))
    rule_id = fields.Many2one('tsc.commission.rule', string=_('Rule'))
    amount = fields.Float(required=True)
    state = fields.Selection([
        ('draft', _('Draft')),
        ('approved', _('Approved')),
        ('paid', _('Paid')),
    ], default='draft', tracking=True)
    commission_date = fields.Date(string=_('Commission Date'), default=fields.Date.today)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tsc.commission') or 'New'
        return super().create(vals_list)

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_pay(self):
        self.write({'state': 'paid'})

    @api.model
    def compute_commission(self, invoice):
        if invoice.state != 'paid':
            return
        rules = self.env['tsc.commission.rule'].search([
            ('active', '=', True),
        ])
        for rule in rules:
            if rule.commission_type == 'percentage':
                amount = invoice.subtotal * rule.rate / 100
            else:
                amount = rule.rate
            if amount <= 0:
                continue
            self.create({
                'invoice_id': invoice.id,
                'lead_id': invoice.lead_id.id if invoice.lead_id else False,
                'rule_id': rule.id,
                'amount': amount,
                'agency_id': rule.agency_id.id if rule.agency_id else False,
            })
