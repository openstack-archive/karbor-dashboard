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

import collections
from django.utils.translation import ugettext_lazy as _

OPERATION_TYPE_FILTER = 'type_filter'
OPERATION_STATUS_FILTER = 'status_filter'

OPERATION_TYPE_PROTECT = 'Protect'
OPERATION_TYPE_RESTORE = 'Restore'
OPERATION_TYPE_DELETE = 'Delete'

OPERATION_TYPE_CHOICES = [(OPERATION_TYPE_PROTECT, _('Protect')),
                          (OPERATION_TYPE_RESTORE, _('Restore')),
                          (OPERATION_TYPE_DELETE, _('Delete'))]
OPERATION_TYPE_DICT = collections.OrderedDict(OPERATION_TYPE_CHOICES)

OPERATION_STATUS_COMMITED = 'commited'
OPERATION_STATUS_RUNNING = 'running'
OPERATION_STATUS_FINISHED = 'finished'
OPERATION_STATUS_FAILED = 'failed'

OPERATION_STATUS_CHOICES = [(OPERATION_STATUS_COMMITED, _('Commited')),
                            (OPERATION_STATUS_RUNNING, _('Running')),
                            (OPERATION_STATUS_FINISHED, _('Finished')),
                            (OPERATION_STATUS_FAILED, _('Failed'))]
OPERATION_STATUS_DICT = collections.OrderedDict(OPERATION_STATUS_CHOICES)
