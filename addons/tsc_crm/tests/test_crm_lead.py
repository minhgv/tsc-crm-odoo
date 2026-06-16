from odoo.tests.common import TransactionCase


class TestCrmLeadTsc(TransactionCase):

    def setUp(self):
        super().setUp()
        self.region = self.env['tsc.region'].create({
            'name': 'Vientiane',
            'code': 'VT',
        })

    def test_lead_creation_with_order_id(self):
        lead = self.env['crm.lead'].create({
            'name': 'Test Lead',
            'tsc_service_type': 'direct',
            'tsc_customer_type': 'business',
            'tsc_source': 'cms',
            'tsc_region_id': self.region.id,
        })
        self.assertTrue(lead.tsc_order_id)
        self.assertNotEqual(lead.tsc_order_id, 'New')

    def test_lead_overdue_computation(self):
        lead = self.env['crm.lead'].create({
            'name': 'Test Lead',
            'tsc_sla_deadline': '2020-01-01 00:00:00',
        })
        self.assertTrue(lead.tsc_is_overdue)
