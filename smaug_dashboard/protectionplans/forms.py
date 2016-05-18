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

from smaug_dashboard.api import smaug as smaugclient


class ScheduleProtectForm(horizon_forms.SelfHandlingForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    name = forms.CharField(label=_("Name"), widget=forms.HiddenInput)
    provider_id = forms.CharField(label=_("Provider ID"),
                                  widget=forms.HiddenInput)
    trigger_id = horizon_forms.DynamicChoiceField(
        label=_("Associate with Trigger"),
        add_item_link="horizon:smaug:triggers:create")

    def __init__(self, request, *args, **kwargs):
        super(ScheduleProtectForm, self).__init__(request, *args, **kwargs)

        result = []
        triggers = smaugclient.trigger_list(request)
        if triggers:
            result = [(e.id, e.name) for e in triggers]

        self.fields['trigger_id'].choices = result

    def handle(self, request, data):
        try:
            operation_definition = dict(provider_id=data["provider_id"],
                                        plan_id=data["id"])
            smaugclient.scheduled_operation_create(request,
                                                   data["name"],
                                                   "protect",
                                                   data["trigger_id"],
                                                   operation_definition)
            messages.success(request, _("Schedule protect successfully."))
            return True
        except Exception:
            exceptions.handle(request, _('Unable to schedule protect.'))
