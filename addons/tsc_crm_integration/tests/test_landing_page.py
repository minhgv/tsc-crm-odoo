from odoo.tests.common import TransactionCase


class TestTscLandingPage(TransactionCase):

    def setUp(self):
        super().setUp()
        self.service = self.env['tsc.service'].create({
            'name': 'Cloud Server',
            'code': 'CS',
            'service_type': 'direct',
        })

    def test_landing_page_creation(self):
        page = self.env['tsc.landing.page'].create({
            'name': 'TSC Landing Page',
            'slogan': 'Your Digital Partner',
            'seo_title': 'TSC CRM - Digital Services',
            'seo_description': 'TSC provides digital services',
        })
        self.assertEqual(page.name, 'TSC Landing Page')
        self.assertTrue(page.active)

    def test_landing_page_with_services(self):
        page = self.env['tsc.landing.page'].create({
            'name': 'Services Page',
            'service_ids': [(4, self.service.id)],
        })
        self.assertIn(self.service, page.service_ids)
