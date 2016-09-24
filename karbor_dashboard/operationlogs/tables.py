#    Copyright (c) 2016 Huawei, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import tables


class OperationLogsTable(tables.DataTable):
    id = tables.Column('id',
                       verbose_name=_('ID'))
    name = tables.Column('name',
                         verbose_name=_('Name'))
    type = tables.Column('type',
                         verbose_name=_('Type'))
    state = tables.Column('state',
                          verbose_name=_('State'))
    expect_start_time = tables.Column(
        'expect_start_time',
        verbose_name=_('Expect Start Time'))
    actual_start_time = tables.Column(
        'actual_start_time',
        verbose_name=_('Actual Start Time'))
    end_time = tables.Column(
        'end_time',
        verbose_name=_('End Time'))

    class Meta(object):
        name = 'operationlogs'
        verbose_name = _('Operation Logs')
