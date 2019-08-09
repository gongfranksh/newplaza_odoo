# -*- coding: utf-8 -*-
{
    'name': "bn_newplaza",

    'summary': """
         for analysis buynow newplaza contractor data""",

    'description': """
       for analysis buynow newplaza contractor data
    """,

    'author': "buynow",
    'website': "http://www.buynow.com.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/bn_newplaza_base_info.xml',
        'views/bn_rpt_floor_plan.xml',
        'views/bn_rpt_contract_file.xml',
        'views/proc_sync_newplaza.xml',
        'views/bn_discount_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}