from odoo.tests.common import TransactionCase


class TestTscRegion(TransactionCase):

    def setUp(self):
        super().setUp()
        self.region = self.env['tsc.region'].create({
            'name': 'Vientiane Capital',
            'code': 'VT',
        })

    def test_region_creation(self):
        self.assertEqual(self.region.name, 'Vientiane Capital')
        self.assertEqual(self.region.code, 'VT')
        self.assertTrue(self.region.active)

    def test_region_hierarchy(self):
        child = self.env['tsc.region'].create({
            'name': 'Saysettha',
            'code': 'VT-SS',
            'parent_id': self.region.id,
        })
        self.assertEqual(child.parent_id, self.region)
        self.assertIn(child, self.region.child_ids)

    def test_region_name_get(self):
        child = self.env['tsc.region'].create({
            'name': 'Saysettha',
            'code': 'VT-SS',
            'parent_id': self.region.id,
        })
        self.assertEqual(child.name_get()[0][1], 'Vientiane Capital / Saysettha')
