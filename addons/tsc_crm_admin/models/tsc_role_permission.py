from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TscRole(models.Model):
    _name = 'tsc.role'
    _description = _('Role')
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, unique=True)
    permission_ids = fields.One2many('tsc.role.permission', 'role_id', string=_('Permissions'))
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)


class TscPermission(models.Model):
    _name = 'tsc.permission'
    _description = _('Permission')
    _rec_name = 'name'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, unique=True)
    model_id = fields.Many2one('ir.model', string=_('Model'))
    operation = fields.Selection([
        ('create', _('Create')),
        ('read', _('Read')),
        ('update', _('Update')),
        ('delete', _('Delete')),
    ], required=True, string=_('Operation'))
    description = fields.Text(translate=True)


class TscRolePermission(models.Model):
    _name = 'tsc.role.permission'
    _description = _('Role-Permission Mapping')
    _rec_name = 'role_id'

    role_id = fields.Many2one('tsc.role', string=_('Role'), required=True, ondelete='cascade')
    permission_id = fields.Many2one('tsc.permission', string=_('Permission'), required=True)

    _sql_constraints = [
        ('unique_role_permission', 'UNIQUE(role_id, permission_id)', 'Permission already assigned to this role!'),
    ]
