{
    'name': 'TSC CRM Commission',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Commission rules and auto-calculation',
    'description': 'Commission module for TSC CRM. Manages commission rules and auto-calculation on invoice payment.',
    'author': 'TSC',
    'website': 'https://tsc.la',
    'depends': [
        'tsc_crm',
        'tsc_crm_service',
        'tsc_crm_workflow',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/tsc_commission_views.xml',
        'views/tsc_menu.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
