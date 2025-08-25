# -*- coding: utf-8 -*-
{
    'name': "odoo_medical",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'license': 'GPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'icon': '/odoo_medical/static/description/icon.png',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'partner_contact_birthdate', 'partner_firstname', 'product', 'account', 'mail'],

    # always loaded
    'data': [
        'security/medical_history_security.xml',
        'security/ir.model.access.csv',
        'data/medical_consultation_sequence.xml',
        'data/medical_therapy_sequence.xml',
        'data/medical_xray_sequence.xml',
        'data/icd10_infectious_diseases_data.xml',
        'reports/medical_certificate_reports.xml',
        'reports/private_medical_certificate_template.xml',
        'reports/iess_medical_certificate_template.xml',
        'views/medical_consultation_views.xml',
        'views/medical_history_views.xml',
        'views/medical_icd10_group_views.xml',
        'views/medical_affected_apparatus_views.xml',
        'views/medical_treatment_component_views.xml',
        'views/medical_treatment_session_views.xml',
        'views/medical_treatment_views.xml',
        'views/medical_session_record_views.xml',
        'views/medical_therapy_views.xml',
        'views/medical_therapy_menus.xml',
        'views/medical_xray_area_views.xml',
        'views/medical_xray_order_views.xml',
        'views/medical_xray_menus.xml',
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        'demo/therapy_demo.xml',
        'demo/xray_demo.xml',
    ],
}

