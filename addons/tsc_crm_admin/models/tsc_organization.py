from odoo import _, fields, models


class TscOrganization(models.Model):
    _name = 'tsc.organization'
    _description = _('Organization Unit')
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, unique=True)
    sequence = fields.Integer(default=10)
    org_type = fields.Selection([
        ('headquarters', _('TSC (Headquarters)')),
        ('province', _('Province')),
        ('district', _('District')),
        ('village', _('Village')),
    ], required=True, string=_('Organization Type'))
    parent_id = fields.Many2one('tsc.organization', string=_('Parent'))
    child_ids = fields.One2many('tsc.organization', 'parent_id', string=_('Children'))
    division = fields.Selection([
        ('business', _('Business')),
        ('technical', _('Technical')),
        ('cc', _('Customer Care')),
    ], required=True, string=_('Division'))
    manager_id = fields.Many2one('hr.employee', string=_('Manager'))
    active = fields.Boolean(default=True)

    def name_get(self):
        result = []
        for org in self:
            name = org.name
            if org.parent_id:
                name = f'{org.parent_id.name} / {name}'
            result.append((org.id, name))
        return result
