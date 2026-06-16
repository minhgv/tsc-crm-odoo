{
    'name': 'TSC CRM Workflow',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Contract, invoice, payment, VAT/WHT, exchange rate, SLA',
    'description': 'Workflow module for TSC CRM. Manages contracts, invoices, payments, VAT/WHT configuration, exchange rates, and SLA tracking.',
    'author': 'TSC',
    'website': 'https://tsc.la',
    'depends': [
        'tsc_crm',
        'tsc_crm_service',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/tsc_contract_views.xml',
        'views/tsc_invoice_views.xml',
        'views/tsc_payment_views.xml',
        'views/tsc_config_views.xml',
        'views/tsc_voffice_views.xml',
        'views/tsc_menu.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
