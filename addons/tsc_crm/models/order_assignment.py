from odoo import _, api, fields, models


class TscOrderAssignment(models.Model):
    _name = 'tsc.order.assignment'
    _description = _('Order Assignment Log')
    _order = 'create_date desc'
    _rec_name = 'lead_id'

    lead_id = fields.Many2one('crm.lead', string=_('Order'), required=True, ondelete='cascade')
    assigned_from = fields.Many2one('hr.employee', string=_('Assigned From'))
    assigned_to = fields.Many2one('hr.employee', string=_('Assigned To'), required=True)
    assigned_by = fields.Many2one('res.users', string=_('Assigned By'), default=lambda self: self.env.user)
    reason = fields.Selection([
        ('auto', 'Auto Assignment'),
        ('manual', 'Manual Assignment'),
        ('reassign', 'Reassignment'),
        ('override', 'Admin Override'),
    ], string=_('Reason'), required=True)
    notes = fields.Text(string=_('Notes'))
