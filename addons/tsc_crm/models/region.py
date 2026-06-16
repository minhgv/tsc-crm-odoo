from odoo import _, fields, models


class TscRegion(models.Model):
    _name = 'tsc.region'
    _description = _('Region')
    _order = 'sequence, name, id'
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, unique=True)
    sequence = fields.Integer(default=10)
    parent_id = fields.Many2one('tsc.region', string=_('Parent Region'))
    child_ids = fields.One2many('tsc.region', 'parent_id', string=_('Child Regions'))
    manager_id = fields.Many2one('hr.employee', string=_('Region Manager'))
    active = fields.Boolean(default=True)

    def name_get(self):
        result = []
        for region in self:
            name = region.name
            if region.parent_id:
                name = f'{region.parent_id.name} / {name}'
            result.append((region.id, name))
        return result
