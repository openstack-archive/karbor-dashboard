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
from django.utils.translation import ungettext_lazy

from horizon import tables

from karbor_dashboard.api import karbor as karborclient


class ScheduledOperationFilterAction(tables.FilterAction):
    def filter(self, table, scheduledoperations, filter_string):
        """Naive case-insensitive search."""
        query = filter_string.lower()
        return [scheduledoperation
                for scheduledoperation in scheduledoperations
                if query in scheduledoperation.name.lower()]


class DeleteScheduledOperationsAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(u"Delete Scheduled Operation",
                              u"Delete Scheduled Operations",
                              count)

    @staticmethod
    def action_past(count):
        return ungettext_lazy(u"Deleted Scheduled Operation",
                              u"Deleted Scheduled Operations",
                              count)

    def allowed(self, request, scheduledoperation):
        return True

    def delete(self, request, obj_id):
        karborclient.scheduled_operation_delete(request, obj_id)


class ScheduledOperationsTable(tables.DataTable):
    id = tables.Column(
        'id',
        verbose_name=_('ID'))
    name = tables.Column(
        'name',
        verbose_name=_('Name'))
    operation_type = tables.Column(
        'operation_type',
        verbose_name=_('Operation Type'))
    plan_name = tables.Column(
        'plan_name',
        verbose_name=_('Protection Plan'))
    provider_name = tables.Column(
        'provider_name',
        verbose_name=_('Protection Provider'))
    trigger_name = tables.Column(
        'trigger_name',
        verbose_name=_('Trigger'))

    class Meta(object):
        name = 'scheduledoperations'
        verbose_name = _('Scheduled Operations')
        row_actions = (DeleteScheduledOperationsAction,)
        table_actions = (ScheduledOperationFilterAction,
                         DeleteScheduledOperationsAction)
