from odoo.tests.common import TransactionCase


class TestHrEmployee(TransactionCase):

    def test_employee_role(self):
        employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'tsc_role': 'manager',
            'tsc_group_type': 'business',
        })
        self.assertEqual(employee.tsc_role, 'manager')
        self.assertEqual(employee.tsc_group_type, 'business')

    def test_employee_staff_role(self):
        employee = self.env['hr.employee'].create({
            'name': 'Staff Employee',
            'tsc_role': 'staff',
            'tsc_group_type': 'technical',
        })
        self.assertEqual(employee.tsc_role, 'staff')
        self.assertEqual(employee.tsc_group_type, 'technical')

    def test_employee_max_order_default(self):
        employee = self.env['hr.employee'].create({
            'name': 'Default Employee',
        })
        self.assertEqual(employee.tsc_max_order, 0)
