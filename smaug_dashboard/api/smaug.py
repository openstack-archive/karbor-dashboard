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
from horizon.utils import functions as utils
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


def update_pagination(entities, page_size, marker, sort_dir, sort_key,
                      reversed_order):
    has_more_data = has_prev_data = False
    if len(entities) > page_size:
        has_more_data = True
        entities.pop()
        if marker is not None:
            has_prev_data = True
    # first page condition when reached via prev back
    elif reversed_order and marker is not None:
        has_more_data = True
    # last page condition
    elif marker is not None:
        has_prev_data = True

    # restore the original ordering here
    if reversed_order:
        entities = sorted(entities, key=lambda entity:
                          (getattr(entity, sort_key) or '').lower(),
                          reverse=(sort_dir == 'asc'))

    return entities, has_more_data, has_prev_data


def plan_create(request, name, provider_id, resources):
    return smaugclient(request).plans.create(name, provider_id, resources)


def plan_delete(request, plan_id):
    return smaugclient(request).plans.delete(plan_id)


def plan_update(request, plan_id, data):
    return smaugclient(request).plans.update(plan_id, data)


def plan_list(request, detailed=False, search_opts=None, marker=None,
              limit=None, sort_key=None, sort_dir=None, sort=None):
    return smaugclient(request).plans.list(detailed=detailed,
                                           search_opts=search_opts,
                                           marker=marker,
                                           limit=limit,
                                           sort_key=sort_key,
                                           sort_dir=sort_dir,
                                           sort=sort)


def plan_list_paged(request, detailed=False, search_opts=None, marker=None,
                    limit=None, sort_key=None, sort_dir=None, sort=None,
                    paginate=False, reversed_order=False):
    has_more_data = False
    has_prev_data = False

    if paginate:
        if reversed_order:
            sort_dir = 'desc' if sort_dir == 'asc' else 'asc'
        page_size = utils.get_page_size(request)
        plans = smaugclient(request).plans.list(detailed=detailed,
                                                search_opts=search_opts,
                                                marker=marker,
                                                limit=page_size + 1,
                                                sort_key=sort_key,
                                                sort_dir=sort_dir,
                                                sort=sort)
        plans, has_more_data, has_prev_data = update_pagination(
            plans, page_size, marker, sort_dir, sort_key, reversed_order)
    else:
        plans = smaugclient(request).plans.list(detailed=detailed,
                                                search_opts=search_opts,
                                                marker=marker,
                                                limit=limit,
                                                sort_key=sort_key,
                                                sort_dir=sort_dir,
                                                sort=sort)
    return (plans, has_more_data, has_prev_data)


def plan_get(request, plan_id):
    return smaugclient(request).plans.get(plan_id)
