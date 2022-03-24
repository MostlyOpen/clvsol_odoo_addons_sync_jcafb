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

    def _person_relation_setup(self, schedule):

        from time import time
        start = time()

        if schedule.enable_sync:

            date_last_sync = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            method_args = literal_eval(schedule.method_args)

            AbstractExternalSync = self.env['clv.abstract.external_sync']
            ExternalSync = self.env['clv.external_sync']
            PersonRelationType = self.env['clv.person.relation.type']
            PersonRelation = self.env['clv.person.relation']

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

                schedule.sync_log += 'Executing: "' + '_person_relation_setup' + '"...\n\n'

                sync_objects = ExternalSync.search([
                    ('model', '=', 'clv.person'),
                    ('external_sync_state', '=', 'synchronized'),
                ])
                _logger.info(u'%s %s', '>>>>>>>>>> (sync_objects):', len(sync_objects))

                reg_count = 0

                external_object_fields = ['id', 'spouse_id', 'father_id', 'mother_id',
                                          'responsible_id', 'caregiver_id']

                spouse_relation_id = PersonRelationType.search([
                    ('name', '=', 'Spouse'),
                ]).id

                father_relation_id = PersonRelationType.search([
                    ('name', '=', 'Father'),
                ]).id

                mother_relation_id = PersonRelationType.search([
                    ('name', '=', 'Mother'),
                ]).id

                responsible_relation_id = PersonRelationType.search([
                    ('name', '=', 'Responsible'),
                ]).id

                caregiver_relation_id = PersonRelationType.search([
                    ('name', '=', 'Caregiver'),
                ]).id

                for sync_object in sync_objects:

                    reg_count += 1
                    _logger.info(u'%s %s %s', '>>>>>>>>>>', reg_count,
                                 sync_object.external_id, )

                    left_person_id = sync_object.res_id

                    external_args = [
                        ('id', '=', sync_object.external_id),
                    ]
                    external_objects = sock.execute(external_dbname, uid, external_user_pw,
                                                    'clv.person', 'search_read',
                                                    external_args,
                                                    external_object_fields)

                    external_object = external_objects[0]

                    if external_object['spouse_id'] is not False:

                        spouse_sync_object = ExternalSync.search([
                            ('model', '=', 'clv.person'),
                            ('external_sync_state', '=', 'synchronized'),
                            ('external_id', '=', external_object['spouse_id'][0]),
                        ])
                        right_person_id = spouse_sync_object.res_id
                        _logger.info(u'>>>>>>>>>>>>>>> %s %s (%s)', left_person_id, right_person_id, 'Responsible')

                        values = {}
                        values['left_person_id'] = left_person_id
                        values['right_person_id'] = right_person_id
                        values['type_id'] = spouse_relation_id
                        PersonRelation.create(values)

                    if external_object['father_id'] is not False:

                        father_sync_object = ExternalSync.search([
                            ('model', '=', 'clv.person'),
                            ('external_sync_state', '=', 'synchronized'),
                            ('external_id', '=', external_object['father_id'][0]),
                        ])
                        right_person_id = father_sync_object.res_id
                        _logger.info(u'>>>>>>>>>>>>>>> %s %s (%s)', left_person_id, right_person_id, 'Responsible')

                        values = {}
                        values['left_person_id'] = left_person_id
                        values['right_person_id'] = right_person_id
                        values['type_id'] = father_relation_id
                        PersonRelation.create(values)

                    if external_object['mother_id'] is not False:

                        mother_sync_object = ExternalSync.search([
                            ('model', '=', 'clv.person'),
                            ('external_sync_state', '=', 'synchronized'),
                            ('external_id', '=', external_object['mother_id'][0]),
                        ])
                        right_person_id = mother_sync_object.res_id
                        _logger.info(u'>>>>>>>>>>>>>>> %s %s (%s)', left_person_id, right_person_id, 'Responsible')

                        values = {}
                        values['left_person_id'] = left_person_id
                        values['right_person_id'] = right_person_id
                        values['type_id'] = mother_relation_id
                        PersonRelation.create(values)

                    if external_object['responsible_id'] is not False:

                        responsible_sync_object = ExternalSync.search([
                            ('model', '=', 'clv.person'),
                            ('external_sync_state', '=', 'synchronized'),
                            ('external_id', '=', external_object['responsible_id'][0]),
                        ])
                        right_person_id = responsible_sync_object.res_id
                        _logger.info(u'>>>>>>>>>>>>>>> %s %s (%s)', left_person_id, right_person_id, 'Responsible')

                        values = {}
                        values['left_person_id'] = left_person_id
                        values['right_person_id'] = right_person_id
                        values['type_id'] = responsible_relation_id
                        PersonRelation.create(values)

                    if external_object['caregiver_id'] is not False:

                        caregiver_sync_object = ExternalSync.search([
                            ('model', '=', 'clv.person'),
                            ('external_sync_state', '=', 'synchronized'),
                            ('external_id', '=', external_object['caregiver_id'][0]),
                        ])
                        right_person_id = caregiver_sync_object.res_id
                        _logger.info(u'>>>>>>>>>>>>>>> %s %s (%s)', left_person_id, right_person_id, 'Caaregiver')

                        values = {}
                        values['left_person_id'] = left_person_id
                        values['right_person_id'] = right_person_id
                        values['type_id'] = caregiver_relation_id
                        PersonRelation.create(values)

            _logger.info(u'%s %s', '>>>>>>>>>> date_last_sync: ', date_last_sync)
            _logger.info(u'%s %s', '>>>>>>>>>> Execution time: ', secondsToStr(time() - start))

            schedule.date_last_sync = date_last_sync
            schedule.sync_log +=  \
                'method_args: ' + str(method_args) + '\n' + \
                'object_count: ' + str(object_count) + '\n' + \
                'date_last_sync: ' + str(date_last_sync) + '\n' + \
                'Execution time: ' + str(secondsToStr(time() - start)) + '\n\n'
