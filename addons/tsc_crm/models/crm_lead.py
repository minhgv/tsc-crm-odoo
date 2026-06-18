from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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
    tsc_assignment_ids = fields.One2many('tsc.order.assignment', 'lead_id', string=_('Assignment Log'))
    tsc_assigned_to = fields.Many2one('hr.employee', string=_('Assigned To'))
    tsc_technical_task_ids = fields.One2many('tsc.technical.task', 'lead_id', string=_('Technical Tasks'))
    tsc_stage_key = fields.Selection([
        ('created', _('Created')),
        ('assigned', _('Assigned')),
        ('accepted', _('Accepted')),
        ('surveying', _('Surveying')),
        ('confirm', _('Confirm')),
        ('contract', _('Contract')),
        ('paid', _('Paid')),
    ], compute='_compute_stage_key', store=True, string=_('Workflow Stage'))

    @api.depends('stage_id')
    def _compute_stage_key(self):
        stage_map = {
            'Created': 'created',
            'Assigned': 'assigned',
            'Accepted': 'accepted',
            'Survey / Consultation': 'surveying',
            'Confirm': 'confirm',
            'Contract Signing': 'contract',
            'Payment': 'paid',
            'Completed': 'paid',
        }
        for lead in self:
            lead.tsc_stage_key = stage_map.get(lead.stage_id.name, 'created')

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

    def action_assign_order(self, employee):
        self.ensure_one()
        if not employee:
            raise ValidationError(_('Please select an employee'))
        old_employee = self.tsc_assigned_to
        self.write({'tsc_assigned_to': employee.id})
        stage_assigned = self.env.ref('tsc_crm.tsc_stage_assigned', raise_if_not_found=False)
        if stage_assigned:
            self.write({'stage_id': stage_assigned.id})
        self.env['tsc.order.assignment'].create({
            'lead_id': self.id,
            'assigned_from': old_employee.id if old_employee else False,
            'assigned_to': employee.id,
            'reason': 'auto' if not old_employee else 'reassign',
        })
        self.message_post(body=_('Order assigned to %s') % employee.name)

    def action_confirm_order(self):
        self.ensure_one()
        stage_confirm = self.env.ref('tsc_crm.tsc_stage_confirm', raise_if_not_found=False)
        if stage_confirm:
            self.write({'stage_id': stage_confirm.id})
        self.message_post(body=_('Order confirmed'))

    def action_accept_order(self):
        self.ensure_one()
        stage_accepted = self.env.ref('tsc_crm.tsc_stage_accepted', raise_if_not_found=False)
        if stage_accepted:
            self.write({'stage_id': stage_accepted.id})
        self.message_post(body=_('Order accepted by %s') % self.env.user.name)

    def action_survey_order(self):
        self.ensure_one()
        stage_survey = self.env.ref('tsc_crm.tsc_stage_survey', raise_if_not_found=False)
        if stage_survey:
            self.write({'stage_id': stage_survey.id})
        self.message_post(body=_('Order moved to survey phase'))

    @api.model
    def _cron_check_sla(self):
        """Cron job to check SLA violations and send notifications"""
        now = fields.Datetime.now()
        overdue_leads = self.search([
            ('tsc_sla_deadline', '<', now),
            ('tsc_is_overdue', '=', True),
            ('stage_id.is_won', '=', False),
        ])
        for lead in overdue_leads:
            lead._handle_sla_violation()

    def _handle_sla_violation(self):
        """Handle SLA violation for a lead"""
        self.ensure_one()
        # Find applicable SLA config
        sla_configs = self.env['tsc.sla.config'].search([
            ('active', '=', True),
        ])
        sla_config = sla_configs.filtered(
            lambda c: c.stage_key == self.tsc_stage_key or c.stage == self.tsc_stage_key
        )[:1]

        if not sla_config:
            return

        # Create violation record
        self.env['tsc.sla.violation'].create({
            'lead_id': self.id,
            'sla_config_id': sla_config.id,
            'stage_key': self.tsc_stage_key,
            'violation_date': fields.Datetime.now(),
        })

        # Execute auto action
        auto_action = getattr(sla_config, 'auto_action', 'notify')
        if auto_action == 'auto_assign_admin':
            admin_employee = self.env['hr.employee'].search([
                ('tsc_role', '=', 'manager'),
            ], limit=1)
            if admin_employee:
                self.action_assign_order(admin_employee)
        elif auto_action == 'notify':
            template = self.env.ref('tsc_crm.mail_template_sla_violated', raise_if_not_found=False)
            if template:
                template.send_mail(self.id, force_send=True)

        self.message_post(body=_('SLA violated - auto action triggered'))
