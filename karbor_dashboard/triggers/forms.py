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

from karbor_dashboard.api import karbor as karborclient
from karbor_dashboard.triggers import utils


class CreateTriggerForm(horizon_forms.SelfHandlingForm):
    name = forms.CharField(label=_("Name"))
    type = forms.ChoiceField(label=_("Type"),
                             choices=utils.TRIGGERTYPE_CHOICES,
                             widget=horizon_forms.Select(attrs={
                                 'class': 'switchable',
                                 'data-slug': 'source',
                                 'disabled': 'disabled'
                             }))
    frequence = forms.ChoiceField(
        label=_('Frequence'),
        choices=utils.FREQUENCE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'switchable switched',
            'data-slug': 'frequence'}))
    day = forms.ChoiceField(
        label=_("Day"),
        required=False,
        widget=horizon_forms.Select(attrs={
            'class': 'switched',
            'data-switch-on': 'frequence',
            'data-frequence-everyweek': _('Day')}))
    date = forms.ChoiceField(
        label=_("Date"),
        required=False,
        widget=horizon_forms.Select(attrs={
            'class': 'switched',
            'data-switch-on': 'frequence',
            'data-frequence-everymonth': _('Date')}))
    time = forms.TimeField(
        label=_('Execution Time (HH:MM)'),
        input_formats=("%H:%M",),
        initial="00:00")

    def __init__(self, request, *args, **kwargs):
        super(CreateTriggerForm, self).__init__(request, *args, **kwargs)

        self.fields['day'].choices = utils.DAY_CHOICES
        self.fields['date'].choices = [(e, e) for e in range(1, 31 + 1)]

    def handle(self, request, data):
        try:
            data_properties = utils.CrontabUtil.convert_to_crontab(data)
            new_trigger = karborclient.trigger_create(request,
                                                      data["name"],
                                                      data["type"],
                                                      data_properties)
            messages.success(request, _("Trigger created successfully."))

            return new_trigger
        except Exception:
            exceptions.handle(request, _('Unable to create trigger.'))
            return False
