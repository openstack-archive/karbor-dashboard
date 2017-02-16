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

import uuid

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from calendar import monthrange
from datetime import date
from datetime import timedelta
from horizon import exceptions
from horizon import forms as horizon_forms
from horizon import tables as horizon_tables
from horizon.utils import memoized

from karbor_dashboard.api import karbor as karborclient
from karbor_dashboard.checkpoints import forms
from karbor_dashboard.checkpoints import tables
from karbor_dashboard.checkpoints import utils
from karborclient.v1 import protectables


class IndexView(horizon_tables.DataTableView):
    table_class = tables.CheckpointsTable
    template_name = 'checkpoints/index.html'
    page_title = _("Checkpoints")

    @memoized.memoized_method
    def get_provider_list(self):
        return karborclient.provider_list(self.request)

    @memoized.memoized_method
    def get_plan_list(self):
        return karborclient.plan_list(self.request)

    @memoized.memoized_method
    def get_filter_list(self):
        filters = {}

        # Get all filter
        for key in utils.FILTER_LIST:
            filters[key] = self.request.POST.get(key, u"All")

        # Remove the "All" of provider_filter
        provider_filter = utils.FILTER_LIST[0]
        try:
            providers = self.get_provider_list()
            filters[provider_filter] = \
                self.request.POST.get(provider_filter, providers[0].id)
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve anyone provider.'))

        # Get arguments from the providers page
        if self.kwargs.get("provider_id", None) is not None:
            filters[provider_filter] = self.kwargs["provider_id"]
        return filters

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            context["provider_list"] = self.get_provider_list()
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve anyone provider.'))

        context["plan_list"] = self.get_plan_list()
        context["date_list"] = utils.DATE_CHOICES
        context["url"] = reverse("horizon:karbor:checkpoints:index")
        context = dict(context, **self.get_filter_list())
        return context

    @memoized.memoized_method
    def get_search_opts(self):
        def _total_days(year, month, num_months):
            days = 0
            i = 0
            while i < num_months:
                days += monthrange(year, month)[1]
                month = month - 1 if month > 1 else 12
                year = year if month > 1 else year - 1
                i += 1
            return days

        search_opts = {}
        filters = self.get_filter_list()
        provider_id = filters.get(utils.FILTER_LIST[0], None)
        plan_id = filters.get(utils.FILTER_LIST[1], u"All")
        if plan_id != u"All":
            search_opts["plan_id"] = plan_id

        now = date.today()
        date_filter = filters.get(utils.FILTER_LIST[2], None)
        if date_filter == utils.TODAY:
            delta = timedelta(days=1)
        elif date_filter == utils.LASTESTONEWEEK:
            delta = timedelta(weeks=1)
        elif date_filter == utils.LASTESTTWOWEEKS:
            delta = timedelta(weeks=2)
        elif date_filter == utils.LASTESTONEMONTH:
            days = _total_days(now.year, now.month, 1)
            delta = timedelta(days=days)
        elif date_filter == utils.LASTESTTHREEMONTHS:
            days = _total_days(now.year, now.month, 3)
            delta = timedelta(days=days)
        else:
            delta = None

        if delta:
            search_opts["start_date"] = now - delta
            search_opts["end_date"] = now

        return provider_id, search_opts

    def has_prev_data(self, table):
        return self._prev

    def has_more_data(self, table):
        return self._more

    def get_data(self):
        prev_marker = self.request.GET.get(
            tables.CheckpointsTable._meta.prev_pagination_param, None)

        if prev_marker is not None:
            marker = prev_marker
        else:
            marker = self.request.GET.get(
                tables.CheckpointsTable._meta.pagination_param, None)

        reversed_order = prev_marker is not None
        checkpoints = []
        try:
            # Get provider id and search_opts
            provider_id, search_opts = self.get_search_opts()
            if provider_id is None:
                raise Exception()

            checkpoints, self._more, self._prev = \
                karborclient.checkpoint_list_paged(
                    self.request,
                    provider_id=provider_id,
                    search_opts=search_opts,
                    marker=marker,
                    paginate=True,
                    sort_dir='asc',
                    sort_key='name',
                    reversed_order=reversed_order)
            provider = karborclient.provider_get(self.request, provider_id)
            for checkpoint in checkpoints:
                setattr(checkpoint, "provider_name", provider.name)
                setattr(checkpoint, "provider_id", provider_id)
        except Exception:
            self._prev = False
            self._more = False
            exceptions.handle(self.request,
                              _('Unable to retrieve checkpoints list.'))
        return checkpoints

    def get_table(self):
        super(IndexView, self).get_table()
        provider_id, _ = self.get_search_opts()
        setattr(self.table, 'provider_id', provider_id)
        return self.table


