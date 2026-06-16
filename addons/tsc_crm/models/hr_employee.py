from odoo import _, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    tsc_role = fields.Selection([
        ('manager', _('Manager')),
        ('staff', _('Staff')),
    ], string=_('TSC Role'))
    tsc_group_type = fields.Selection([
        ('business', _('Business')),
        ('technical', _('Technical')),
    ], string=_('Group Type'))
    tsc_lao_id = fields.Char(string=_('LaoID'))
    tsc_max_order = fields.Integer(string=_('Max Concurrent Orders'), default=0)
    tsc_current_order = fields.Integer(string=_('Current Orders'), compute='_compute_current_order')

    def _compute_current_order(self):
        for employee in self:
            employee.tsc_current_order = self.env['crm.lead'].search_count([
                ('user_id', '=', employee.user_id.id),
                ('stage_id.is_won', '=', False),
            ])
