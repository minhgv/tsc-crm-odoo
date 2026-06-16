from odoo.tests.common import TransactionCase


class TestTscAgency(TransactionCase):

    def test_agency_creation(self):
        agency = self.env['tsc.agency'].create({
            'name': 'Agency Vientiane',
            'code': 'AG-VT',
            'contact_name': 'Somchai',
            'phone': '2055123456',
            'email': 'somchai@agency.la',
            'revenue_tier': 'tier1',
        })
        self.assertEqual(agency.name, 'Agency Vientiane')
        self.assertEqual(agency.code, 'AG-VT')
        self.assertEqual(agency.revenue_tier, 'tier1')

    def test_agency_unique_code(self):
        a1 = self.env['tsc.agency'].create({
            'name': 'Agency 1',
            'code': 'AG-001',
        })
        self.assertTrue(a1)
        a2 = self.env['tsc.agency'].search([('code', '=', 'AG-001')])
        self.assertEqual(len(a2), 1)

    def test_agency_revenue_tiers(self):
        for tier in ['tier1', 'tier2', 'tier3']:
            agency = self.env['tsc.agency'].create({
                'name': f'Agency {tier}',
                'code': f'AG-{tier}',
                'revenue_tier': tier,
            })
            self.assertEqual(agency.revenue_tier, tier)
