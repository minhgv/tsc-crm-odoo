from odoo import _, api, fields, models


class TscSign(models.Model):
    _name = 'tsc.sign'
    _description = _('TSC Signing Record')
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    name = fields.Char(string=_('Signing Record'), compute='_compute_name', store=True)
    contract_id = fields.Many2one('tsc.contract', string=_('Contract'), required=True, ondelete='cascade')
    lead_id = fields.Many2one('crm.lead', string=_('Order'), related='contract_id.lead_id', store=True)
    partner_id = fields.Many2one('res.partner', string=_('Customer'), related='contract_id.partner_id', store=True)
    doc_type = fields.Selection([
        ('contract', _('Contract')),
        ('appendix', _('Appendix')),
        ('other', _('Other')),
    ], string=_('Document Type'), default='contract')
    voffice_doc_id = fields.Char(string=_('VOffice Document ID'))
    voffice_trans_code = fields.Char(string=_('VOffice Transaction Code'))
    voffice_status = fields.Selection([
        ('none', _('Not Sent')),
        ('pending', _('Pending Signing')),
        ('signed', _('Signed')),
        ('published', _('Published')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled')),
    ], string=_('VOffice Status'), default='none', tracking=True)
    signed_file = fields.Binary(string=_('Signed File'))
    signed_filename = fields.Char(string=_('Signed Filename'))
    sign_date = fields.Datetime(string=_('Sign Date'))
    notes = fields.Text(string=_('Notes'))
    error_message = fields.Text(string=_('Error Message'))

    @api.depends('contract_id.name', 'doc_type')
    def _compute_name(self):
        for sign in self:
            if sign.contract_id:
                doc_type_label = dict(sign._fields['doc_type'].selection).get(sign.doc_type, sign.doc_type)
                sign.name = f"{sign.contract_id.name} - {doc_type_label}"
            else:
                sign.name = _('New Signing')

    def action_send_to_voffice(self):
        self.ensure_one()
        # Stub implementation - will be replaced with actual VOffice API call
        self.write({'voffice_status': 'pending'})
        self.message_post(body=_('Sent to VOffice for signing'))

    def action_check_status(self):
        self.ensure_one()
        # Stub implementation - will be replaced with actual VOffice API call
        pass

    def action_mark_signed(self):
        self.ensure_one()
        self.write({
            'voffice_status': 'signed',
            'sign_date': fields.Datetime.now(),
        })
        self.message_post(body=_('Document signed'))

    def action_mark_published(self):
        self.ensure_one()
        self.write({'voffice_status': 'published'})
        self.contract_id.action_sign()
        self.message_post(body=_('Document published'))

    def action_mark_rejected(self):
        self.ensure_one()
        self.write({'voffice_status': 'rejected'})
        self.message_post(body=_('Document rejected'))

    def action_cancel(self):
        self.ensure_one()
        self.write({'voffice_status': 'cancelled'})
        self.message_post(body=_('Signing cancelled'))
