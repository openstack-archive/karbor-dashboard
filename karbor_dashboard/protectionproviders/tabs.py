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

from horizon import exceptions
from horizon import tabs

from karbor_dashboard.api import karbor as karborclient
import simplejson as json


class OptionsSchemaTab(tabs.Tab):
    name = _("Options Schema")
    slug = "optionsschema"
    template_name = "protectionproviders/_schema_contents.html"

    def get_context_data(self, request):
        try:
            provider_id = self.tab_group.kwargs['provider_id']
            provider = karborclient.provider_get(request, provider_id)

            schema = {}
            if provider is not None:
                if 'options_schema' in provider.extended_info_schema:
                    schema = provider.extended_info_schema['options_schema']

            return {"schema_contents": json.dumps(schema, indent=4)}
        except Exception:
            msg = _('Unable to retrieve provider contents.')
            exceptions.handle(request, msg)
            return None


class RestoreSchemaTab(tabs.Tab):
    name = _("Restore Schema")
    slug = "restoreschema"
    template_name = "protectionproviders/_schema_contents.html"

    def get_context_data(self, request):
        try:
            provider_id = self.tab_group.kwargs['provider_id']
            provider = karborclient.provider_get(request, provider_id)

            schema = {}
            if provider is not None:
                if 'restore_schema' in provider.extended_info_schema:
                    schema = provider.extended_info_schema['restore_schema']

            return {"schema_contents": json.dumps(schema, indent=4)}
        except Exception:
            msg = _('Unable to retrieve provider contents.')
            exceptions.handle(request, msg)
            return None


class SavedInfoSchemaTab(tabs.Tab):
    name = _("Saved Info Schema")
    slug = "savedinfoschema"
    template_name = "protectionproviders/_schema_contents.html"

    def get_context_data(self, request):
        try:
            provider_id = self.tab_group.kwargs['provider_id']
            provider = karborclient.provider_get(request, provider_id)
            schema = {}
            if provider is not None:
                if 'saved_info_schema' in provider.extended_info_schema:
                    schema = provider.extended_info_schema['saved_info_schema']

            return {"schema_contents": json.dumps(schema, indent=4)}
        except Exception:
            msg = _('Unable to retrieve provider contents.')
            exceptions.handle(request, msg)
            return None


class ProviderDetailTabs(tabs.TabGroup):
    slug = "provider_details"
    tabs = (OptionsSchemaTab, RestoreSchemaTab, SavedInfoSchemaTab)
