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
