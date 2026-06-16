from odoo import _, api, fields, models


class TscDashboard(models.Model):
    _name = 'tsc.dashboard'
    _description = _('Dashboard')
    _rec_name = 'name'

    name = fields.Char(string=_('Dashboard'), default=_('TSC CRM Dashboard'))

    def _get_stats(self):
        self.ensure_one()
        lead_model = self.env['crm.lead'].sudo()
        contract_model = self.env['tsc.contract'].sudo()
        invoice_model = self.env['tsc.invoice'].sudo()
        payment_model = self.env['tsc.payment'].sudo()
        commission_model = self.env['tsc.commission'].sudo()

        return {
            'total_orders': lead_model.search_count([('tsc_order_id', '!=', False)]),
            'overdue_orders': lead_model.search_count([
                ('tsc_order_id', '!=', False),
                ('tsc_is_overdue', '=', True),
            ]),
            'draft_orders': lead_model.search_count([
                ('tsc_order_id', '!=', False),
                ('stage_id.is_won', '=', False),
            ]),
            'done_orders': lead_model.search_count([
                ('tsc_order_id', '!=', False),
                ('stage_id.is_won', '=', True),
            ]),
            'total_contracts': contract_model.search_count([]),
            'active_contracts': contract_model.search_count([('state', '=', 'active')]),
            'total_invoices': invoice_model.search_count([]),
            'unpaid_invoices': invoice_model.search_count([('state', 'in', ['draft', 'posted'])]),
            'total_revenue': sum(payment_model.search([
                ('state', '=', 'confirmed'),
            ]).mapped('amount')),
            'total_commission': sum(commission_model.search([
                ('state', 'in', ['approved', 'paid']),
            ]).mapped('amount')),
        }

    def action_view_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Orders'),
            'res_model': 'crm.lead',
            'view_mode': 'list,form,kanban',
            'domain': [('tsc_order_id', '!=', False)],
        }

    def action_view_overdue(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Overdue Orders'),
            'res_model': 'crm.lead',
            'view_mode': 'list,form',
            'domain': [('tsc_order_id', '!=', False), ('tsc_is_overdue', '=', True)],
        }

    def action_view_contracts(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Contracts'),
            'res_model': 'tsc.contract',
            'view_mode': 'list,form',
        }

    def action_view_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoices'),
            'res_model': 'tsc.invoice',
            'view_mode': 'list,form',
        }

    def action_view_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments'),
            'res_model': 'tsc.payment',
            'view_mode': 'list,form',
        }
