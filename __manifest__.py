{

    'name': 'Purchase Request',
    'version': '1.0.0',
    'author': 'mohamed',
    'sequence': -12,
    'website': 'www.proengmht.com',
    'category': '',
    'summary': '',
    'description': """""",
    'demo': [],
    'depends': ['sale','base','purchase','mail'],
    'data': ['security /group.xml',
             "security /ir.model.access.csv",
             'data/email_template.xml',
             'data/sequence.xml',
                'wizard/rejection_reason_views.xml' ,
             'views/purchase_request_views.xml'
             ],
    # 'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',

}