class CheckpointsRestoreView(horizon_forms.ModalFormView):
    template_name = 'checkpoints/restore.html'
    modal_header = _("Restore Checkpoint")
    form_id = "restore_checkpoint_form"
    form_class = forms.RestoreCheckpointForm
    submit_label = _("Restore Checkpoint")
    submit_url = 'horizon:karbor:checkpoints:restore'
    success_url = reverse_lazy('horizon:karbor:restores:index')
    page_title = _("Restore Checkpoint")

    def get_initial(self):
        return {"provider_id": self.kwargs['provider_id'],
                "checkpoint_id": self.kwargs['checkpoint_id']}

    def get_context_data(self, **kwargs):
            context = super(CheckpointsRestoreView, self). \
                get_context_data(**kwargs)
            provider_id = self.kwargs['provider_id']
            checkpoint_id = self.kwargs['checkpoint_id']
            context['provider_id'] = provider_id
            context['checkpoint_id'] = checkpoint_id
            context["instances"] = self.get_resources()
            context['submit_url'] = reverse(self.submit_url,
                                            args=(provider_id, checkpoint_id))
            return context

    @memoized.memoized_method
    def get_resources(self):
        results = []
        try:
            provider_id = self.kwargs['provider_id']
            checkpoint_id = self.kwargs['checkpoint_id']
            checkpoint = karborclient.checkpoint_get(self.request,
                                                     provider_id,
                                                     checkpoint_id)
            graphnodes = utils.deserialize_resource_graph(
                checkpoint.resource_graph)
            self.get_results(graphnodes, None, results)
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve checkpoint details.'),
                redirect=reverse("horizon:karbor:checkpoints:index"))
        return results

    def get_results(self, graphnodes, showparentid, results):
        for graphnode in graphnodes:
            if graphnode is not None:
                # add graph node to results
                resource = {}
                resource["id"] = graphnode.value.id
                resource["type"] = graphnode.value.type
                resource["name"] = graphnode.value.name
                resource["showid"] = str(uuid.uuid4())
                resource["showparentid"] = showparentid
                result = protectables.Instances(self, resource)
                results.append(result)
                # add child graph nodes to results
                self.get_results(graphnode.child_nodes,
                                 result.showid,
                                 results
                                 )


class DetailView(horizon_tables.DataTableView):
    table_class = tables.DetailTable
    template_name = 'checkpoints/detail.html'
    page_title = _("{{ checkpoint.protection_plan.name }}")

    @memoized.memoized_method
    def get_checkpoint_data(self):
        try:
            provider_id = self.kwargs['provider_id']
            checkpoint_id = self.kwargs['checkpoint_id']
            checkpoint = karborclient.checkpoint_get(self.request,
                                                     provider_id,
                                                     checkpoint_id)
        except Exception:
            checkpoint = []
            msg = _('checkpoint list can not be retrieved.')
            exceptions.handle(self.request, msg)
        return checkpoint

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        checkpoint = self.get_checkpoint_data()
        context["checkpoint"] = checkpoint
        provider_id = self.kwargs['provider_id']
        provider = karborclient.provider_get(self.request, provider_id)
        context["provider_name"] = provider.name
        context["resources"] = self.get_resources()
        context["url"] = reverse("horizon:karbor:protectionplans:index")
        return context

    @memoized.memoized_method
    def get_resources(self):
        results = []
        try:
            provider_id = self.kwargs['provider_id']
            checkpoint_id = self.kwargs['checkpoint_id']
            checkpoint = karborclient.checkpoint_get(self.request,
                                                     provider_id,
                                                     checkpoint_id)
            graphnodes = utils.deserialize_resource_graph(
                checkpoint.resource_graph)
            self.get_results(graphnodes, None, results)
        except Exception:
            exceptions.handle(
                self.request,
                _('Unable to retrieve checkpoint details.'),
                redirect=reverse("horizon:karbor:checkpoints:index"))
        return results

    def get_results(self, graphnodes, showparentid, results):
        for graphnode in graphnodes:
            if graphnode is not None:
                # add graph node to results
                resource = {}
                resource["id"] = graphnode.value.id
                resource["type"] = graphnode.value.type
                resource["name"] = graphnode.value.name
                resource["showid"] = str(uuid.uuid4())
                resource["showparentid"] = showparentid
                result = protectables.Instances(self, resource)
                results.append(result)
                # add child graph nodes to results
                self.get_results(graphnode.child_nodes,
                                 result.showid,
                                 results
                                 )
