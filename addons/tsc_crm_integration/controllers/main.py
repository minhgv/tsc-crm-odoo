from odoo import http
from odoo.http import request


class TscFrontendController(http.Controller):

    @http.route('/services', type='http', auth='public', website=True)
    def services(self, **kwargs):
        services = request.env['tsc.service'].sudo().search([('active', '=', True)])
        return request.render('tsc_crm_integration.services_page', {
            'services': services,
        })

    @http.route('/services/<int:service_id>', type='http', auth='public', website=True)
    def service_detail(self, service_id, **kwargs):
        service = request.env['tsc.service'].sudo().browse(service_id)
        if not service.exists():
            return request.not_found()
        return request.render('tsc_crm_integration.service_detail_page', {
            'service': service,
        })

    @http.route('/order/create', type='http', auth='user', website=True)
    def order_create(self, **kwargs):
        services = request.env['tsc.service'].sudo().search([('active', '=', True)])
        regions = request.env['tsc.region'].sudo().search([('active', '=', True)])
        return request.render('tsc_crm_integration.order_create_page', {
            'services': services,
            'regions': regions,
        })

    @http.route('/order/<string:order_code>/status', type='http', auth='user', website=True)
    def order_status(self, order_code, **kwargs):
        order = request.env['crm.lead'].sudo().search([('tsc_order_id', '=', order_code)], limit=1)
        if not order.exists():
            return request.not_found()
        return request.render('tsc_crm_integration.order_status_page', {
            'order': order,
        })

    @http.route('/invoice/<string:invoice_code>', type='http', auth='user', website=True)
    def invoice_view(self, invoice_code, **kwargs):
        invoice = request.env['tsc.invoice'].sudo().search([('name', '=', invoice_code)], limit=1)
        if not invoice.exists():
            return request.not_found()
        return request.render('tsc_crm_integration.invoice_view_page', {
            'invoice': invoice,
        })
