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

from horizon import exceptions
from horizon import tables as horizon_tables

from karbor_dashboard.api import karbor as karborclient
from karbor_dashboard.scheduledoperations import tables


class IndexView(horizon_tables.DataTableView):
    table_class = tables.ScheduledOperationsTable
    template_name = 'scheduledoperations/index.html'
    page_title = _("Scheduled Operations")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        request = self.request
        prev_marker = request.GET.get(
            tables.ScheduledOperationsTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = request.GET.get(
                tables.ScheduledOperationsTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        scheduledoperations = []
        try:
            scheduledoperations, self._more, self._prev = \
                karborclient.scheduled_operation_list_paged(
                    self.request,
                    marker=marker,
                    paginate=True,
                    sort_dir='asc',
                    sort_key='name',
                    reversed_order=reversed_order)

            for scheduledoperation in scheduledoperations:
                plan_name, provider_name, trigger_name = '', '', ''
                operation_definition = scheduledoperation.operation_definition

                if "plan_id" in operation_definition.keys():
                    plan = karborclient.plan_get(
                        self.request,
                        operation_definition["plan_id"])
                    if plan:
                        plan_name = plan.name

                if "provider_id" in operation_definition.keys():
                    provider = karborclient.provider_get(
                        self.request,
                        operation_definition["provider_id"])
                    if provider:
                        provider_name = provider.name

                trigger = karborclient.trigger_get(
                    self.request,
                    scheduledoperation.trigger_id)
                if trigger:
                    trigger_name = trigger.name

                setattr(scheduledoperation, "plan_name", plan_name)
                setattr(scheduledoperation, "provider_name", provider_name)
                setattr(scheduledoperation, "trigger_name", trigger_name)

        except Exception:
            self._prev = False
            self._more = False
            exceptions.handle(
                self.request,
                _('Unable to retrieve scheduled operation list.'))
        return scheduledoperations
