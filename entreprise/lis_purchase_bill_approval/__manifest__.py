# -*- coding: utf-8 -*-
{
    'name': "PO Bill Approval",
    'summary': "PO Bill Approval",
    'description': """ PO Bill Approval """,
    'author': "Loyal IT Solutions Pvt Ltd",
    'website': "https://www.loyalitsolutions.com",
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',
    'depends': ['purchase', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_data.xml',
        'views/purchase_order_views.xml',
        'views/account_move_views.xml',
        'wizard/reject_wizard_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
}
