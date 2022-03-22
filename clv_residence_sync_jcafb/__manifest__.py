# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Residence External Sync (for CLVhealth-JCAFB Solution)',
    'summary': 'Residence External Sync Module used in CLVhealth-JCAFB Solution.',
    'version': '15.0.6.0',
    'author': 'Carlos Eduardo Vercelino - CLVsol',
    'category': 'CLVsol Solutions',
    'license': 'AGPL-3',
    'website': 'https://github.com/CLVsol',
    'depends': [
        'clv_residence',
        'clv_external_sync',
    ],
    'data': [
        'data/residence_category_sync.xml',
        'data/residence_marker_sync.xml',
        'data/residence_1_sync.xml',
        'data/residence_2_sync.xml',
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
