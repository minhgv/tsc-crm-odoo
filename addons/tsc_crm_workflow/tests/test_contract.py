from odoo.tests.common import TransactionCase


class TestTscContract(TransactionCase):

    def setUp(self):
        super().setUp()
        self.lead = self.env['crm.lead'].create({
            'name': 'Test Lead',
            'tsc_order_id': 'ORD-TEST-001',
        })

    def test_contract_creation(self):
        contract = self.env['tsc.contract'].create({
            'lead_id': self.lead.id,
        })
        self.assertEqual(contract.state, 'draft')
        self.assertTrue(contract.name)
        self.assertNotEqual(contract.name, 'New')

    def test_contract_submit(self):
        contract = self.env['tsc.contract'].create({
            'lead_id': self.lead.id,
        })
        contract.action_submit()
        self.assertEqual(contract.state, 'pending_sign')

    def test_contract_sign(self):
        contract = self.env['tsc.contract'].create({
            'lead_id': self.lead.id,
        })
        contract.action_submit()
        contract.action_sign()
        self.assertEqual(contract.state, 'signed')
        self.assertEqual(contract.contract_date, __import__('odoo').fields.Date.today())

    def test_contract_full_flow(self):
        contract = self.env['tsc.contract'].create({
            'lead_id': self.lead.id,
        })
        self.assertEqual(contract.state, 'draft')
        contract.action_submit()
        self.assertEqual(contract.state, 'pending_sign')
        contract.action_sign()
        self.assertEqual(contract.state, 'signed')
        contract.action_scan()
        self.assertEqual(contract.state, 'scanned')
        contract.action_activate()
        self.assertEqual(contract.state, 'active')

    def test_contract_terminate(self):
        contract = self.env['tsc.contract'].create({
            'lead_id': self.lead.id,
        })
        contract.action_submit()
        contract.action_sign()
        contract.action_terminate()
        self.assertEqual(contract.state, 'terminated')

    def test_contract_partner_related(self):
        partner = self.env['res.partner'].create({'name': 'Test Customer'})
        lead = self.env['crm.lead'].create({
            'name': 'Lead with Partner',
            'partner_id': partner.id,
        })
        contract = self.env['tsc.contract'].create({
            'lead_id': lead.id,
        })
        self.assertEqual(contract.partner_id, partner)
