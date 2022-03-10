# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime
from functools import reduce
from ast import literal_eval

from odoo import models

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ExternalSync(models.Model):
    _inherit = 'clv.external_sync'

    def _lab_test_report_updt_result_id(self, schedule):

        from time import time
        start = time()

        if schedule.enable_sync:

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            method_args = literal_eval(schedule.method_args)

            AbstractExternalSync = self.env['clv.abstract.external_sync']
            ExternalSync = self.env['clv.external_sync']
            LabTestReport = self.env['clv.lab_test.report']

            external_host = schedule.external_host_id.name
            external_dbname = schedule.external_host_id.external_dbname
            external_user = schedule.external_host_id.external_user
            external_user_pw = schedule.external_host_id.external_user_pw

            uid, sock, login_msg = AbstractExternalSync.external_sync_host_login(
                external_host,
                external_dbname,
                external_user,
                external_user_pw
            )
            schedule.sync_log += 'login_msg: ' + str(login_msg) + '\n\n'

            object_count = 0

            if uid is not False:

                schedule.sync_log += 'Executing: "' + '_lab_test_report_updt_result_id' + '"...\n\n'

                sync_objects = ExternalSync.search([
                    ('model', '=', 'clv.lab_test.result'),
                    ('external_sync_state', '=', 'synchronized'),
                ])
                _logger.info(u'%s %s', '>>>>>>>>>> (sync_objects):', len(sync_objects))

                reg_count = 0

                external_object_fields = ['id', 'lab_test_request_id', 'lab_test_report_id']

                for sync_object in sync_objects:

                    reg_count += 1
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', reg_count,
                                 sync_object.external_id, )

                    lab_test_result_id = sync_object.res_id

                    external_args = [
                        ('id', '=', sync_object.external_id),
                    ]
                    external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                                    'clv.lab_test.result', 'search_read',
                                                    external_args,
                                                    external_object_fields)

                    external_object = external_objects[0]

                    if external_object['lab_test_report_id'] is not False:

                        lab_test_report_sync_object = ExternalSync.search([
                            ('model', '=', 'clv.lab_test.report'),
                            ('external_sync_state', '=', 'synchronized'),
                            ('external_id', '=', external_object['lab_test_report_id'][0]),
                        ])

                        _logger.info(u'>>>>>>>>>>>>>>> %s %s', external_object, lab_test_report_sync_object)

                        lab_test_report_id = lab_test_report_sync_object.res_id
                        lab_test_report = LabTestReport.search([
                            ('id', '=', lab_test_report_id),
                        ])
                        lab_test_report.lab_test_result_id = lab_test_result_id

            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.sync_log +=  \
                'method_args: ' + str(method_args) + '\n' + \
                'object_count: ' + str(object_count) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'
