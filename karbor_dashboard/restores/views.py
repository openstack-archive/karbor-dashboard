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
from karbor_dashboard.restores import tables


class IndexView(horizon_tables.DataTableView):
    table_class = tables.RestoresTable
    template_name = 'restores/index.html'
    page_title = _("Restores")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        request = self.request
        prev_marker = request.GET.get(
            tables.RestoresTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = request.GET.get(
                tables.RestoresTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        restores = []
        try:
            restores, self._more, self._prev = \
                karborclient.restore_list_paged(
                    self.request,
                    marker=marker,
                    paginate=True,
                    sort_dir='asc',
                    sort_key='id',
                    reversed_order=reversed_order)

            for restore in restores:
                try:
                    checkpoint = karborclient.checkpoint_get(
                        self.request,
                        restore.provider_id,
                        restore.checkpoint_id)
                    plan_name = checkpoint.protection_plan["name"]
                except Exception:
                    plan_name = "Not Found"
                provider = karborclient.provider_get(self.request,
                                                     restore.provider_id)
                setattr(restore, "name", plan_name)
                setattr(restore, "provider_name", provider.name)

        except Exception:
            self._prev = False
            self._more = False
            exceptions.handle(self.request,
                              _('Unable to retrieve restore list.'))
        return restores
