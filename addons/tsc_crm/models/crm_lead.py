from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    tsc_order_id = fields.Char(string=_('Order Reference'), readonly=True)
    tsc_service_type = fields.Selection([
        ('direct', _('Direct Sale')),
        ('project', _('Project')),
    ], string=_('Service Type'))
    tsc_customer_type = fields.Selection([
        ('individual', _('Individual')),
        ('business', _('Business')),
        ('government', _('Government')),
    ], string=_('Customer Type'))
    tsc_source = fields.Selection([
        ('miniapp', _('Miniapp')),
        ('cms', _('CMS CRM')),
    ], string=_('Source'))
    tsc_region_id = fields.Many2one('tsc.region', string=_('Region'))
    tsc_confirm_deadline = fields.Datetime(string=_('Confirmation Deadline'))
    tsc_sla_deadline = fields.Datetime(string=_('SLA Deadline'))
    tsc_is_overdue = fields.Boolean(string=_('Overdue'), compute='_compute_tsc_overdue', store=True)
    tsc_order_line_ids = fields.One2many('tsc.order.line', 'lead_id', string=_('Order Lines'))
    tsc_order_total = fields.Float(string=_('Order Total'), compute='_compute_order_total', store=True)

    @api.depends('tsc_sla_deadline')
    def _compute_tsc_overdue(self):
        now = fields.Datetime.now()
        for lead in self:
            lead.tsc_is_overdue = (
                lead.tsc_sla_deadline
                and lead.tsc_sla_deadline < now
                and lead.stage_id and not lead.stage_id.is_won
            )

    @api.depends('tsc_order_line_ids.total_price')
    def _compute_order_total(self):
        for lead in self:
            lead.tsc_order_total = sum(lead.tsc_order_line_ids.mapped('total_price'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('tsc_order_id', 'New') == 'New':
                vals['tsc_order_id'] = self.env['ir.sequence'].next_by_code('tsc.order') or 'New'
        return super().create(vals_list)
