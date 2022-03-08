# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime
from functools import reduce
from ast import literal_eval

from odoo import models
# from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.http_routing.models.ir_http import slugify

_logger = logging.getLogger(__name__)


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ExternalSync(models.Model):
    _inherit = 'clv.external_sync'

    def x_survey_survey_adapt(self, schedule):

        from time import time
        start = time()

        if schedule.enable_sync:

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            method_args = literal_eval(schedule.method_args)

            SurveySurvey = self.env['survey.survey']
            surveys = SurveySurvey.search([])
            object_count = 0
            for survey in surveys:
                object_count += 1

                # access_token = slug(survey)
                access_token = slugify(survey.title or '')

                values = {}
                values['access_token'] = access_token
                survey.write(values)
                _logger.info(u'%s %s %s', '>>>>>>>>>> survey.title: ', object_count, survey.title)

            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.sync_log +=  \
                'method_args: ' + str(method_args) + '\n' + \
                'object_count: ' + str(object_count) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'

    def x_survey_question_adapt(self, schedule):

        from time import time
        start = time()

        if schedule.enable_sync:

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            method_args = literal_eval(schedule.method_args)

            _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

            AbstractExternalSync = self.env['clv.abstract.external_sync']
            SurveyQuestion = self.env['survey.question']
            ExternalSync = self.env['clv.external_sync']

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

            questions = SurveyQuestion.search([('is_page', '!=', True)])

            object_count = 0
            for question in questions:
                object_count += 1
                _logger.info(u'%s %s %s', '>>>>>>>>>> question.title: ', object_count, question.title)

                question_external_sync = ExternalSync.search(
                    [('model', '=', 'survey.question'),
                     ('res_id', '=', question.id)
                     ])
                remote_question = sock.execute(external_dbname, uid, external_user_pw,
                                               'survey.question', 'search_read',
                                               [('id', '=', question_external_sync.external_id)],
                                               ['title', 'survey_id', 'page_id'])

                page_external_sync = ExternalSync.search(
                    [('external_model', '=', 'survey.page'),
                     ('external_id', '=', remote_question[0]['page_id'][0])
                     ])

                question_record = {}
                question_record['page_id'] = page_external_sync.res_id
                question.write(question_record)

            questions = SurveyQuestion.search([], order='code')

            object_count_2 = 0
            for question in questions:
                object_count_2 += 1
                _logger.info(u'%s %s %s', '>>>>>>>>>> question.title: ', object_count_2, question.title)

                question_record = {}
                question_record['sequence'] = object_count_2
                question.write(question_record)

            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.sync_log +=  \
                'method_args: ' + str(method_args) + '\n' + \
                'object_count: ' + str(object_count) + '\n' + \
                'object_count_2: ' + str(object_count_2) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'

    def x_survey_label_adapt(self, schedule):

        from time import time
        start = time()

        if schedule.enable_sync:

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            method_args = literal_eval(schedule.method_args)

            _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

            AbstractExternalSync = self.env['clv.abstract.external_sync']
            SurveyLabel = self.env['survey.label']
            ExternalSync = self.env['clv.external_sync']

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

            labels = SurveyLabel.search([])

            object_count = 0
            for label in labels:
                object_count += 1
                _logger.info(u'%s %s %s', '>>>>>>>>>> label.value: ', object_count, label.value)

                label_external_sync = ExternalSync.search(
                    [('model', '=', 'survey.label'),
                     ('res_id', '=', label.id)
                     ])
                remote_label = sock.execute(external_dbname, uid, external_user_pw,
                                            'survey.label', 'search_read',
                                            [('id', '=', label_external_sync.external_id)],
                                            ['value', 'question_id', 'question_id_2'])

                if remote_label[0]['question_id'] is not False:
                    question_external_sync = ExternalSync.search(
                        [('external_model', '=', 'survey.question'),
                         ('external_id', '=', remote_label[0]['question_id'][0])
                         ])

                if remote_label[0]['question_id_2'] is not False:
                    question_2_external_sync = ExternalSync.search(
                        [('external_model', '=', 'survey.question'),
                         ('external_id', '=', remote_label[0]['question_id_2'][0])
                         ])

                question_record = {}
                if remote_label[0]['question_id'] is not False:
                    question_record['question_id'] = question_external_sync.res_id
                if remote_label[0]['question_id_2'] is not False:
                    question_record['question_id_2'] = question_2_external_sync.res_id
                label.write(question_record)

            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.sync_log +=  \
                'method_args: ' + str(method_args) + '\n' + \
                'object_count: ' + str(object_count) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'

    def x_survey_user_input_adapt(self, schedule):

        from time import time
        start = time()

        if schedule.enable_sync:

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            method_args = literal_eval(schedule.method_args)

            _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

            SurveyUserInput = self.env['survey.user_input']
            SurveyQuestion = self.env['survey.question']

            user_inputs = SurveyUserInput.search([])

            object_count = 0
            for user_input in user_inputs:
                object_count += 1
                _logger.info(u'%s %s %s', '>>>>>>>>>> user_input.survey_id: ', object_count, user_input.survey_id)

                questions = SurveyQuestion.search(
                    [('survey_id', '=', user_input.survey_id.id),
                     ('is_page', '=', False)
                     ])

                m2m_list = []
                for question in questions:
                    m2m_list.append((4, question.id))
                _logger.info(u'%s %s', '>>>>>>>>>>>>>>> m2m_list: ', m2m_list)

                user_input_record = {}
                user_input_record['question_ids'] = m2m_list
                user_input.write(user_input_record)

            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.sy0nc_log +=  \
                'method_args: ' + str(method_args) + '\n' + \
                'object_count: ' + str(object_count) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'

    def x_survey_user_input_adapt_2(self, schedule):

        from time import time
        start = time()

        if schedule.enable_sync:

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            method_args = literal_eval(schedule.method_args)

            _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

            AbstractExternalSync = self.env['clv.abstract.external_sync']
            SurveyUserInput = self.env['survey.user_input']
            ExternalSync = self.env['clv.external_sync']

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

            user_inputs = SurveyUserInput.search([])

            object_count = 0
            for user_input in user_inputs:
                object_count += 1
                _logger.info(u'%s %s %s', '>>>>>>>>>> user_input.survey_id: ', object_count, user_input.survey_id)

                user_input_external_sync = ExternalSync.search(
                    [('model', '=', 'survey.user_input'),
                     ('res_id', '=', user_input.id)
                     ])
                remote_user_input = sock.execute(external_dbname, uid, external_user_pw,
                                                 'survey.user_input', 'search_read',
                                                 [('id', '=', user_input_external_sync.external_id)],
                                                 ['survey_id', 'last_displayed_page_id'])

                if remote_user_input[0]['last_displayed_page_id'] is not False:
                    question_external_sync = ExternalSync.search(
                        [('external_model', '=', 'survey.page'),
                         ('external_id', '=', remote_user_input[0]['last_displayed_page_id'][0])
                         ])

                token = slugify(user_input.document_code or '')

                user_input_record = {}
                if remote_user_input[0]['last_displayed_page_id'] is not False:
                    user_input_record['last_displayed_page_id'] = question_external_sync.res_id
                if token != '':
                    user_input_record['token'] = token
                user_input.write(user_input_record)

            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.sync_log +=  \
                'method_args: ' + str(method_args) + '\n' + \
                'object_count: ' + str(object_count) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'

    def x_survey_user_input_line_adapt(self, schedule):

        from time import time
        start = time()

        if schedule.enable_sync:

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            method_args = literal_eval(schedule.method_args)

            _logger.info(u'%s %s', '>>>>>>>>>> method_args: ', method_args)

            AbstractExternalSync = self.env['clv.abstract.external_sync']
            SurveyUserInputLine = self.env['survey.user_input_line']
            ExternalSync = self.env['clv.external_sync']

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

            user_input_lines = SurveyUserInputLine.search([])

            object_count = 0
            for user_input_line in user_input_lines:
                object_count += 1
                _logger.info(u'%s %s %s', '>>>>>>>>>> user_input_line.user_input_id: ',
                             object_count, user_input_line.user_input_id)

                user_input_line_external_sync = ExternalSync.search(
                    [('model', '=', 'survey.user_input_line'),
                     ('res_id', '=', user_input_line.id)
                     ])
                remote_user_input_line = sock.execute(external_dbname, uid, external_user_pw,
                                                      'survey.user_input_line', 'search_read',
                                                      [('id', '=', user_input_line_external_sync.external_id)],
                                                      ['user_input_id', 'question_id'])

                if remote_user_input_line[0]['question_id'] is not False:
                    question_external_sync = ExternalSync.search(
                        [('external_model', '=', 'survey.page'),
                         ('external_id', '=', remote_user_input_line[0]['question_id'][0])
                         ])

                user_input_line_record = {}
                if remote_user_input_line[0]['question_id'] is not False:
                    user_input_line_record['question_id'] = question_external_sync.res_id
                user_input_line.write(user_input_line_record)

            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.sync_log +=  \
                'method_args: ' + str(method_args) + '\n' + \
                'object_count: ' + str(object_count) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'
