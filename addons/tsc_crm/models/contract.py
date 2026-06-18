from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscContract(models.Model):
    _name = 'tsc.contract'
    _description = _('TSC Contract')
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(string=_('Contract Number'), readonly=True, copy=False, default='New')
    lead_id = fields.Many2one('crm.lead', string=_('Order'), required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string=_('Customer'), required=True)
    contract_date = fields.Date(string=_('Contract Date'), default=fields.Date.context_today)
    start_date = fields.Date(string=_('Start Date'))
    end_date = fields.Date(string=_('End Date'))
    state = fields.Selection([
        ('draft', _('Draft')),
        ('pending_sign', _('Pending Signing')),
        ('signed', _('Signed')),
        ('active', _('Active')),
        ('expired', _('Expired')),
        ('cancelled', _('Cancelled')),
    ], string=_('Status'), default='draft', tracking=True)
    signed_file = fields.Binary(string=_('Signed Document'))
    signed_filename = fields.Char(string=_('Signed Filename'))
    scan_file = fields.Binary(string=_('Scanned Contract'))
    scan_filename = fields.Char(string=_('Scan Filename'))
    voffice_doc_id = fields.Char(string=_('VOffice Document ID'))
    voffice_status = fields.Selection([
        ('none', _('Not Sent')),
        ('pending', _('Pending')),
        ('signed', _('Signed')),
        ('rejected', _('Rejected')),
    ], string=_('VOffice Status'), default='none')
    notes = fields.Text(string=_('Notes'))
    amount_total = fields.Float(string=_('Total Amount'), compute='_compute_amount_total', store=True)
    currency_id = fields.Many2one('res.currency', string=_('Currency'), default=lambda self: self.env.company.currency_id)
    sign_ids = fields.One2many('tsc.sign', 'contract_id', string=_('Signing Records'))

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', _('Contract number must be unique!')),
    ]

    @api.depends('lead_id.tsc_order_total')
    def _compute_amount_total(self):
        for contract in self:
            contract.amount_total = contract.lead_id.tsc_order_total if contract.lead_id else 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tsc.contract') or 'New'
        return super().create(vals_list)

    def action_submit(self):
        self.ensure_one()
        if self.state != 'draft':
            raise ValidationError(_('Only draft contracts can be submitted'))
        self.write({'state': 'pending_sign'})
        self.message_post(body=_('Contract submitted for signing'))

    def action_sign(self):
        self.ensure_one()
        if self.state != 'pending_sign':
            raise ValidationError(_('Contract must be pending signing'))
        self.write({'state': 'signed'})
        self.message_post(body=_('Contract signed'))

    def action_activate(self):
        self.ensure_one()
        if self.state != 'signed':
            raise ValidationError(_('Contract must be signed to activate'))
        self.write({'state': 'active', 'start_date': fields.Date.context_today(self)})
        self.message_post(body=_('Contract activated'))

    def action_expire(self):
        self.ensure_one()
        self.write({'state': 'expired'})
        self.message_post(body=_('Contract expired'))

    def action_cancel(self):
        self.ensure_one()
        if self.state in ('expired',):
            raise ValidationError(_('Expired contracts cannot be cancelled'))
        self.write({'state': 'cancelled'})
        self.message_post(body=_('Contract cancelled'))

    def action_reset_to_draft(self):
        self.ensure_one()
        if self.state not in ('pending_sign', 'cancelled'):
            raise ValidationError(_('Only pending or cancelled contracts can be reset to draft'))
        self.write({'state': 'draft'})
        self.message_post(body=_('Contract reset to draft'))

    def action_view_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Order'),
            'res_model': 'crm.lead',
            'res_id': self.lead_id.id,
            'view_mode': 'form',
        }
