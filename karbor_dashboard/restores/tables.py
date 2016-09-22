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

from horizon import tables


class RestoresTable(tables.DataTable):
    id = tables.Column(
        'id',
        verbose_name=_('ID'))
    name = tables.Column(
        'name',
        verbose_name=_('Protection Plan'))
    status = tables.Column(
        'status',
        verbose_name=_('Status'))
    restore_from_checkpoint = tables.Column(
        'checkpoint_id',
        verbose_name=_('Restore From Checkpoint'))
    restore_target = tables.Column(
        'restore_target',
        verbose_name=_('Restore Target'))
    protection_provider = tables.Column(
        'provider_name',
        verbose_name=_('Protection Provider'))

    class Meta(object):
        name = 'restores'
        verbose_name = _('Restores')
