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

from smaug_dashboard.api import smaug as smaugclient
from smaug_dashboard.protectionplans import forms
from smaug_dashboard.protectionplans import tables


class IndexView(horizon_tables.DataTableView):
    table_class = tables.ProtectionPlansTable
    template_name = 'protectionplans/index.html'
    page_title = _("Protection Plans")

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        request = self.request
        prev_marker = request.GET.get(
            tables.ProtectionPlansTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = request.GET.get(
                tables.ProtectionPlansTable._meta.pagination_param, None)
        reversed_order = prev_marker is not None
        plans = []
        try:
            plans, self._more, self._prev = smaugclient.plan_list_paged(
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
                              _('Unable to retrieve protection plans list.'))
        return plans


class ScheduleProtectView(horizon_forms.ModalFormView):
    template_name = 'protectionplans/scheduleprotect.html'
    modal_header = _("Schedule Protect")
    form_id = "scheduleprotect_form"
    form_class = forms.ScheduleProtectForm
    submit_label = _("Schedule Protect")
    submit_url = "horizon:smaug:protectionplans:scheduleprotect"
    success_url = reverse_lazy('horizon:smaug:protectionplans:index')
    page_title = _("Schedule Protect")

    @memoized.memoized_method
    def get_object(self):
        try:
            return smaugclient.plan_get(self.request, self.kwargs['plan_id'])
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to schedule protect.'),
                redirect=reverse("horizon:smaug:protectionplans:index"))

    def get_context_data(self, **kwargs):
        context = super(ScheduleProtectView, self).get_context_data(**kwargs)
        args = (self.get_object().id,)
        context["plan"] = self.get_object()
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    def get_initial(self):
        plan = self.get_object()
        return {'id': plan.id,
                'name': plan.name,
                'provider_id': plan.provider_id}
