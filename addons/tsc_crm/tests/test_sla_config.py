from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase


class TestTscSlaConfig(TransactionCase):

    def setUp(self):
        super().setUp()
        try:
            self.sla_config = self.env['tsc.sla.config'].search([], limit=1)
        except KeyError:
            self.skipTest('tsc.sla.config model not available')

    def test_sla_config_exists(self):
        self.assertTrue(self.sla_config.exists())

    def test_get_deadline_hours(self):
        if not hasattr(self.sla_config, 'get_deadline'):
            self.skipTest('get_deadline not available')
        start = datetime(2024, 6, 1, 10, 0, 0)
        deadline = self.sla_config.get_deadline(start)
        self.assertIsNotNone(deadline)
