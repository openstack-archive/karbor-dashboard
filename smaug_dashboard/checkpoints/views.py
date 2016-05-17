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
from horizon.utils import memoized

from smaug_dashboard.api import smaug as smaugclient
from smaug_dashboard.checkpoints import tables
from smaug_dashboard.checkpoints import utils


class IndexView(horizon_tables.DataTableView):
    table_class = tables.CheckpointsTable
    template_name = 'checkpoints/index.html'
    page_title = _("Checkpoints")

    @memoized.memoized_method
    def get_provider_list(self):
        return smaugclient.provider_list(self.request)

    @memoized.memoized_method
    def get_plan_list(self):
        return smaugclient.plan_list(self.request)

    @memoized.memoized_method
    def get_filter_list(self):
        filters = {}

        # Get all filter
        for key in utils.FILTER_LIST:
            filters[key] = self.request.POST.get(key, u"All")

        # Remove the "All" of provider_filter
        provider_filter = utils.FILTER_LIST[0]
        try:
            providers = self.get_provider_list()
            filters[provider_filter] = \
                self.request.POST.get(provider_filter, providers[0].id)
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve anyone provider.'))

        # Get arguments from the providers page
        if provider_filter in self.kwargs.keys():
            filters[provider_filter] = self.kwargs[provider_filter]
        return filters

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            context["provider_list"] = self.get_provider_list()
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve anyone provider.'))

        context["plan_list"] = self.get_plan_list()
        context["date_list"] = utils.DATE_CHOICES
        context["url"] = reverse("horizon:smaug:checkpoints:index")
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
        prev_marker = self.request.GET.get(
            tables.CheckpointsTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                tables.CheckpointsTable._meta.pagination_param, None)

        reversed_order = prev_marker is not None
        checkpoints = []
        try:
            search_opts = self.get_search_opts()

            # Get provider id
            provider_id = search_opts.pop(utils.FILTER_LIST[0], None)

            checkpoints, self._more, self._prev = \
                smaugclient.checkpoint_list_paged(
                    self.request,
                    provider_id=provider_id,
                    search_opts=search_opts,
                    marker=marker,
                    paginate=True,
                    sort_dir='asc',
                    sort_key='name',
                    reversed_order=reversed_order)
            for checkpoint in checkpoints:
                provider = smaugclient.provider_get(self.request,
                                                    checkpoint.provider_id)
                setattr(checkpoint, "provider_name", provider.name)
        except Exception:
            self._prev = False
            self._more = False
            exceptions.handle(self.request,
                              _('Unable to retrieve checkpoints list.'))
        return checkpoints
