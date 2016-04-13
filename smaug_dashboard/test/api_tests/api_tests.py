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

    def test_scheduled_operation_create(self):
        scheduled_operation = self.scheduled_operations.first()
        operation_definition = {"trigger_id": "fake_trigger_id1",
                                "plan_id": "fake_plan_id"}
        smaugclient = self.stub_smaugclient()
        smaugclient.scheduled_operations = self.mox.CreateMockAnything()
        smaugclient.scheduled_operations.create(
            "My-scheduled-operation",
            "protect",
            "fake_trigger_id1",
            operation_definition).AndReturn(scheduled_operation)
        self.mox.ReplayAll()

        ret_so = smaug.scheduled_operation_create(
            self.request,
            name="My-scheduled-operation",
            operation_type="protect",
            trigger_id="fake_trigger_id1",
            operation_definition=operation_definition)
        self.assertEqual(scheduled_operation["id"], ret_so["id"])

    def test_scheduled_operation_delete(self):
        scheduled_operation = self.scheduled_operations.first()
        smaugclient = self.stub_smaugclient()
        smaugclient.scheduled_operations = self.mox.CreateMockAnything()
        smaugclient.scheduled_operations.delete(scheduled_operation["id"])
        self.mox.ReplayAll()

        smaug.scheduled_operation_delete(self.request,
                                         scheduled_operation["id"])

    def test_scheduled_operation_list(self):
        scheduled_operation = self.scheduled_operations.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.scheduled_operations = self.mox.CreateMockAnything()
        smaugclient.scheduled_operations.list(
            detailed=False,
            search_opts=None,
            marker=None,
            limit=None,
            sort_key=None,
            sort_dir=None,
            sort=None).AndReturn(scheduled_operation)
        self.mox.ReplayAll()

        ret_val = smaug.scheduled_operation_list(self.request)
        self.assertEqual(len(scheduled_operation), len(ret_val))

    def test_scheduled_operation_list_false(self):
        scheduled_operation = self.scheduled_operations.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.scheduled_operations = self.mox.CreateMockAnything()
        smaugclient.scheduled_operations.list(
            detailed=False,
            search_opts=None,
            marker=None,
            limit=None,
            sort_key=None,
            sort_dir=None,
            sort=None).AndReturn(scheduled_operation)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = \
            smaug.scheduled_operation_list_paged(self.request, paginate=False)
        self.assertEqual(len(scheduled_operation), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_scheduled_operation_list_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)
        scd_operation = self.scheduled_operations.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.scheduled_operations = self.mox.CreateMockAnything()
        smaugclient.scheduled_operations.list(
            detailed=False,
            search_opts=None,
            marker=None,
            limit=page_size + 1,
            sort_key=None,
            sort_dir=None,
            sort=None).AndReturn(scd_operation)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = \
            smaug.scheduled_operation_list_paged(self.request, paginate=True)
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_scheduled_operation_list_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        scd_operation = self.scheduled_operations.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.scheduled_operations = self.mox.CreateMockAnything()
        smaugclient.scheduled_operations.list(
            detailed=False,
            search_opts=None,
            marker=None,
            limit=page_size + 1,
            sort_key=None,
            sort_dir=None,
            sort=None).AndReturn(scd_operation)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = \
            smaug.scheduled_operation_list_paged(self.request, paginate=True)

        self.assertEqual(len(scd_operation), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_scheduled_operation_list_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        scd_operation = self.scheduled_operations.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.scheduled_operations = self.mox.CreateMockAnything()
        smaugclient.scheduled_operations.list(
            detailed=False,
            search_opts=None,
            marker=None,
            limit=page_size + 1,
            sort_key=None,
            sort_dir=None,
            sort=None).AndReturn(scd_operation[:page_size + 1])
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = \
            smaug.scheduled_operation_list_paged(self.request, paginate=True)

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)

    def test_scheduled_operation_get(self):
        scheduled_operation = self.scheduled_operations.first()
        smaugclient = self.stub_smaugclient()
        smaugclient.scheduled_operations = self.mox.CreateMockAnything()
        smaugclient.scheduled_operations.get(
            scheduled_operation["id"]).AndReturn(scheduled_operation)
        self.mox.ReplayAll()

        ret_val = smaug.scheduled_operation_get(self.request,
                                                "fake_scheduled_operation_1")
        self.assertEqual(scheduled_operation["id"], ret_val["id"])

    def test_restore_create(self):
        restore = self.restores.first()
        smaugclient = self.stub_smaugclient()
        smaugclient.restores = self.mox.CreateMockAnything()
        smaugclient.restores.create(restore["provider_id"],
                                    restore["checkpoint_id"],
                                    restore["restore_target"],
                                    restore["parameters"]).AndReturn(restore)
        self.mox.ReplayAll()

        ret_val = smaug.restore_create(self.request,
                                       restore["provider_id"],
                                       restore["checkpoint_id"],
                                       restore["restore_target"],
                                       restore["parameters"])
        self.assertEqual(restore["id"], ret_val["id"])

    def test_restore_delete(self):
        restore = self.restores.first()
        smaugclient = self.stub_smaugclient()
        smaugclient.restores = self.mox.CreateMockAnything()
        smaugclient.restores.delete(restore["id"]).AndReturn(restore)
        self.mox.ReplayAll()

        smaug.restore_delete(self.request, restore["id"])

    def test_restore_list(self):
        restores = self.restores.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.restores = self.mox.CreateMockAnything()
        smaugclient.restores.list(detailed=False,
                                  search_opts=None,
                                  marker=None,
                                  limit=None,
                                  sort_key=None,
                                  sort_dir=None,
                                  sort=None).AndReturn(restores)
        self.mox.ReplayAll()

        ret_val = smaug.restore_list(self.request)
        self.assertEqual(len(restores), len(ret_val))

    def test_restore_list_false(self):
        restores = self.restores.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.restores = self.mox.CreateMockAnything()
        smaugclient.restores.list(detailed=False,
                                  search_opts=None,
                                  marker=None,
                                  limit=None,
                                  sort_key=None,
                                  sort_dir=None,
                                  sort=None).AndReturn(restores)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = smaug.restore_list_paged(
            self.request, paginate=False)
        self.assertEqual(len(restores), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_restore_list_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)
        restore_list = self.restores.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.restores = self.mox.CreateMockAnything()
        smaugclient.restores.list(detailed=False,
                                  search_opts=None,
                                  marker=None,
                                  limit=page_size + 1,
                                  sort_key=None,
                                  sort_dir=None,
                                  sort=None).AndReturn(restore_list)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = smaug.restore_list_paged(
            self.request, paginate=True)
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_restore_list_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        restore_list = self.restores.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.restores = self.mox.CreateMockAnything()
        smaugclient.restores.list(detailed=False,
                                  search_opts=None,
                                  marker=None,
                                  limit=page_size + 1,
                                  sort_key=None,
                                  sort_dir=None,
                                  sort=None).AndReturn(restore_list)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = smaug.restore_list_paged(
            self.request, paginate=True)

        self.assertEqual(len(restore_list), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_restore_list_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        restore_list = self.restores.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.restores = self.mox.CreateMockAnything()
        smaugclient.restores.list(
            detailed=False,
            search_opts=None,
            marker=None,
            limit=page_size + 1,
            sort_key=None,
            sort_dir=None,
            sort=None).AndReturn(restore_list[:page_size + 1])
        self.mox.ReplayAll()
        ret_val, has_more_data, has_prev_data = smaug.restore_list_paged(
            self.request, paginate=True)

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)

    def test_restore_get(self):
        restore = self.restores.first()
        smaugclient = self.stub_smaugclient()
        smaugclient.restores = self.mox.CreateMockAnything()
        smaugclient.restores.get(restore["id"]).AndReturn(restore)
        self.mox.ReplayAll()

        ret_val = smaug.restore_get(self.request, restore["id"])
        self.assertEqual(restore["id"], ret_val["id"])

    def test_protectable_list(self):
        protectables_list = self.protectables_list.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.protectables = self.mox.CreateMockAnything()
        smaugclient.protectables.list().AndReturn(protectables_list)
        self.mox.ReplayAll()

        ret_val = smaug.protectable_list(self.request)
        self.assertEqual(len(protectables_list), len(ret_val))

    def test_protectable_get(self):
        protectable = self.protectables_show.list()[0]
        smaugclient = self.stub_smaugclient()
        smaugclient.protectables = self.mox.CreateMockAnything()
        smaugclient.protectables.get("OS::Nova::Server").AndReturn(protectable)
        self.mox.ReplayAll()

        ret_val = smaug.protectable_get(self.request,
                                        protectable_type="OS::Nova::Server")
        self.assertEqual(protectable["name"], ret_val["name"])

    def test_protectable_list_instances(self):
        protectable = self.protectables_ins.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.protectables = self.mox.CreateMockAnything()
        smaugclient.protectables.list_instances(
            protectable_type="OS::Nova::Server",
            search_opts=None,
            marker=None,
            limit=None,
            sort_key=None,
            sort_dir=None,
            sort=None).AndReturn(protectable)
        self.mox.ReplayAll()

        ret_val = smaug.protectable_list_instances(
            self.request, protectable_type="OS::Nova::Server")
        self.assertEqual(len(protectable), len(ret_val))

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_protectable_list_instances_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)
        protectable_list = self.protectables_ins.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.protectables = self.mox.CreateMockAnything()
        smaugclient.protectables.list_instances("OS::Nova::Server",
                                                search_opts=None,
                                                marker=None,
                                                limit=page_size + 1,
                                                sort_key=None,
                                                sort_dir=None,
                                                sort=None,
                                                ).AndReturn(protectable_list)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = \
            smaug.protectable_list_instances_paged(
                self.request,
                paginate=True,
                protectable_type="OS::Nova::Server")
        self.assertEqual(page_size, len(ret_val[0]))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_protectable_list_instances_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        protectable_list = self.protectables_ins.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.protectables = self.mox.CreateMockAnything()
        smaugclient.protectables.list_instances("OS::Nova::Server",
                                                search_opts=None,
                                                marker=None,
                                                limit=page_size + 1,
                                                sort_key=None,
                                                sort_dir=None,
                                                sort=None,
                                                ).AndReturn(protectable_list)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = \
            smaug.protectable_list_instances_paged(
                self.request,
                paginate=True,
                protectable_type="OS::Nova::Server")
        self.assertEqual(len(protectable_list), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_protectable_list_instances_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        protectable_list = self.protectables_ins.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.protectables = self.mox.CreateMockAnything()
        smaugclient.protectables.list_instances(
            "OS::Nova::Server",
            search_opts=None,
            marker=None,
            limit=page_size + 1,
            sort_key=None,
            sort_dir=None,
            sort=None
        ).AndReturn(protectable_list[:page_size + 1])
        self.mox.ReplayAll()
        ret_val, has_more_data, has_prev_data = \
            smaug.protectable_list_instances_paged(
                self.request,
                paginate=True,
                protectable_type="OS::Nova::Server")

        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

    def test_protectable_list_instances_false(self):
        protectable = self.protectables_ins.list()
        smaugclient = self.stub_smaugclient()
        smaugclient.protectables = self.mox.CreateMockAnything()
        smaugclient.protectables.list_instances(
            "OS::Nova::Server",
            search_opts=None,
            marker=None,
            limit=None,
            sort_key=None,
            sort_dir=None,
            sort=None
        ).AndReturn(protectable)
        self.mox.ReplayAll()

        ret_val, has_more_data, has_prev_data = \
            smaug.protectable_list_instances_paged(
                self.request,
                protectable_type="OS::Nova::Server")
        self.assertEqual(len(protectable), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
