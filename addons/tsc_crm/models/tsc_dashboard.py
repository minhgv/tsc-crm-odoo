from odoo import _, api, fields, models


class TscDashboard(models.Model):
    _name = 'tsc.dashboard'
    _description = _('Dashboard')
    _rec_name = 'name'

    name = fields.Char(string=_('Dashboard'), default=_('TSC CRM Dashboard'))

    def _get_stats(self):
        self.ensure_one()
        lead_model = self.env['crm.lead'].sudo()
        tech_model = self.env['tsc.technical.task'].sudo()

        stages = self.env['crm.stage'].sudo().search([], order='sequence')
        stage_stats = []
        for stage in stages:
            count = lead_model.search_count([
                ('tsc_order_id', '!=', False),
                ('stage_id', '=', stage.id),
            ])
            stage_stats.append({
                'stage_id': stage.id,
                'stage_name': stage.name,
                'count': count,
            })

        regions = self.env['tsc.region'].sudo().search([('active', '=', True)])
        region_stats = []
        for region in regions:
            count = lead_model.search_count([
                ('tsc_order_id', '!=', False),
                ('tsc_region_id', '=', region.id),
            ])
            region_stats.append({
                'region_id': region.id,
                'region_name': region.name,
                'count': count,
            })

        stats = {
            'total_orders': lead_model.search_count([('tsc_order_id', '!=', False)]),
            'overdue_orders': lead_model.search_count([
                ('tsc_order_id', '!=', False),
                ('tsc_is_overdue', '=', True),
            ]),
            'stage_stats': stage_stats,
            'region_stats': region_stats,
            'pending_tasks': tech_model.search_count([('state', 'in', ['draft', 'assigned'])]),
            'overdue_tasks': tech_model.search_count([('is_overdue', '=', True)]),
            'done_tasks': tech_model.search_count([('state', '=', 'done')]),
        }

        for model_name in ['tsc.contract', 'tsc.invoice', 'tsc.payment']:
            try:
                self.env[model_name].sudo()
            except KeyError:
                continue

        if self.env['ir.model'].sudo().search_count([('model', '=', 'tsc.contract')]):
            contract_model = self.env['tsc.contract'].sudo()
            stats['total_contracts'] = contract_model.search_count([])
            stats['active_contracts'] = contract_model.search_count([('state', '=', 'active')])

        if self.env['ir.model'].sudo().search_count([('model', '=', 'tsc.invoice')]):
            invoice_model = self.env['tsc.invoice'].sudo()
            stats['total_invoices'] = invoice_model.search_count([])
            stats['unpaid_invoices'] = invoice_model.search_count([('state', 'in', ['draft', 'posted'])])

        if self.env['ir.model'].sudo().search_count([('model', '=', 'tsc.payment')]):
            payment_model = self.env['tsc.payment'].sudo()
            stats['total_revenue'] = sum(payment_model.search([
                ('state', '=', 'confirmed'),
            ]).mapped('amount'))

        return stats

    def action_view_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Orders'),
            'res_model': 'crm.lead',
            'view_mode': 'kanban,list,form',
            'domain': [('tsc_order_id', '!=', False)],
            'context': {'group_by': 'stage_id'},
        }

    def action_view_overdue(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Overdue Orders'),
            'res_model': 'crm.lead',
            'view_mode': 'kanban,list,form',
            'domain': [('tsc_order_id', '!=', False), ('tsc_is_overdue', '=', True)],
        }

    def action_view_tech_tasks(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Technical Tasks'),
            'res_model': 'tsc.technical.task',
            'view_mode': 'list,form',
        }

    def action_view_overdue_tasks(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Overdue Tasks'),
            'res_model': 'tsc.technical.task',
            'view_mode': 'list,form',
            'domain': [('is_overdue', '=', True)],
        }

    def action_open_kanban(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Orders Kanban'),
            'res_model': 'crm.lead',
            'view_mode': 'kanban',
            'domain': [('tsc_order_id', '!=', False)],
            'context': {'group_by': 'stage_id'},
        }
