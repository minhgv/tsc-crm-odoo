from odoo import _, api, fields, models


class TscSlaViolation(models.Model):
    _name = 'tsc.sla.violation'
    _description = _('TSC SLA Violation')
    _order = 'violation_date desc'
    _rec_name = 'name'

    name = fields.Char(string=_('Description'), compute='_compute_name', store=True)
    lead_id = fields.Many2one('crm.lead', string=_('Order'), required=True, ondelete='cascade')
    sla_config_id = fields.Many2one('tsc.sla.config', string=_('SLA Config'), required=True, ondelete='cascade')
    stage_key = fields.Char(string=_('Stage Key'))
    violation_date = fields.Datetime(string=_('Violation Date'), default=fields.Datetime.now)
    action_taken = fields.Text(string=_('Action Taken'))
    resolved = fields.Boolean(string=_('Resolved'), default=False)
    resolved_date = fields.Datetime(string=_('Resolved Date'))
    notes = fields.Text(string=_('Notes'))

    @api.depends('lead_id', 'sla_config_id')
    def _compute_name(self):
        for violation in self:
            if violation.lead_id and violation.sla_config_id:
                violation.name = f"{violation.lead_id.name or violation.lead_id.tsc_order_id} - {violation.sla_config_id.name} SLA Violation"
            else:
                violation.name = _('New SLA Violation')

    def action_resolve(self):
        for violation in self:
            violation.write({
                'resolved': True,
                'resolved_date': fields.Datetime.now(),
            })

    def action_reopen(self):
        for violation in self:
            violation.write({
                'resolved': False,
                'resolved_date': False,
            })
