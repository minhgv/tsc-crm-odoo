from odoo.tests.common import TransactionCase


class TestCrmTeam(TransactionCase):

    def setUp(self):
        super().setUp()
        self.region = self.env['tsc.region'].create({
            'name': 'Vientiane',
            'code': 'VT',
        })

    def test_team_creation_with_region(self):
        team = self.env['crm.team'].create({
            'name': 'Sales Team Vientiane',
            'tsc_region_id': self.region.id,
            'tsc_team_type': 'business',
        })
        self.assertEqual(team.tsc_region_id, self.region)
        self.assertEqual(team.tsc_team_type, 'business')

    def test_team_technical_type(self):
        team = self.env['crm.team'].create({
            'name': 'Technical Team',
            'tsc_team_type': 'technical',
        })
        self.assertEqual(team.tsc_team_type, 'technical')
