# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Employee External Sync (for CLVhealth-JCAFB Solution)',
    'summary': 'Employee External Sync Module used in CLVhealth-JCAFB Solution.',
    'version': '15.0.6.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_employee',
        'clv_external_sync_jcafb',
    ],
    'data': [
        'data/hr_department_rec.xml',
        'data/hr_department_sync.xml',
        'data/hr_job_sync.xml',
        'data/hr_employee_rec.xml',
        'data/hr_employee_1_sync.xml',
        'data/hr_employee_2_sync.xml',
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
