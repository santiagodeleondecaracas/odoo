# -*- coding: utf-8 -*-
{
    # Theme information
    'name': 'Purchase Report Custom',
    'version': '17.0.0.1',
    'summary': 'Purchase Report Custom Agg Multy Currency.',
    'category': 'Purchase/Purchase',
    'description': """Purchase report custom  add Multy Currency.""",
    # Author
    'author': 'ITBC Venezuela',
    'contributors': [
        'Aarón Argotte, Email: <[aaron_argotte@hotmail.com]>,GitHub: <santiagodeleondecaracas>',
    ],
    # Dependencies
    'depends': [
        'purchase',
        'l10n_ve_currency_rate',
    ],
    # always loaded
    'data' : [
        ## Security
        
        ## Report
        'views/purchase_report_views.xml'
        ## Wiews

        ## Wizard
        
    ],
    # Technical
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,

}
