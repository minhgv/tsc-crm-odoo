from datetime import date
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestTscDiscountPolicy(TransactionCase):

    def setUp(self):
        super().setUp()
        self.agency = self.env['tsc.agency'].create({
            'name': 'Agency Test',
            'code': 'AG-T',
        })

    def test_policy_all_agents(self):
        policy = self.env['tsc.discount.policy'].create({
            'name': 'Revenue 5%',
            'discount_type': 'revenue',
            'discount_mode': 'percentage',
            'value': 5.0,
            'scope': 'all_agents',
        })
        self.assertEqual(policy.scope, 'all_agents')
        self.assertTrue(policy.active)

    def test_policy_specific_agent(self):
        policy = self.env['tsc.discount.policy'].create({
            'name': 'Agent 10K',
            'discount_type': 'order_count',
            'discount_mode': 'fixed',
            'value': 10000,
            'scope': 'specific_agent',
            'agency_ids': [(4, self.agency.id)],
        })
        self.assertIn(self.agency, policy.agency_ids)

    def test_policy_specific_agent_requires_agency(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.discount.policy'].create({
                'name': 'No Agency',
                'discount_type': 'revenue',
                'discount_mode': 'percentage',
                'value': 5.0,
                'scope': 'specific_agent',
            })

    def test_policy_date_range(self):
        policy = self.env['tsc.discount.policy'].create({
            'name': 'Dated Policy',
            'discount_type': 'revenue',
            'discount_mode': 'percentage',
            'value': 3.0,
            'scope': 'all_agents',
            'date_from': date(2024, 1, 1),
            'date_to': date(2024, 12, 31),
        })
        self.assertEqual(policy.date_from, date(2024, 1, 1))

    def test_policy_bad_dates(self):
        with self.assertRaises(ValidationError):
            self.env['tsc.discount.policy'].create({
                'name': 'Bad Dates',
                'discount_type': 'revenue',
                'discount_mode': 'fixed',
                'value': 1000,
                'scope': 'all_agents',
                'date_from': date(2024, 12, 31),
                'date_to': date(2024, 1, 1),
            })
