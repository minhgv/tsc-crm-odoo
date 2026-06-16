from odoo import _, api, fields, models


class TscContract(models.Model):
    _name = 'tsc.contract'
    _description = _('Contract')
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(required=True, readonly=True, default='New')
    lead_id = fields.Many2one('crm.lead', string=_('Order'), required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', related='lead_id.partner_id', string=_('Customer'))
    state = fields.Selection([
        ('draft', _('Draft')),
        ('pending_sign', _('Pending Signature')),
        ('signed', _('Signed')),
        ('scanned', _('Scanned')),
        ('active', _('Active')),
        ('expired', _('Expired')),
        ('terminated', _('Terminated')),
    ], default='draft', tracking=True, required=True)
    contract_date = fields.Date(string=_('Contract Date'))
    effective_date = fields.Date(string=_('Effective Date'))
    expiry_date = fields.Date(string=_('Expiry Date'))
    signed_file = fields.Binary(string=_('Signed File'))
    voffice_doc_id = fields.Char(string=_('Voffice Document ID'))
    notes = fields.Text()
    invoice_id = fields.Many2one('tsc.invoice', string=_('Invoice'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('tsc.contract') or 'New'
        return super().create(vals_list)

    def action_submit(self):
        self.write({'state': 'pending_sign'})

    def action_sign(self):
        self.write({'state': 'signed', 'contract_date': fields.Date.today()})

    def action_scan(self):
        self.write({'state': 'scanned'})

    def action_activate(self):
        self.write({'state': 'active'})

    def action_terminate(self):
        self.write({'state': 'terminated'})
