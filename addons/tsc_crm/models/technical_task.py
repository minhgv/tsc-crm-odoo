from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscTechnicalTask(models.Model):
    _name = 'tsc.technical.task'
    _description = _('Technical Task')
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, create_date desc'
    _rec_name = 'name'

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True, translate=True)
    lead_id = fields.Many2one('crm.lead', string=_('Order'), required=True, ondelete='cascade',
                              domain="[('tsc_order_id', '!=', False)]")
    assigned_by = fields.Many2one('hr.employee', string=_('Assigned By'))
    assigned_to = fields.Many2one('hr.employee', string=_('Assigned To'))
    task_type = fields.Selection([
        ('survey', _('Survey')),
        ('implementation', _('Implementation')),
        ('maintenance', _('Maintenance')),
    ], string=_('Task Type'), required=True, default='survey')
    state = fields.Selection([
        ('draft', _('Draft')),
        ('assigned', _('Assigned')),
        ('accepted', _('Accepted')),
        ('in_progress', _('In Progress')),
        ('done', _('Done')),
        ('cancelled', _('Cancelled')),
    ], default='draft', string=_('Status'), tracking=True)
    deadline = fields.Datetime(string=_('Deadline'))
    is_overdue = fields.Boolean(string=_('Overdue'), compute='_compute_is_overdue', store=True)
    notes = fields.Text(string=_('Notes'))

    @api.depends('deadline', 'state')
    def _compute_is_overdue(self):
        now = fields.Datetime.now()
        for task in self:
            task.is_overdue = (
                task.deadline
                and task.deadline < now
                and task.state not in ('done', 'cancelled')
            )

    def action_assign(self):
        for task in self:
            if not task.assigned_to:
                raise ValidationError(_('Please select an assignee'))
            task.write({'state': 'assigned'})
            task.message_post(body=_('Task assigned to %s') % task.assigned_to.name)

    def action_accept(self):
        for task in self:
            task.write({'state': 'accepted'})

    def action_start(self):
        for task in self:
            task.write({'state': 'in_progress'})

    def action_done(self):
        for task in self:
            task.write({'state': 'done'})
            task.message_post(body=_('Task completed'))

    def action_cancel(self):
        for task in self:
            task.write({'state': 'cancelled'})

    def action_reset(self):
        for task in self:
            task.write({'state': 'draft'})
