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
from django.utils.translation import pgettext_lazy
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
        return checkpoint.status == 'available'


class DeleteCheckpointsAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ungettext_lazy(u"Delete Checkpoint",
                              u"Delete Checkpoints",
                              count)

    @staticmethod
    def action_past(count):
        return ungettext_lazy(u"Scheduled deletion of Checkpoint",
                              u"Scheduled deletion of Checkpoints",
                              count)

    def allowed(self, request, checkpoint):
        return checkpoint.status == 'available'

    def delete(self, request, obj_id):
        datum = self.table.get_object_by_id(obj_id)
        provider_id = datum.provider_id
        karborclient.checkpoint_delete(request,
                                       provider_id=provider_id,
                                       checkpoint_id=obj_id)


def get_provider_link(obj):
    return reverse('horizon:karbor:protectionproviders:detail',
                   args=(obj.provider_id, ))


def get_checkpoint_link(obj):
    """url Two args"""
    return reverse("horizon:karbor:checkpoints:detail",
                   args=(obj.provider_id, obj.id))


def get_plan_name(obj):
    name = ""
    plan = getattr(obj, 'protection_plan')
    if plan is not None:
        name = plan.get("name")
    return name


class UpdateRow(tables.Row):
    ajax = True

    def __init__(self, table, datum=None):
        super(UpdateRow, self).__init__(table, datum)
        self.provider_id = getattr(table, 'provider_id')

    def get_data(self, request, obj_id):
        provider = karborclient.provider_get(request, self.provider_id)
        checkpoint = karborclient.checkpoint_get(request,
                                                 self.provider_id,
                                                 obj_id)
        setattr(checkpoint, "provider_name", provider.name)
        setattr(checkpoint, "provider_id", provider.id)
        return checkpoint


TASK_DISPLAY_CHOICES = (
    ("error", pgettext_lazy("Task status of an Checkpoint", u"Error")),
    ("protecting", pgettext_lazy("Task status of an Checkpoint",
                                 u"Protecting")),
    ("available", pgettext_lazy("Task status of an Checkpoint", u"Available")),
    ("deleting", pgettext_lazy("Task status of an Checkpoint", u"Deleting")),
    ("deleted", pgettext_lazy("Task status of an Checkpoint", u"Deleted")),
    ("error-deleting", pgettext_lazy("Task status of an Checkpoint",
                                     u"Error Deleting")),
)


class CheckpointsTable(tables.DataTable):
    TASK_STATUS_CHOICES = (
        ("error", False),
        ("available", True),
        ("deleted", True),
        ("error-deleting", False),
    )
    checkpointId = tables.Column(
        "id",
        link=get_checkpoint_link,
        verbose_name=_('Checkpoint ID'))
    protectionProvider = tables.Column(
        "provider_name",
        link=get_provider_link,
        verbose_name=_('Protection Provider'))
    protectPlan = tables.Column(
        get_plan_name,
        verbose_name=_('Protection Plan'))
    status = tables.Column(
        'status',
        verbose_name=_('Status'),
        status=True,
        status_choices=TASK_STATUS_CHOICES,
        display_choices=TASK_DISPLAY_CHOICES)

    class Meta(object):
        name = 'checkpoints'
        verbose_name = _('Checkpoints')
        status_columns = ["status", ]
        row_class = UpdateRow
        row_actions = (RestoreCheckpointLink, DeleteCheckpointsAction)


class DetailTable(tables.DataTable):

    class Meta(object):
        name = "protectionresources"
        verbose_name = _("Protection Resources")
        hidden_title = False
