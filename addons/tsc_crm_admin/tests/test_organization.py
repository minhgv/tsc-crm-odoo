from odoo.tests.common import TransactionCase


class TestTscOrganization(TransactionCase):

    def test_org_creation(self):
        org = self.env['tsc.organization'].create({
            'name': 'TSC Headquarter',
            'code': 'TSC-HQ',
            'org_type': 'headquarters',
            'division': 'business',
        })
        self.assertEqual(org.org_type, 'headquarters')
        self.assertTrue(org.active)

    def test_org_hierarchy(self):
        hq = self.env['tsc.organization'].create({
            'name': 'TSC',
            'code': 'TSC',
            'org_type': 'headquarters',
            'division': 'business',
        })
        province = self.env['tsc.organization'].create({
            'name': 'Vientiane',
            'code': 'TSC-VT',
            'org_type': 'province',
            'division': 'business',
            'parent_id': hq.id,
        })
        district = self.env['tsc.organization'].create({
            'name': 'Saysettha',
            'code': 'TSC-VT-SS',
            'org_type': 'district',
            'division': 'business',
            'parent_id': province.id,
        })
        village = self.env['tsc.organization'].create({
            'name': 'Nongbone',
            'code': 'TSC-VT-SS-NB',
            'org_type': 'village',
            'division': 'business',
            'parent_id': district.id,
        })
        self.assertEqual(province.parent_id, hq)
        self.assertIn(province, hq.child_ids)
        self.assertEqual(village.org_type, 'village')

    def test_org_divisions(self):
        for div in ['business', 'technical', 'cc']:
            org = self.env['tsc.organization'].create({
                'name': f'Org {div}',
                'code': f'ORG-{div}',
                'org_type': 'province',
                'division': div,
            })
            self.assertEqual(org.division, div)

    def test_org_name_get(self):
        hq = self.env['tsc.organization'].create({
            'name': 'TSC',
            'code': 'TSC',
            'org_type': 'headquarters',
            'division': 'business',
        })
        province = self.env['tsc.organization'].create({
            'name': 'Vientiane',
            'code': 'VT',
            'org_type': 'province',
            'division': 'business',
            'parent_id': hq.id,
        })
        self.assertEqual(province.name_get()[0][1], 'TSC / Vientiane')
