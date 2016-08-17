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
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import tables

from karbor_dashboard.api import karbor as karborclient


class RestoreCheckpointLink(tables.LinkAction):
    name = "restore"
    verbose_name = _("Restore Checkpoint")
    url = "horizon:karbor:checkpoints:restore"
    classes = ("ajax-modal",)
    icon = "plus"

    def get_link_url(self, checkpoint):
        checkpoint_id = checkpoint.id
        return reverse(self.url, args=(checkpoint.provider_id, checkpoint_id))

    def allowed(self, request, checkpoint):
        return True


class DeleteCheckpointsAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(u"Delete Checkpoint",
                              u"Delete Checkpoints",
                              count)

    @staticmethod
    def action_past(count):
        return ungettext_lazy(u"Deleted Checkpoint",
                              u"Deleted Checkpoints",
                              count)

    def allowed(self, request, checkpoint):
        return True

    def delete(self, request, obj_id):
        datum = self.table.get_object_by_id(obj_id)
        provider_id = datum.provider_id
        karborclient.checkpoint_delete(request,
                                       provider_id=provider_id,
                                       checkpoint_id=obj_id)


def get_provider_link(checkpoint):
    """url Two args"""
    return reverse("horizon:karbor:checkpoints:detail",
                   args=(checkpoint.provider_id, checkpoint.id))


def get_plan_name(obj):
    name = ""
    plan = getattr(obj, 'protection_plan')
    if plan is not None:
        name = plan.get("name")
    return name


class CheckpointsTable(tables.DataTable):
    checkpointId = tables.Column(
        "id",
        link=get_provider_link,
        verbose_name=_('Checkpoint ID'))
    protectionProvider = tables.Column(
        "provider_name",
        verbose_name=_('Protection Provider'))
    protectPlan = tables.Column(
        get_plan_name,
        verbose_name=_('Protection Plan'))
    status = tables.Column(
        'status',
        verbose_name=_('Status'))

    class Meta(object):
        name = 'checkpoints'
        verbose_name = _('Checkpoints')
        row_actions = (RestoreCheckpointLink, DeleteCheckpointsAction)


class DetailTable(tables.DataTable):

    class Meta(object):
        name = "protectionresources"
        verbose_name = _("Protection Resources")
        hidden_title = False
