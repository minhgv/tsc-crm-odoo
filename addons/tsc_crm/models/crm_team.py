from odoo import _, fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    tsc_region_id = fields.Many2one('tsc.region', string=_('Region'))
    tsc_team_type = fields.Selection([
        ('business', _('Business')),
        ('technical', _('Technical')),
    ], string=_('Team Type'))
    tsc_manager_id = fields.Many2one('hr.employee', string=_('Team Manager'))
