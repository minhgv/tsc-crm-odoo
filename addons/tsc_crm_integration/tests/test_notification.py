from odoo.tests.common import TransactionCase


class TestTscNotificationTemplate(TransactionCase):

    def test_template_sms(self):
        template = self.env['tsc.notification.template'].create({
            'name': 'New Order SMS',
            'notification_type': 'sms',
            'trigger_event': 'new_order',
            'body': 'New order received: {order_id}',
        })
        self.assertEqual(template.notification_type, 'sms')
        self.assertTrue(template.active)

    def test_template_all_types(self):
        for ntype in ['sms', 'email', 'push']:
            template = self.env['tsc.notification.template'].create({
                'name': f'Template {ntype}',
                'notification_type': ntype,
                'trigger_event': 'order_assigned',
                'body': 'Test body',
            })
            self.assertEqual(template.notification_type, ntype)

    def test_template_triggers(self):
        triggers = ['new_order', 'order_assigned', 'order_transferred',
                     'order_overdue', 'contract_signed', 'invoice_created', 'payment_received']
        for trigger in triggers:
            template = self.env['tsc.notification.template'].create({
                'name': f'Trigger {trigger}',
                'notification_type': 'email',
                'trigger_event': trigger,
                'body': 'Test body',
            })
            self.assertEqual(template.trigger_event, trigger)


class TestTscNotificationLog(TransactionCase):

    def test_log_creation(self):
        template = self.env['tsc.notification.template'].create({
            'name': 'Test Template',
            'notification_type': 'sms',
            'trigger_event': 'new_order',
            'body': 'Test',
        })
        log = self.env['tsc.notification.log'].create({
            'template_id': template.id,
            'recipient': '2055123456',
            'notification_type': 'sms',
            'body': 'Order created',
            'state': 'sent',
        })
        self.assertEqual(log.state, 'sent')
        self.assertEqual(log.recipient, '2055123456')

    def test_log_states(self):
        template = self.env['tsc.notification.template'].create({
            'name': 'State Test',
            'notification_type': 'email',
            'trigger_event': 'payment_received',
            'body': 'Payment received',
        })
        for state in ['pending', 'sent', 'failed']:
            log = self.env['tsc.notification.log'].create({
                'template_id': template.id,
                'recipient': 'test@test.la',
                'notification_type': 'email',
                'body': 'Test',
                'state': state,
            })
            self.assertEqual(log.state, state)
