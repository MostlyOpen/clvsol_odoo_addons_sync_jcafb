# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Lab Test External Sync (for CLVhealth-JCAFB Solution)',
    'summary': 'Lab Test External Sync Module used in CLVhealth-JCAFB Solution.',
    'version': '15.0.6.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_lab_test',
        'clv_external_sync',
    ],
    'data': [
        'data/lab_test_type_1_sync.xml',
        'data/lab_test_type_2_sync.xml',
        'data/lab_test_type_parameter_sync.xml',
        # 'data/lab_test_export_xls_param_sync.xml',
        'data/lab_test_request_1_sync.xml',
        'data/lab_test_request_2_sync.xml',
        'data/lab_test_result_1_sync.xml',
        'data/lab_test_result_2_sync.xml',
        'data/lab_test_report_1_sync.xml',
        'data/lab_test_report_2_sync.xml',
        # # 'data/lab_test_report_updt_result_id.xml',
        'data/lab_test_criterion_1_sync.xml',
        'data/lab_test_criterion_2_sync.xml',
    ],
    'demo': [],
    'test': [],
    'init_xml': [],
    'test': [],
    'update_xml': [],
    'installable': True,
    'application': False,
    'active': False,
    'css': [],
}
