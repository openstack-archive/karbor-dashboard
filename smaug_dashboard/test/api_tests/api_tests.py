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


from django.conf import settings
from django.test.utils import override_settings

from smaug_dashboard.api import smaug
from smaug_dashboard.test import helpers as test


class SmaugApiTests(test.APITestCase):
    def test_plan_get(self):
        plan = self.plans.first()
        smaugclient = self.stub_smaugclient()
        smaugclient.plans = self.mox.CreateMockAnything()
        smaugclient.plans.get(plan["id"]).AndReturn(plan)
        self.mox.ReplayAll()

        ret_plan = smaug.plan_get(self.request,
                                  plan_id='fake_plan_id1')
        self.assertEqual(plan["id"], ret_plan["id"])

    def test_plan_create(self):
        plan = self.plans.first()
        fake_resources = plan["resources"]
        smaugclient = self.stub_smaugclient()
        smaugclient.plans = self.mox.CreateMockAnything()
        smaugclient.plans.create(plan["name"], plan["provider_id"],
                                 plan["resources"]).AndReturn(plan)
        self.mox.ReplayAll()

        ret_plan = smaug.plan_create(self.request,
                                     name="fake_name_1",
                                     provider_id="fake_provider_id1",
                                     resources=fake_resources)
        self.assertEqual(len(plan), len(ret_plan))

    def test_plan_delete(self):
        plan = self.plans.first()
        smaugclient = self.stub_smaugclient()
        smaugclient.plans = self.mox.CreateMockAnything()
        smaugclient.plans.delete(plan["id"])
        self.mox.ReplayAll()

        smaug.plan_delete(self.request,
                          plan_id="fake_plan_id1")

    def test_plan_update(self):
        plan = self.plans.first()
        plan2 = self.plans.list()[0]
        data = {"name": "fake_name_new"}
        smaugclient = self.stub_smaugclient()
        smaugclient.plans = self.mox.CreateMockAnything()
        smaugclient.plans.update(plan["id"], data).AndReturn(plan2)
        self.mox.ReplayAll()

        ret_plan = smaug.plan_update(self.request,
                                     plan_id="fake_plan_id1",
                                     data=data)
        self.assertEqual(plan["name"], ret_plan["name"])

    def test_plan_list(self):
        plans = self.plans.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.plans = self.mox.CreateMockAnything()
        smaugclient.plans.list(detailed=False,
                               search_opts=None,
                               marker=None,
                               limit=None,
                               sort_key=None,
                               sort_dir=None,
                               sort=None).AndReturn(plans)
        self.mox.ReplayAll()

        ret_list = smaug.plan_list(self.request)
        self.assertEqual(len(plans), len(ret_list))

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_plan_list_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)

        plan = self.plans.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.plans = self.mox.CreateMockAnything()
        smaugclient.plans.list(detailed=False,
                               search_opts=None,
                               marker=None,
                               limit=page_size + 1,
                               sort_key=None,
                               sort_dir=None,
                               sort=None).AndReturn(plan)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = smaug.plan_list_paged(
            self.request, paginate=True)
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_plan_list_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        plan = self.plans.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.plans = self.mox.CreateMockAnything()
        smaugclient.plans.list(detailed=False,
                               search_opts=None,
                               marker=None,
                               limit=page_size + 1,
                               sort_key=None,
                               sort_dir=None,
                               sort=None).AndReturn(plan)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = smaug.plan_list_paged(
            self.request, paginate=True)

        self.assertEqual(len(plan), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_plan_list_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        plan = self.plans.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.plans = self.mox.CreateMockAnything()
        smaugclient.plans.list(detailed=False,
                               search_opts=None,
                               marker=None,
                               limit=page_size + 1,
                               sort_key=None,
                               sort_dir=None,
                               sort=None).AndReturn(plan[:page_size + 1])
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = smaug.plan_list_paged(
            self.request, paginate=True)

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)

    def test_plan_list_paged_false(self):
        plans = self.plans.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.plans = self.mox.CreateMockAnything()
        smaugclient.plans.list(detailed=False,
                               search_opts=None,
                               marker=None,
                               limit=None,
                               sort_key=None,
                               sort_dir=None,
                               sort=None).AndReturn(plans)
        self.mox.ReplayAll()

        plans, has_more_data, has_prev_data = smaug.plan_list_paged(
            self.request)
        self.assertEqual(len(plans), len(plans))
