{
    'name': 'TSC CRM Service Catalog',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Service catalog, packages, combos, discounts, agencies',
    'description': 'Service catalog module for TSC CRM. Manages services, packages, combos, discounts, and agencies.',
    'author': 'TSC',
    'website': 'https://tsc.la',
    'depends': [
        'tsc_crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/tsc_service_views.xml',
        'views/tsc_package_views.xml',
        'views/tsc_combo_views.xml',
        'views/tsc_discount_views.xml',
        'views/tsc_agency_views.xml',
        'views/tsc_menu.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
