{
    'name': 'TSC CRM Administration',
    'version': '18.0.1.0.0',
    'category': 'Administration',
    'summary': 'User management, organization hierarchy, role & permission',
    'description': 'Administration module for TSC CRM. Manages organization hierarchy, roles, and permissions.',
    'author': 'TSC',
    'website': 'https://tsc.la',
    'depends': [
        'tsc_crm',
        'tsc_crm_auth',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/tsc_organization_views.xml',
        'views/tsc_role_permission_views.xml',
        'views/tsc_menu.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
