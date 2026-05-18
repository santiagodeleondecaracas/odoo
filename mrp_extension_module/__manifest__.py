{
    'name': 'MRP Backdating Extension',
    'version': '17.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Extiende stock_move_backdating para Órdenes de Producción',
    'depends': [
        'mrp',
        'stock_account',
    ],
    'data': [
        'views/mrp_production_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}