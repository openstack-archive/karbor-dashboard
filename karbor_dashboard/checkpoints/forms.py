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

EMPTY_VALUES = (None, '', u'', [], (), {})


class RestoreCheckpointForm(horizon_forms.SelfHandlingForm):
    provider_id = forms.CharField(label=_("Provider ID"),
                                  widget=forms.HiddenInput(),
                                  required=False)
    checkpoint_id = forms.CharField(label=_("Checkpoint ID"),
                                    widget=forms.HiddenInput(),
                                    required=False)
    use_current_session = forms.BooleanField(
        label=_("Use current session credentials"),
        widget=forms.CheckboxInput(attrs={
            'class': 'disable_input',
            'data-slug': 'use_current_session',
            'data-disable-on-checked': 'true',
            'checked': 'checked'
        }),
        initial=False,
        required=False)
    restore_target = forms.URLField(
        label=_("Restore Target"),
        widget=forms.URLInput(attrs={
            'class': 'disabled_input',
            'data-disable-on': 'use_current_session',
            'data-source-manual': _("Restore Target"),
            'disabled': 'disabled',
            'value': 'Target: Current project'
        }),
        required=False)
    restore_target_username = forms.CharField(
        label=_("Restore Target Username"),
        widget=forms.TextInput(attrs={
            'class': 'disabled_input',
            'data-disable-on': 'use_current_session',
            'data-source-manual': _("Restore Target Username"),
            'disabled': 'disabled',
            'value': 'Target Username: current user'
        }),
        required=False)
    restore_target_password = forms.CharField(
        label=_("Restore Target Password"),
        widget=forms.PasswordInput(attrs={
            'class': 'disabled_input',
            'data-disable-on': 'use_current_session',
            'data-source-manual': _("Restore Target Password"),
            'disabled': 'disabled',
            'hidden': 'hidden'
        }),
        required=False)
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
        def all_empty(data_list):
            return all(map(lambda x: x in EMPTY_VALUES, data_list))

        def all_not_empty(data_list):
            return all(map(lambda x: x not in EMPTY_VALUES, data_list))

        def empty_to_none(data_):
            return data_ if data_ not in EMPTY_VALUES else None

        target = empty_to_none(data["restore_target"])
        target_username = empty_to_none(data["restore_target_username"])
        target_password = empty_to_none(data["restore_target_password"])
        use_current_session = empty_to_none(data["use_current_session"])

        if not use_current_session:
            validate_data = [target, target_username, target_password]
            if not (all_empty(validate_data) or all_not_empty(validate_data)):
                messages.warning(request,
                                 _('Restore Target, Restore Target Username '
                                   'and Restore Target Password must be '
                                   'assigned at the same time or not '
                                   'assigned.'))
                return False

        try:
            data_parameters = json.loads(data["parameters"])
            restore_auth = {
                "type": "password",
                "username": target_username,
                "password": target_password,
            }
            new_restore = karborclient.restore_create(
                request,
                provider_id=data["provider_id"],
                checkpoint_id=data["checkpoint_id"],
                restore_target=target,
                parameters=data_parameters,
                restore_auth=restore_auth)
            messages.success(request, _("Checkpoint restore initiated"))
            return new_restore
        except Exception:
            exceptions.handle(request, _('Unable to restore checkpoint.'))
