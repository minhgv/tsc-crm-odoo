import logging
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


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
    signed_file_name = fields.Char(string=_('Signed File Name'))
    voffice_doc_id = fields.Char(string=_('Voffice Document ID'), readonly=True)
    voffice_config_id = fields.Many2one('tsc.voffice.config', string=_('VOffice Config'))
    voffice_sign_ids = fields.One2many('tsc.voffice.sign', 'contract_id', string=_('Signing Records'))
    voffice_status = fields.Selection([
        ('none', _('Not Sent')),
        ('sent', _('Sent')),
        ('signing', _('Signing')),
        ('signed', _('Signed')),
        ('rejected', _('Rejected')),
    ], compute='_compute_voffice_status', store=True, string=_('VOffice Status'))
    notes = fields.Text()
    invoice_id = fields.Many2one('tsc.invoice', string=_('Invoice'))

    @api.depends('voffice_sign_ids.status')
    def _compute_voffice_status(self):
        for rec in self:
            latest = rec.voffice_sign_ids[:1]
            if not latest:
                rec.voffice_status = 'none'
            elif latest.status in ('sent', 'uploaded'):
                rec.voffice_status = 'sent'
            elif latest.status in ('signing',):
                rec.voffice_status = 'signing'
            elif latest.status == 'published':
                rec.voffice_status = 'signed'
            elif latest.status in ('rejected', 'cancelled'):
                rec.voffice_status = 'rejected'
            else:
                rec.voffice_status = 'none'

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

    def action_send_to_voffice(self):
        self.ensure_one()
        if not self.voffice_config_id:
            config = self.env['tsc.voffice.config'].search([('active', '=', True)], limit=1)
            if not config:
                raise UserError(_('No VOffice configuration found. Please configure VOffice first.'))
            self.voffice_config_id = config

        if not self.signed_file:
            raise UserError(_('Please upload the contract file first.'))

        sign = self.env['tsc.voffice.sign'].create({
            'contract_id': self.id,
            'voffice_config_id': self.voffice_config_id.id,
        })

        try:
            sign.action_upload_and_send()
        except Exception as e:
            raise UserError(_('Failed to send to VOffice: %s') % str(e))

        self.write({'state': 'pending_sign'})
        self.message_post(body=_('Contract sent to VOffice for signing.'))
        return True

    def action_check_voffice_status(self):
        for rec in self:
            if rec.voffice_sign_ids:
                rec.voffice_sign_ids[:1].action_check_status()

    def action_download_signed(self):
        self.ensure_one()
        if not self.signed_file:
            raise ValueError(_('No signed file available.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Signed Contract'),
            'res_model': 'tsc.contract',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
