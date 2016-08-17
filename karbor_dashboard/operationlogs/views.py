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

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables as horizon_tables

from karbor_dashboard.api import karbor as karborclient
from karbor_dashboard.operationlogs import tables
from karbor_dashboard.operationlogs import utils


class IndexView(horizon_tables.DataTableView):
    table_class = tables.OperationLogsProtectTable
    template_name = 'operationlogs/index.html'
    page_title = _("Operation Logs")

    def get_table(self):
        if not self.table_class:
            raise AttributeError('You must specify a DataTable class for the '
                                 '"table_class" attribute on %s.'
                                 % self.__class__.__name__)
        # Protect is the default operation type
        type_filter = self.request.POST.get(utils.OPERATION_TYPE_FILTER,
                                            utils.OPERATION_TYPE_PROTECT)
        self.table_class = eval("tables.OperationLogs%sTable"
                                % str(type_filter))
        if not hasattr(self, "table"):
            self.table = self.table_class(self.request, **self.kwargs)
        return self.table

    def get_filter_list(self):
        filters = {}

        # Operation type
        filters[utils.OPERATION_TYPE_FILTER] = \
            self.request.POST.get(utils.OPERATION_TYPE_FILTER,
                                  utils.OPERATION_TYPE_PROTECT)
        # Operation status
        filters[utils.OPERATION_STATUS_FILTER] = \
            self.request.POST.get(utils.OPERATION_STATUS_FILTER, u"All")

        return filters

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["type_list"] = utils.OPERATION_TYPE_CHOICES
        context["status_list"] = utils.OPERATION_STATUS_CHOICES
        context["url"] = reverse("horizon:karbor:operationlogs:index")
        context = dict(context, **self.get_filter_list())
        return context

    def get_search_opts(self):
        search_opts = self.get_filter_list()
        for key, val in search_opts.items():
            if val == u"All":
                search_opts.pop(key)
        return search_opts

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        logs = []
        try:
            search_opts = self.get_search_opts()
            search_type = search_opts.get(utils.OPERATION_TYPE_FILTER,
                                          utils.OPERATION_TYPE_PROTECT)

            if search_type == utils.OPERATION_TYPE_PROTECT:
                logs = self.get_protect_data(search_opts)
            elif search_type == utils.OPERATION_TYPE_RESTORE:
                logs = self.get_restore_data(search_opts)
            elif search_type == utils.OPERATION_TYPE_DELETE:
                logs = self.get_delete_data(search_opts)

        except Exception:
            exceptions.handle(self.request,
                              _('Unable to retrieve operation log list.'))
        return logs

    def get_protect_data(self, search_opts):
        # TODO(xiangxinyong) Get protect operation logs
        logs, self._more, self._prev = ([], False, False)
        return logs

    def get_restore_data(self, search_opts):
        prev_marker = self.request.GET.get(
            tables.OperationLogsRestoreTable._meta.prev_pagination_param,
            None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                tables.OperationLogsRestoreTable._meta.pagination_param,
                None)

        reversed_order = prev_marker is not None
        logs = []
        try:
            # Get filter_opts
            filter_opts = None
            status = search_opts.get(utils.OPERATION_STATUS_FILTER, None)
            if status is not None:
                filter_opts = {"status": status}

            # Get restore operation logs
            logs, self._more, self._prev = \
                karborclient.restore_list_paged(
                    self.request,
                    search_opts=filter_opts,
                    marker=marker,
                    paginate=True,
                    sort_dir='asc',
                    sort_key='id',
                    reversed_order=reversed_order)

            for log in logs:
                checkpoint = karborclient.checkpoint_get(self.request,
                                                         log.provider_id,
                                                         log.checkpoint_id)
                provider = karborclient.provider_get(self.request,
                                                     log.provider_id)
                setattr(log, "name", checkpoint.protection_plan["name"])
                setattr(log, "type",
                        utils.OPERATION_TYPE_DICT[
                            utils.OPERATION_TYPE_RESTORE])
                setattr(log, "provider_name", provider.name)

        except Exception:
            self._prev = False
            self._more = False
            exceptions.handle(self.request,
                              _('Unable to retrieve restore list.'))
        return logs

    def get_delete_data(self, search_opts):
        # TODO(xiangxinyong) Get delete operation logs
        logs, self._more, self._prev = ([], False, False)
        return logs
