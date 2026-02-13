{
    'name': "Simple Sales Manager",
    'author': "Anas ahmed",
    'category': '',
    'depends': ['base','sale_management',
        ],
    'data': [
        'security\security.xml',
        'security\ir.model.access.csv',
        'views\\base_menu.xml',
        'views\simple_sale_order.xml',
        'data\sequency.xml',
        'reports\simple_sale_order_report.xml',
        'wizerd\print_report_wizerd.xml',
        'views\sale_order_inherit_view.xml',




    ],
      'application': True,
}