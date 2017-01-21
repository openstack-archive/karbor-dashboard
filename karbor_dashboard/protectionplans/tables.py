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
from django import http
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import exceptions
from horizon import messages
from horizon import tables

from karbor_dashboard.api import karbor as karborclient


class CreateProtectionPlanLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Protection Plan")
    url = "horizon:karbor:protectionplans:create"
    classes = ("ajax-modal",)
    icon = "plus"

    def allowed(self, request, protectionplan):
        return True


class ScheduleProtectLink(tables.LinkAction):
    name = "scheduleprotect"
    verbose_name = _("Schedule Protect")
    url = "horizon:karbor:protectionplans:scheduleprotect"
    classes = ("ajax-modal",)

    def allowed(self, request, plan):
        return True


class EditPlanLink(tables.LinkAction):
    name = "editplan"
    verbose_name = _("Edit Plan")
    url = "horizon:karbor:protectionplans:update"
    classes = ("ajax-modal",)

    def allowed(self, request, protectionplan):
        return True


class ProtectNowLink(tables.Action):
    name = "protectnow"
    verbose_name = _("Protect Now")

    def allowed(self, request, protectionplan):
        return True

    def single(self, table, request, obj_id):
        try:
            datum = self.table.get_object_by_id(obj_id)
            provider_id = datum.provider_id
            karborclient.checkpoint_create(request, provider_id, obj_id)
            messages.success(request, _("Plan protection initiated"))
            redirect = reverse("horizon:karbor:checkpoints:index",
                               args=(provider_id,))
            return http.HttpResponseRedirect(redirect)
        except Exception:
            exceptions.handle(request, _('Unable to protect now'))


class DeleteProtectionPlansAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete Protection Plan",
            u"Delete Protection Plans",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Delete Protection Plan",
            u"Delete Protection Plans",
            count
        )

    def allowed(self, request, protectionplan):
        return True

    def delete(self, request, obj_id):
        karborclient.plan_delete(request, obj_id)


class ProtectionPlanFilterAction(tables.FilterAction):
    def filter(self, table, protectionplans, filter_string):
        """Naive case-insensitive search."""
        query = filter_string.lower()
        return [protectionplan for protectionplan in protectionplans
                if query in protectionplan.name.lower()]


def provider_link(plan):
    return reverse('horizon:karbor:protectionproviders:detail',
                   args=(plan.provider_id, ))


class ProtectionPlansTable(tables.DataTable):
    name = tables.Column('name',
                         link="horizon:karbor:protectionplans:detail",
                         verbose_name=_('Name'))

    provider = tables.Column('provider_name',
                             link=provider_link,
                             verbose_name=_('Protection Provider'))

    status = tables.Column('status',
                           verbose_name=_('Status'))

    class Meta(object):
        name = 'protectionplans'
        verbose_name = _('Protection Plans')
        row_actions = (ScheduleProtectLink, EditPlanLink, ProtectNowLink,
                       DeleteProtectionPlansAction)
        table_actions = (ProtectionPlanFilterAction, CreateProtectionPlanLink,
                         DeleteProtectionPlansAction)


class DetailTable(tables.DataTable):
    id = tables.Column("id", verbose_name=_("ID"))
    type = tables.Column("type", verbose_name=_("TYPE"))

    class Meta(object):
        name = "protectionresources"
        verbose_name = _("Protection Resources")
        hidden_title = False
