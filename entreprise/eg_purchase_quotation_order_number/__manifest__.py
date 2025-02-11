{
    'name': 'Purchase Quotation number',
    'version': '18.0',
    'category': 'Purchase',
    'summery': 'Purchase Quotation number',
    'author': 'INKERP',
    'website': "https://www.inkerp.com",
    'depends': ['purchase'],
    'data': [
        'data/quotation_order_sequence.xml',
        'reports/purchase_report_templates.xml',
        'views/purchase_order_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
