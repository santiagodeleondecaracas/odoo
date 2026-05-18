{
    'name': 'MRP Backdating Extension',
    'version': '17.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Extiende stock_move_backdating para Órdenes de Producción',
    'author': 'aaron_argotte@hotmail.com',
    'depends': [
        'mrp',
        'stock_account',
    ],
    'data': [
        'views/mrp_production_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'price': 120.0,           # Required to display "on sale"
    'currency': 'USD',        # Must be EUR or USD (Odoo preferred default is EUR)
    'license': 'OPL-1',       # MANDATORY for paid apps. Open source licenses will break the pricing logic.
    'application': True,      # Tells the app store to treat it as a standalone app
    'installable': True,
}