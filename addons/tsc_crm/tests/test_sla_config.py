from odoo.tests.common import TransactionCase


class TestSlaConfig(TransactionCase):

    def test_sla_config_creation(self):
        sla = self.env['tsc.sla.config'].create({
            'name': 'Assignment SLA',
            'stage': 'assignment',
            'max_hours': 4,
            'warning_hours': 2,
            'applies_to': 'new_order',
        })
        self.assertEqual(sla.max_hours, 4)
        self.assertTrue(sla.active)

    def test_sla_config_all_stages(self):
        stages = ['assignment', 'survey', 'implementation', 'contract', 'payment']
        for stage in stages:
            sla = self.env['tsc.sla.config'].create({
                'name': f'{stage} SLA',
                'stage': stage,
                'max_hours': 24,
            })
            self.assertEqual(sla.stage, stage)
