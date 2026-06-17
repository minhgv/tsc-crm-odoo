from odoo.tests.common import TransactionCase


class TestResPartnerTsc(TransactionCase):

    def test_partner_customer_code(self):
        partner = self.env['res.partner'].create({
            'name': 'Test Customer',
            'tsc_customer_code': 'CUS-001',
            'tsc_customer_type': 'individual',
        })
        self.assertEqual(partner.tsc_customer_code, 'CUS-001')
        self.assertEqual(partner.tsc_customer_type, 'individual')

    def test_partner_customer_type_selection(self):
        for ctype in ['individual', 'business', 'government']:
            partner = self.env['res.partner'].create({
                'name': f'Test {ctype}',
                'tsc_customer_type': ctype,
            })
            self.assertEqual(partner.tsc_customer_type, ctype)
