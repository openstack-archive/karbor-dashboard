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

from django import forms
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import messages

import json
from karbor_dashboard.api import karbor as karborclient

STATUS_CHOICE = [("suspended", "suspended"),
                 ("started", "started")]


class CreateProtectionPlanForm(horizon_forms.SelfHandlingForm):
    name = forms.CharField(label=_("Name"))
    provider_id = forms.ChoiceField(label=_('Protection Provider'),
                                    choices=[],
                                    widget=forms.Select(attrs={
                                        'class': 'switchable'}))
    providers = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "providers"}))
    actionmode = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "actionmode"}))
    resources = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "resources"}))
    parameters = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "parameters"}))

    def __init__(self, request, *args, **kwargs):
        self.next_view = kwargs.pop('next_view')
        super(CreateProtectionPlanForm, self).\
            __init__(request, *args, **kwargs)

        result = []
        providers = karborclient.provider_list(request)

        self.fields['providers'].initial = \
            json.dumps([f._info for f in providers])

        if providers:
            result = [(e.id, e.name) for e in providers]

        self.fields['provider_id'].choices = result

    def handle(self, request, data):
        try:
            new_plan = karborclient.plan_create(request,
                                                data["name"],
                                                data["provider_id"],
                                                json.loads(data["resources"]),
                                                json.loads(data["parameters"]))

            messages.success(request,
                             _("Protection Plan created successfully."))

            if data["actionmode"] == "schedule":
                request.method = 'GET'
                return self.next_view.as_view()(request,
                                                plan_id=new_plan.id)
            elif data["actionmode"] == "now":
                karborclient.checkpoint_create(request, new_plan.provider_id,
                                               new_plan.id)
                messages.success(request, _("Protect now successfully."))
            return new_plan
        except Exception:
            exceptions.handle(request, _('Unable to create protection plan.'))


class UpdateProtectionPlanForm(horizon_forms.SelfHandlingForm):
    name = forms.CharField(label=_("Name"), max_length=255, required=False)
    status = forms.ChoiceField(label=_('Status'),
                               choices=STATUS_CHOICE,
                               widget=forms.Select(attrs={
                                   'class': 'switchable'}))
    plan = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "plan"}))
    provider = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "provider"}))
    resources = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "resources"}))
    parameters = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "parameters"}))

    def handle(self, request, data):
        plan_id = self.initial['plan_id']
        status = data["status"]
        data_ = {"status": status}

        name = data["name"]
        if name:
            data_.update({"name": name})

        resources = json.loads(data["resources"])
        if resources:
            resources_ = []
            for resource in resources:
                if resource not in resources_:
                    resources_.append(resource)
            data_.update({"resources": resources_})

        try:
            new_plan = karborclient.plan_update(request,
                                                plan_id,
                                                data_)
            messages.success(request,
                             _("Protection Plan updated successfully."))
            return new_plan
        except Exception as e:
            msg = _('Unable to update protection plan. ') + e.message
            exceptions.handle(request, msg)


class ScheduleProtectForm(horizon_forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    name = forms.CharField(label=_("Name"), widget=forms.HiddenInput)
    provider_id = forms.CharField(label=_("Provider ID"),
                                  widget=forms.HiddenInput)
    trigger_id = horizon_forms.DynamicChoiceField(
        label=_("Associate with Trigger"),
        add_item_link="horizon:karbor:triggers:create")

    def __init__(self, request, *args, **kwargs):
        super(ScheduleProtectForm, self).__init__(request, *args, **kwargs)

        result = []
        triggers = karborclient.trigger_list(request)
        if triggers:
            result = [(e.id, e.name) for e in triggers]

        self.fields['trigger_id'].choices = result

    def handle(self, request, data):
        try:
            operation_definition = dict(provider_id=data["provider_id"],
                                        plan_id=data["id"])
            karborclient.scheduled_operation_create(request,
                                                    data["name"],
                                                    "protect",
                                                    data["trigger_id"],
                                                    operation_definition)
            messages.success(request, _("Schedule protect successfully."))
            return True
        except Exception:
            exceptions.handle(request, _('Unable to schedule protect.'))
