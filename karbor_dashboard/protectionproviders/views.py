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
from horizon import tabs as horizon_tabs
from horizon.utils import memoized

from karbor_dashboard.api import karbor as karborclient
from karbor_dashboard.protectionproviders import tables
from karbor_dashboard.protectionproviders import tabs


class IndexView(horizon_tables.DataTableView):
    table_class = tables.ProtectionProvidersTable
    template_name = 'protectionproviders/index.html'
    page_title = _("Protection Providers")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        request = self.request
        prev_marker = request.GET.get(
            tables.ProtectionProvidersTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = request.GET.get(
                tables.ProtectionProvidersTable._meta.pagination_param, None)
            reversed_order = prev_marker is not None
        providers = []
        try:
            providers, self._more, self._prev = \
                karborclient.provider_list_paged(
                    request, None,
                    marker=marker,
                    paginate=True,
                    sort_dir='asc',
                    sort_key='name',
                    reversed_order=reversed_order)
        except Exception:
            self._prev = False
            self._more = False
            exceptions.handle(
                self.request,
                _('Unable to retrieve protection providers list.'))
        return providers


class DetailView(horizon_tabs.TabView):
    redirect_url = "horizon:karbor:protectionproviders:index"
    tab_group_class = tabs.ProviderDetailTabs
    template_name = 'protectionproviders/detail.html'
    page_title = "{{ provider.name }}"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["provider"] = self.get_data()
        return context

    @memoized.memoized_method
    def get_data(self):
        try:
            provider_id = self.kwargs['provider_id']
            provider = karborclient.provider_get(self.request, provider_id)
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve protection provider details.'),
                redirect=reverse("horizon:karbor:protectionproviders:index"))
        return provider

    def get_tabs(self, request, *args, **kwargs):
        provider = self.get_data()
        return self.tab_group_class(request, provider=provider, **kwargs)
