from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTscRolePermission(TransactionCase):

    def test_role_creation(self):
        role = self.env['tsc.role'].create({
            'name': 'Sales Manager',
            'code': 'SALES_MGR',
        })
        self.assertEqual(role.code, 'SALES_MGR')
        self.assertTrue(role.active)

    def test_permission_creation(self):
        model = self.env['ir.model'].search([('model', '=', 'crm.lead')], limit=1)
        perm = self.env['tsc.permission'].create({
            'name': 'Create Lead',
            'code': 'LEAD_CREATE',
            'model_id': model.id,
            'operation': 'create',
        })
        self.assertEqual(perm.operation, 'create')

    def test_role_permission_mapping(self):
        role = self.env['tsc.role'].create({
            'name': 'Staff',
            'code': 'STAFF',
        })
        model = self.env['ir.model'].search([('model', '=', 'crm.lead')], limit=1)
        perm = self.env['tsc.permission'].create({
            'name': 'Read Lead',
            'code': 'LEAD_READ',
            'model_id': model.id,
            'operation': 'read',
        })
        self.env['tsc.role.permission'].create({
            'role_id': role.id,
            'permission_id': perm.id,
        })
        self.assertIn(perm, role.permission_ids.mapped('permission_id'))

    def test_role_permission_unique(self):
        role = self.env['tsc.role'].create({
            'name': 'Admin',
            'code': 'ADMIN',
        })
        model = self.env['ir.model'].search([('model', '=', 'crm.lead')], limit=1)
        perm = self.env['tsc.permission'].create({
            'name': 'Delete Lead',
            'code': 'LEAD_DELETE',
            'model_id': model.id,
            'operation': 'delete',
        })
        self.env['tsc.role.permission'].create({
            'role_id': role.id,
            'permission_id': perm.id,
        })
        with self.assertRaises(Exception):
            self.env['tsc.role.permission'].create({
                'role_id': role.id,
                'permission_id': perm.id,
            })
