from odoo.tests.common import TransactionCase


class TestTscCommissionRule(TransactionCase):

    def test_rule_percentage(self):
        rule = self.env['tsc.commission.rule'].create({
            'name': 'Revenue 5%',
            'commission_type': 'percentage',
            'rate': 5.0,
            'target_group': 'agency',
        })
        self.assertEqual(rule.rate, 5.0)
        self.assertTrue(rule.active)

    def test_rule_fixed(self):
        rule = self.env['tsc.commission.rule'].create({
            'name': 'Fixed 100K',
            'commission_type': 'fixed',
            'rate': 100000.0,
            'target_group': 'staff',
        })
        self.assertEqual(rule.commission_type, 'fixed')

    def test_rule_target_groups(self):
        for group in ['am', 'agency', 'staff', 'management']:
            rule = self.env['tsc.commission.rule'].create({
                'name': f'Rule {group}',
                'commission_type': 'fixed',
                'rate': 1000,
                'target_group': group,
            })
            self.assertEqual(rule.target_group, group)


class TestTscCommission(TransactionCase):

    def setUp(self):
        super().setUp()
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
            'tsc_order_id': 'ORD-COM-001',
        })
        self.invoice = self.env['tsc.invoice'].create({
            'lead_id': self.lead.id,
            'subtotal': 1000000.0,
        })

    def test_commission_creation(self):
        commission = self.env['tsc.commission'].create({
            'invoice_id': self.invoice.id,
            'amount': 50000.0,
        })
        self.assertEqual(commission.state, 'draft')
        self.assertTrue(commission.name.startswith('COM'))

    def test_commission_approve_and_pay(self):
        commission = self.env['tsc.commission'].create({
            'invoice_id': self.invoice.id,
            'amount': 50000.0,
        })
        commission.action_approve()
        self.assertEqual(commission.state, 'approved')
        commission.action_pay()
        self.assertEqual(commission.state, 'paid')

    def test_compute_commission_percentage(self):
        self.env['tsc.commission.rule'].create({
            'name': 'Test Rule',
            'commission_type': 'percentage',
            'rate': 5.0,
            'target_group': 'agency',
        })
        self.invoice.write({'state': 'paid'})
        self.env['tsc.commission'].compute_commission(self.invoice)
        commissions = self.env['tsc.commission'].search([('invoice_id', '=', self.invoice.id)])
        self.assertEqual(len(commissions), 1)
        self.assertEqual(commissions.amount, 50000.0)

    def test_compute_commission_fixed(self):
        self.env['tsc.commission.rule'].create({
            'name': 'Fixed Rule',
            'commission_type': 'fixed',
            'rate': 100000.0,
            'target_group': 'staff',
        })
        self.invoice.write({'state': 'paid'})
        self.env['tsc.commission'].compute_commission(self.invoice)
        commissions = self.env['tsc.commission'].search([('invoice_id', '=', self.invoice.id)])
        self.assertEqual(len(commissions), 1)
        self.assertEqual(commissions.amount, 100000.0)

    def test_compute_commission_not_paid(self):
        self.env['tsc.commission.rule'].create({
            'name': 'Draft Rule',
            'commission_type': 'fixed',
            'rate': 100000.0,
            'target_group': 'staff',
        })
        self.env['tsc.commission'].compute_commission(self.invoice)
        commissions = self.env['tsc.commission'].search([('invoice_id', '=', self.invoice.id)])
        self.assertEqual(len(commissions), 0)
