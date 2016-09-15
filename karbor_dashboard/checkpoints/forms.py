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
from django.views.decorators.debug import sensitive_variables  # noqa

from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import messages

import json
from karbor_dashboard.api import karbor as karborclient


class RestoreCheckpointForm(horizon_forms.SelfHandlingForm):
    provider_id = forms.CharField(label=_("Provider ID"),
                                  widget=forms.HiddenInput(),
                                  required=False)
    checkpoint_id = forms.CharField(label=_("Checkpoint ID"),
                                    widget=forms.HiddenInput(),
                                    required=False)
    restore_target = forms.CharField(label=_("Restore Target"))
    restore_target_username = forms.CharField(
        label=_("Restore Target Username"))
    restore_target_password = forms.CharField(
        label=_("Restore Target Password"),
        widget=forms.PasswordInput())
    provider = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "provider"}))
    parameters = forms.CharField(
        widget=forms.HiddenInput(attrs={"class": "parameters"}))
    failure_url = 'horizon:karbor:checkpoints:index'

    def __init__(self, request, *args, **kwargs):
        super(RestoreCheckpointForm, self).\
            __init__(request, *args, **kwargs)

        provider_id = str(kwargs["initial"]["provider_id"])
        provider = karborclient.provider_get(request, provider_id)
        self.fields['provider'].initial = json.dumps(provider._info)

    @sensitive_variables('restore_target_password')
    def handle(self, request, data):
        try:
            data_parameters = json.loads(data["parameters"])
            restore_auth = {
                "type": "password",
                "username": data["restore_target_username"],
                "password": data["restore_target_password"],
            }
            new_restore = karborclient.restore_create(
                request,
                provider_id=data["provider_id"],
                checkpoint_id=data["checkpoint_id"],
                restore_target=data["restore_target"],
                parameters=data_parameters,
                restore_auth=restore_auth)
            messages.success(request, _("Checkpoint restore initiated"))
            return new_restore
        except Exception:
            exceptions.handle(request, _('Unable to restore checkpoint.'))
