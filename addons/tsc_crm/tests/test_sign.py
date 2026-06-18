from odoo.tests.common import TransactionCase


class TestTscSign(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Customer',
        })
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Order',
            'tsc_order_id': 'ORD-TEST-001',
            'partner_id': self.partner.id,
        })
        self.contract = self.env['tsc.contract'].create({
            'lead_id': self.lead.id,
            'partner_id': self.partner.id,
        })
        self.sign = self.env['tsc.sign'].create({
            'contract_id': self.contract.id,
            'doc_type': 'contract',
        })

    def test_sign_creation(self):
        self.assertEqual(self.sign.contract_id, self.contract)
        self.assertEqual(self.sign.voffice_status, 'none')
        self.assertEqual(self.sign.doc_type, 'contract')

    def test_sign_name_computation(self):
        self.assertIn(self.contract.name, self.sign.name)

    def test_sign_workflow(self):
        self.assertEqual(self.sign.voffice_status, 'none')
        self.sign.action_send_to_voffice()
        self.assertEqual(self.sign.voffice_status, 'pending')
        self.sign.action_mark_signed()
        self.assertEqual(self.sign.voffice_status, 'signed')
        self.assertTrue(self.sign.sign_date)
        # Submit contract for signing before publishing
        self.contract.action_submit()
        self.sign.action_mark_published()
        self.assertEqual(self.sign.voffice_status, 'published')
        self.assertEqual(self.contract.state, 'signed')

    def test_sign_reject(self):
        self.sign.action_send_to_voffice()
        self.sign.action_mark_rejected()
        self.assertEqual(self.sign.voffice_status, 'rejected')

    def test_sign_cancel(self):
        self.sign.action_send_to_voffice()
        self.sign.action_cancel()
        self.assertEqual(self.sign.voffice_status, 'cancelled')
