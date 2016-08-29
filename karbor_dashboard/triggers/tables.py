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

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables

from karbor_dashboard.api import karbor as karborclient


class CreateTriggerLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Trigger")
    url = "horizon:karbor:triggers:create"
    classes = ("ajax-modal",)
    icon = "plus"

    def allowed(self, request, trigger):
        return True


class DeleteTriggersAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(u"Delete Trigger",
                              u"Delete Triggers",
                              count)

    @staticmethod
    def action_past(count):
        return ungettext_lazy(u"Deleted Trigger",
                              u"Deleted Triggers",
                              count)

    def allowed(self, request, trigger):
        return True

    def delete(self, request, obj_id):
        karborclient.trigger_delete(request, obj_id)


class TriggerFilterAction(tables.FilterAction):
    def filter(self, table, triggers, filter_string):
        """Naive case-insensitive search."""
        query = filter_string.lower()
        return [trigger for trigger in triggers
                if query in trigger.name.lower()]


class TriggersTable(tables.DataTable):
    name = tables.Column('name',
                         link="horizon:karbor:triggers:detail",
                         verbose_name=_('Name'))
    type = tables.Column('type',
                         verbose_name=_('Type'))

    class Meta(object):
        name = 'triggers'
        verbose_name = _('Triggers')
        row_actions = (DeleteTriggersAction,)
        table_actions = (TriggerFilterAction, CreateTriggerLink,
                         DeleteTriggersAction)
