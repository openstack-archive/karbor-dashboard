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
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import tables as horizon_tables
from horizon.utils import memoized
from horizon import views as horizon_views

from karbor_dashboard.api import karbor as karborclient
from karbor_dashboard.triggers import forms
from karbor_dashboard.triggers import tables
from karbor_dashboard.triggers import utils


class IndexView(horizon_tables.DataTableView):
    table_class = tables.TriggersTable
    template_name = 'triggers/index.html'
    page_title = _("Triggers")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        request = self.request
        prev_marker = request.GET.get(
            tables.TriggersTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = request.GET.get(
                tables.TriggersTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        triggers = []
        try:
            triggers, self._more, self._prev = karborclient.trigger_list_paged(
                request, None,
                marker=marker,
                paginate=True,
                sort_dir='asc',
                sort_key='name',
                reversed_order=reversed_order)
        except Exception:
            self._prev = False
            self._more = False
            exceptions.handle(self.request,
                              _('Unable to retrieve triggers list.'))
        return triggers


class CreateView(horizon_forms.ModalFormView):
    template_name = 'triggers/create.html'
    modal_header = _("Create Trigger")
    form_id = "create_trigger_form"
    form_class = forms.CreateTriggerForm
    submit_label = _("Create Trigger")
    submit_url = reverse_lazy("horizon:karbor:triggers:create")
    success_url = reverse_lazy('horizon:karbor:triggers:index')
    page_title = _("Create Trigger")


class DetailView(horizon_views.HorizonTemplateView):
    template_name = 'triggers/detail.html'
    page_title = "{{ trigger.name }}"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        trigger = self.get_data()
        table = tables.TriggersTable(self.request)

        if trigger is not None and trigger.properties is not None:
            if trigger.properties["format"] == utils.CRONTAB:
                data = utils.CrontabUtil\
                    .convert_from_crontab(trigger.properties)
                if data:
                    for key, value in data.items():
                        setattr(trigger, key, value)

        context["trigger"] = trigger
        context["url"] = reverse("horizon:karbor:triggers:index")
        context["actions"] = table.render_row_actions(trigger)
        return context

    @memoized.memoized_method
    def get_data(self):
        try:
            trigger_id = self.kwargs['trigger_id']
            trigger = karborclient.trigger_get(self.request, trigger_id)
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve trigger details.'),
                redirect=reverse("horizon:karbor:triggers:index"))
        return trigger
