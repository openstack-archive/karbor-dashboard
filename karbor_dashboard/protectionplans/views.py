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

import json
import uuid

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import tables as horizon_tables
from horizon.utils import memoized
from horizon import views as horizon_views

from karbor_dashboard.api import karbor as karborclient
from karbor_dashboard.protectionplans import forms
from karbor_dashboard.protectionplans import tables
from karborclient.v1 import protectables


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
            plans, self._more, self._prev = karborclient.plan_list_paged(
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
        providers = {}
        try:
            providers = {provider.id: provider.name
                         for provider in karborclient.provider_list(request)}
        except Exception:
            pass

        for plan in plans:
            provider_id = plan.provider_id
            plan.provider_name = providers.get(provider_id, provider_id)

        return plans


class CreateView(horizon_forms.ModalFormView):
    template_name = 'protectionplans/create.html'
    modal_header = _("Create Protection Plan")
    form_id = "create_protectionplan_form"
    form_class = forms.CreateProtectionPlanForm
    submit_label = _("Create Protection Plan")
    submit_url = reverse_lazy("horizon:karbor:protectionplans:create")
    success_url = reverse_lazy('horizon:karbor:protectionplans:index')
    page_title = _("Create Protection Plan")

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context["instances"] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['next_view'] = ScheduleProtectView
        return kwargs

    @memoized.memoized_method
    def get_object(self):
        try:
            instances = karborclient.protectable_list_instances(
                self.request, "OS::Keystone::Project")
            results = []
            self.get_results(instances, None, results)
            return results
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to create protection plan.'),
                redirect=reverse("horizon:karbor:protectionplans:index"))

    def get_results(self, instances, showparentid, results):
        for instance in instances:
            if instance is not None:
                resource = {}
                resource["id"] = instance.id
                resource["type"] = instance.type
                resource["name"] = instance.name
                resource["showid"] = str(uuid.uuid4())
                resource["showparentid"] = showparentid
                result = protectables.Instances(self, resource)
                results.append(result)

                for dependent_resource in instance.dependent_resources:
                    if dependent_resource is not None:
                        dependent = karborclient.protectable_get_instance(
                            self.request,
                            dependent_resource["type"],
                            dependent_resource["id"])
                        self.get_results([dependent], result.showid, results)


class UpdateView(horizon_forms.ModalFormView):
    template_name = 'protectionplans/update.html'
    modal_header = _("Update Protection Plan")
    form_id = "update_protectionplan_form"
    form_class = forms.UpdateProtectionPlanForm
    submit_label = _("Update Protection Plan")
    submit_url = "horizon:karbor:protectionplans:update"
    success_url = reverse_lazy('horizon:karbor:protectionplans:index')
    page_title = _("Update Protection Plan")

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["instances"] = self.get_protectable_objects()
        args = (self.kwargs['plan_id'],)
        context['submit_url'] = reverse(self.submit_url, args=args)
        return context

    @memoized.memoized_method
    def get_protectable_objects(self):
        try:
            instances = karborclient.protectable_list_instances(
                self.request, "OS::Keystone::Project")
            results = []
            self.get_results(instances, None, results)
            return results
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve protection resources.'),
                redirect=reverse("horizon:karbor:protectionplans:index"))

    def get_results(self, instances, showparentid, results):
        for instance in instances:
            if instance is not None:
                resource = {}
                resource["id"] = instance.id
                resource["type"] = instance.type
                resource["name"] = instance.name
                resource["showid"] = str(uuid.uuid4())
                resource["showparentid"] = showparentid
                result = protectables.Instances(self, resource)
                results.append(result)

                for dependent_resource in instance.dependent_resources:
                    if dependent_resource is not None:
                        dependent = karborclient.protectable_get_instance(
                            self.request,
                            dependent_resource["type"],
                            dependent_resource["id"])
                        self.get_results([dependent], result.showid, results)

    @memoized.memoized_method
    def get_plan_object(self, *args, **kwargs):
        plan_id = self.kwargs['plan_id']
        try:
            return karborclient.plan_get(self.request, plan_id)
        except Exception:
            redirect = reverse("horizon:karbor:protectionplans:index")
            msg = _('Unable to retrieve protection plan details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    @memoized.memoized_method
    def get_provider_object(self, provider_id):
        try:
            return karborclient.provider_get(self.request, provider_id)
        except Exception:
            redirect = reverse("horizon:karbor:protectionplans:index")
            msg = _('Unable to retrieve provider details.')
            exceptions.handle(self.request, msg, redirect=redirect)

    def get_initial(self):
        initial = super(UpdateView, self).get_initial()
        plan = self.get_plan_object()
        provider = self.get_provider_object(plan.provider_id)
        initial.update({'plan_id': self.kwargs['plan_id'],
                        'name': getattr(plan, 'name', ''),
                        'plan': json.dumps(plan._info),
                        'provider': json.dumps(provider._info)})
        return initial


class ScheduleProtectView(horizon_forms.ModalFormView):
    template_name = 'protectionplans/scheduleprotect.html'
    modal_header = _("Schedule Protect")
    form_id = "scheduleprotect_form"
    form_class = forms.ScheduleProtectForm
    submit_label = _("Schedule Protect")
    submit_url = "horizon:karbor:protectionplans:scheduleprotect"
    success_url = reverse_lazy('horizon:karbor:protectionplans:index')
    page_title = _("Schedule Protect")

    @memoized.memoized_method
    def get_object(self):
        try:
            return karborclient.plan_get(self.request, self.kwargs['plan_id'])
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to schedule protect.'),
                redirect=reverse("horizon:karbor:protectionplans:index"))

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


class DetailView(horizon_views.HorizonTemplateView):
    template_name = 'protectionplans/detail.html'
    page_title = "{{ plan.name }}"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        plan = self.get_data()
        table = tables.ProtectionPlansTable(self.request)
        context["plan"] = plan
        context["provider"] = self.get_provider(plan.provider_id)
        context["instances"] = self.get_instances(plan.resources)
        context["url"] = reverse("horizon:karbor:protectionplans:index")
        context["actions"] = table.render_row_actions(plan)
        return context

    @memoized.memoized_method
    def get_data(self):
        try:
            return karborclient.plan_get(self.request, self.kwargs['plan_id'])
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve protection plan details.'),
                redirect=reverse("horizon:karbor:protectionplans:index"))

    @memoized.memoized_method
    def get_provider(self, provider_id):
        provider = None
        if provider_id:
            try:
                provider = karborclient.provider_get(self.request, provider_id)
            except Exception:
                exceptions.handle(
                    self.request,
                    _('Unable to retrieve protection provider details.'),
                    redirect=reverse("horizon:karbor:protectionplans:index"))
        return provider

    @memoized.memoized_method
    def get_instances(self, instances):
        try:
            result = []
            for instance in instances:
                instance["showid"] = str(uuid.uuid4())
                result.append(protectables.Instances(self, instance))
                detail_instance = karborclient.protectable_get_instance(
                    self.request,
                    instance["type"].strip(),
                    instance["id"].strip())
                if detail_instance.dependent_resources:
                    for dependent in detail_instance.dependent_resources:
                        dependent["showid"] = str(uuid.uuid4())
                        dependent["showparentid"] = instance["showid"]
                        result.append(
                            protectables.Instances(self, dependent))
            return result

        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to get instances.'),
                redirect=reverse("horizon:karbor:protectionplans:index"))
