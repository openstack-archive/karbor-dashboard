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

from horizon import tables


class ShowCheckpointsAction(tables.Action):
    name = "checkpoints"
    verbose_name = _("Show Checkpoints")

    def allowed(self, request, provider):
        return True

    def single(self, table, request, obj_id):
        redirect = reverse("horizon:karbor:checkpoints:index",
                           args=(obj_id,))
        return http.HttpResponseRedirect(redirect)


class ProtectionProviderFilterAction(tables.FilterAction):
    def filter(self, table, protectionproviders, filter_string):
        """Naive case-insensitive search."""
        query = filter_string.lower()
        return [protectionprovider
                for protectionprovider in protectionproviders
                if query in protectionprovider.name.lower()]


class ProtectionProvidersTable(tables.DataTable):
    name = tables.Column('name',
                         link="horizon:karbor:protectionproviders:detail",
                         verbose_name=_('Name'))
    description = tables.Column('description',
                                verbose_name=_('Description'))

    class Meta(object):
        name = 'protectionproviders'
        verbose_name = _('Protection Providers')
        row_actions = (ShowCheckpointsAction,)
        table_actions = (ProtectionProviderFilterAction,)
        multi_select = False
