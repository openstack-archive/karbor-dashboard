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

from __future__ import absolute_import
import logging
import six.moves.urllib.parse as urlparse

from django.conf import settings
from horizon import exceptions
from horizon.utils.memoized import memoized
from openstack_dashboard.api import base
from smaugclient.v1 import client as smaug_client

LOG = logging.getLogger(__name__)


def get_smaug_endpoint(request):
    endpoint = ""
    try:
        endpoint = base.url_for(request, "data-protect")
        parts = urlparse.urlparse(endpoint)
        if parts.scheme and parts.netloc:
            endpoint = '%s://%s' % (parts.scheme, parts.netloc)
    except exceptions.ServiceCatalogException:
        endpoint = 'http://localhost:8799'
        LOG.warning('Smaug API location could not be found in Service '
                    'Catalog, using default: {0}'.format(endpoint))
    return endpoint


@memoized
def smaugclient(request):
    endpoint = get_smaug_endpoint(request)
    LOG.debug('smaugclient connection created using the token "%s" and url'
              '"%s"' % (request.user.token.id, endpoint))
    c = smaug_client.Client(endpoint=endpoint,
                            auth_url=getattr(settings,
                                             'OPENSTACK_KEYSTONE_URL'),
                            token=request.user.token.id,
                            username=request.user.username,
                            project_id=request.user.tenant_id,
                            auth_plugin='token',
                            )
    return c
