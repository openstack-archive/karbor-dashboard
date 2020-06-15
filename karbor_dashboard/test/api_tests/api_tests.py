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

from karbor_dashboard.api import karbor
from karbor_dashboard.test import helpers as test


class karborApiTests(test.APITestCase):

    use_mox = False

    def test_plan_get(self):
        plan = self.plans.first()
        karborclient = self.stub_karborclient()
        karborclient.plans.get.return_value = plan

        ret_plan = karbor.plan_get(self.request,
                                   plan_id='fake_plan_id1')
        self.assertEqual(plan["id"], ret_plan["id"])
        karborclient.plans.get.assert_called_once_with(
            plan["id"])

    def test_plan_create(self):
        plan = self.plans.first()
        fake_resources = plan["resources"]
        fake_parameters = plan["parameters"]
        karborclient = self.stub_karborclient()
        karborclient.plans.create.return_value = plan

        ret_plan = karbor.plan_create(self.request,
                                      name="fake_name_1",
                                      provider_id="fake_provider_id1",
                                      resources=fake_resources,
                                      parameters=fake_parameters)
        self.assertEqual(len(plan), len(ret_plan))
        karborclient.plans.create.assert_called_once_with(
            plan["name"], plan["provider_id"],
            plan["resources"], plan["parameters"])

    def test_plan_delete(self):
        plan = self.plans.first()
        karborclient = self.stub_karborclient()
        karborclient.plans.delete.return_value = None

        karbor.plan_delete(self.request,
                           plan_id="fake_plan_id1")
        karborclient.plans.delete.assert_called_once_with(
            plan["id"])

    def test_plan_update(self):
        plan = self.plans.first()
        plan2 = self.plans.list()[0]
        data = {"name": "fake_name_new"}
        karborclient = self.stub_karborclient()
        karborclient.plans.update.return_value = plan2

        ret_plan = karbor.plan_update(self.request,
                                      plan_id="fake_plan_id1",
                                      data=data)
        self.assertEqual(plan["name"], ret_plan["name"])
        karborclient.plans.update.assert_called_once_with(plan["id"],
                                                          data)

    def test_plan_list(self):
        plans = self.plans.list()
        karborclient = self.stub_karborclient()
        karborclient.plans.list.return_value = plans

        ret_list = karbor.plan_list(self.request)
        self.assertEqual(len(plans), len(ret_list))
        karborclient.plans.list.assert_called_once_with(
            detailed=False, search_opts=None,
            marker=None, limit=None,
            sort_key=None, sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_plan_list_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)

        plan = self.plans.list()
        karborclient = self.stub_karborclient()
        karborclient.plans.list.return_value = plan

        ret_val, has_more_data, has_prev_data = karbor.plan_list_paged(
            self.request, paginate=True)
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.plans.list.assert_called_once_with(
            detailed=False, search_opts=None,
            marker=None, limit=page_size + 1,
            sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_plan_list_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        plan = self.plans.list()
        karborclient = self.stub_karborclient()
        karborclient.plans.list.return_value = plan

        ret_val, has_more_data, has_prev_data = karbor.plan_list_paged(
            self.request, paginate=True)

        self.assertEqual(len(plan), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.plans.list.assert_called_once_with(
            detailed=False, search_opts=None,
            marker=None, limit=page_size + 1,
            sort_key=None, sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_plan_list_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        plan = self.plans.list()
        karborclient = self.stub_karborclient()
        karborclient.plans.list.return_value = plan[:page_size + 1]

        ret_val, has_more_data, has_prev_data = karbor.plan_list_paged(
            self.request, paginate=True)

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.plans.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    def test_plan_list_paged_false(self):
        plans = self.plans.list()
        karborclient = self.stub_karborclient()
        karborclient.plans.list.return_value = plans

        plans, has_more_data, has_prev_data = karbor.plan_list_paged(
            self.request)
        self.assertEqual(len(plans), len(plans))
        karborclient.plans.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=None, sort_key=None, sort_dir=None,
            sort=None)

    def test_scheduled_operation_create(self):
        scheduled_operation = self.scheduled_operations.first()
        operation_definition = {"trigger_id": "fake_trigger_id1",
                                "plan_id": "fake_plan_id"}
        karborclient = self.stub_karborclient()
        karborclient.scheduled_operations.create.return_value = \
            scheduled_operation

        ret_so = karbor.scheduled_operation_create(
            self.request,
            name="My-scheduled-operation",
            operation_type="protect",
            trigger_id="fake_trigger_id1",
            operation_definition=operation_definition)
        self.assertEqual(scheduled_operation["id"], ret_so["id"])
        karborclient.scheduled_operations.create.assert_called_once_with(
            "My-scheduled-operation", "protect", "fake_trigger_id1",
            operation_definition)

    def test_scheduled_operation_delete(self):
        scheduled_operation = self.scheduled_operations.first()
        karborclient = self.stub_karborclient()
        karborclient.scheduled_operations.delete.return_value = None

        karbor.scheduled_operation_delete(self.request,
                                          scheduled_operation["id"])
        karborclient.scheduled_operations.delete.assert_called_once_with(
            scheduled_operation["id"])

    def test_scheduled_operation_list(self):
        scheduled_operation = self.scheduled_operations.list()
        karborclient = self.stub_karborclient()
        karborclient.scheduled_operations.list.return_value = \
            scheduled_operation

        ret_val = karbor.scheduled_operation_list(self.request)
        self.assertEqual(len(scheduled_operation), len(ret_val))
        karborclient.scheduled_operations.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=None, sort_key=None, sort_dir=None, sort=None)

    def test_scheduled_operation_list_false(self):
        scheduled_operation = self.scheduled_operations.list()
        karborclient = self.stub_karborclient()
        karborclient.scheduled_operations.list.return_value = \
            scheduled_operation

        ret_val, has_more_data, has_prev_data = \
            karbor.scheduled_operation_list_paged(self.request, paginate=False)
        self.assertEqual(len(scheduled_operation), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

        karborclient.scheduled_operations.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None, limit=None,
            sort_key=None, sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_scheduled_operation_list_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)
        scd_operation = self.scheduled_operations.list()
        karborclient = self.stub_karborclient()
        karborclient.scheduled_operations.list.return_value = scd_operation

        ret_val, has_more_data, has_prev_data = \
            karbor.scheduled_operation_list_paged(self.request, paginate=True)
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.scheduled_operations.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_scheduled_operation_list_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        scd_operation = self.scheduled_operations.list()
        karborclient = self.stub_karborclient()
        karborclient.scheduled_operations.list.return_value = scd_operation

        ret_val, has_more_data, has_prev_data = \
            karbor.scheduled_operation_list_paged(self.request, paginate=True)

        self.assertEqual(len(scd_operation), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)

        karborclient.scheduled_operations.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None,
            sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_scheduled_operation_list_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        scd_operation = self.scheduled_operations.list()
        karborclient = self.stub_karborclient()
        karborclient.scheduled_operations.list.return_value = \
            scd_operation[:page_size + 1]

        ret_val, has_more_data, has_prev_data = \
            karbor.scheduled_operation_list_paged(self.request, paginate=True)

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)

        karborclient.scheduled_operations.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None,
            sort_dir=None, sort=None)

    def test_scheduled_operation_get(self):
        scheduled_operation = self.scheduled_operations.first()
        karborclient = self.stub_karborclient()
        karborclient.scheduled_operations.get.return_value = \
            scheduled_operation
        ret_val = karbor.scheduled_operation_get(self.request,
                                                 "fake_scheduled_operation_1")
        self.assertEqual(scheduled_operation["id"], ret_val["id"])
        karborclient.scheduled_operations.get.assert_called_once_with(
            scheduled_operation["id"])

    def test_restore_create(self):
        restore = self.restores.first()
        karborclient = self.stub_karborclient()
        karborclient.restores.create.return_value = restore

        ret_val = karbor.restore_create(self.request,
                                        restore["provider_id"],
                                        restore["checkpoint_id"],
                                        restore["restore_target"],
                                        restore["parameters"],
                                        restore["restore_auth"])
        self.assertEqual(restore["id"], ret_val["id"])
        karborclient.restores.create.assert_called_once_with(
            restore["provider_id"], restore["checkpoint_id"],
            restore["restore_target"], restore["parameters"],
            restore["restore_auth"])

    def test_restore_delete(self):
        restore = self.restores.first()
        karborclient = self.stub_karborclient()
        karborclient.restores.delete.return_value = restore

        karbor.restore_delete(self.request, restore["id"])

    def test_restore_list(self):
        restores = self.restores.list()
        karborclient = self.stub_karborclient()
        karborclient.restores.list.return_value = restores

        ret_val = karbor.restore_list(self.request)
        self.assertEqual(len(restores), len(ret_val))
        karborclient.restores.list.asssert_called_with(
            detailed=False, search_opts=None,
            marker=None, limit=None, sort_key=None,
            sort_dir=None, sort=None)

    def test_restore_list_false(self):
        restores = self.restores.list()
        karborclient = self.stub_karborclient()
        karborclient.restores.list.return_value = restores

        ret_val, has_more_data, has_prev_data = karbor.restore_list_paged(
            self.request, paginate=False)
        self.assertEqual(len(restores), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.restores.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=None, sort_key=None, sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_restore_list_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)
        restore_list = self.restores.list()
        karborclient = self.stub_karborclient()
        karborclient.restores.list.return_value = restore_list

        ret_val, has_more_data, has_prev_data = karbor.restore_list_paged(
            self.request, paginate=True)
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.restores.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_restore_list_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        restore_list = self.restores.list()
        karborclient = self.stub_karborclient()
        karborclient.restores.list.return_value = restore_list

        ret_val, has_more_data, has_prev_data = karbor.restore_list_paged(
            self.request, paginate=True)

        self.assertEqual(len(restore_list), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.restores.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_restore_list_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        restore_list = self.restores.list()
        karborclient = self.stub_karborclient()
        karborclient.restores.list.return_value = restore_list[:page_size + 1]
        ret_val, has_more_data, has_prev_data = karbor.restore_list_paged(
            self.request, paginate=True)

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.restores.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    def test_restore_get(self):
        restore = self.restores.first()
        karborclient = self.stub_karborclient()
        karborclient.restores.get.return_value = restore

        ret_val = karbor.restore_get(self.request, restore["id"])
        self.assertEqual(restore["id"], ret_val["id"])
        karborclient.restores.get.assert_called_once_with(restore["id"])

    def test_protectable_list(self):
        protectables_list = self.protectables_list.list()
        karborclient = self.stub_karborclient()
        karborclient.protectables.list.return_value = protectables_list

        ret_val = karbor.protectable_list(self.request)
        self.assertEqual(len(protectables_list), len(ret_val))

        karborclient.protectables.list.assert_called_once_with()

    def test_protectable_get(self):
        protectable = self.protectables_show.list()[0]
        karborclient = self.stub_karborclient()
        karborclient.protectables.get.return_value = protectable

        ret_val = karbor.protectable_get(self.request,
                                         protectable_type="OS::Nova::Server")
        self.assertEqual(protectable["name"], ret_val["name"])
        karborclient.protectables.get.assert_called_once_with(
            "OS::Nova::Server")

    def test_protectable_get_instance(self):
        protectable = self.protectables_ins.list()[1]
        karborclient = self.stub_karborclient()
        karborclient.protectables.get_instance.return_value = protectable
        ret_val = karbor.protectable_get_instance(self.request,
                                                  "OS::Nova::Server",
                                                  protectable["id"]
                                                  )
        self.assertEqual(protectable["name"], ret_val["name"])
        karborclient.protectables.get_instance.assert_called_once_with(
            "OS::Nova::Server", protectable["id"])

    def test_protectable_list_instances(self):
        protectable = self.protectables_ins.list()
        karborclient = self.stub_karborclient()
        karborclient.protectables.list_instances.return_value = \
            protectable

        ret_val = karbor.protectable_list_instances(
            self.request, protectable_type="OS::Nova::Server")
        self.assertEqual(len(protectable), len(ret_val))
        karborclient.protectables.list_instances.assert_called_once_with(
            protectable_type="OS::Nova::Server", search_opts=None,
            marker=None, limit=None, sort_key=None,
            sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_protectable_list_instances_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)
        protectable_list = self.protectables_ins.list()
        karborclient = self.stub_karborclient()
        karborclient.protectables.list_instances.return_value = \
            protectable_list

        ret_val, has_more_data, has_prev_data = \
            karbor.protectable_list_instances_paged(
                self.request,
                paginate=True,
                protectable_type="OS::Nova::Server")
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.protectables.list_instances.assert_called_once_with(
            "OS::Nova::Server", search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_protectable_list_instances_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        protectable_list = self.protectables_ins.list()
        karborclient = self.stub_karborclient()
        karborclient.protectables.list_instances.return_value = \
            protectable_list

        ret_val, has_more_data, has_prev_data = \
            karbor.protectable_list_instances_paged(
                self.request,
                paginate=True,
                protectable_type="OS::Nova::Server")
        self.assertEqual(len(protectable_list), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.protectables.list_instances.assert_called_once_with(
            "OS::Nova::Server", search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None,
            sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_protectable_list_instances_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        protectable_list = self.protectables_ins.list()
        karborclient = self.stub_karborclient()
        karborclient.protectables.list_instances.return_value =\
            protectable_list[:page_size + 1]

        ret_val, has_more_data, has_prev_data = \
            karbor.protectable_list_instances_paged(
                self.request,
                paginate=True,
                protectable_type="OS::Nova::Server")

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.protectables.list_instances.assert_called_once_with(
            "OS::Nova::Server", search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    def test_protectable_list_instances_false(self):
        protectable = self.protectables_ins.list()
        karborclient = self.stub_karborclient()
        karborclient.protectables.list_instances.return_value = protectable

        ret_val, has_more_data, has_prev_data = \
            karbor.protectable_list_instances_paged(
                self.request,
                protectable_type="OS::Nova::Server")
        self.assertEqual(len(protectable), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.protectables.list_instances(
            "OS::Nova::Server", search_opts=None, marker=None,
            limit=None, sort_key=None, sort_dir=None,
            sort=None)

    def test_provider_list(self):
        providers = self.providers.list()
        karborclient = self.stub_karborclient()
        karborclient.providers.list.return_value = providers

        ret_val = karbor.provider_list(self.request)
        self.assertEqual(len(providers), len(ret_val))
        karborclient.providers.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=None, sort_key=None, sort_dir=None,
            sort=None)

    def test_provider_list_paged_false(self):
        providers = self.providers.list()
        karborclient = self.stub_karborclient()
        karborclient.providers.list.return_value = providers

        ret_val, has_more_data, has_prev_data = karbor.provider_list_paged(
            self.request, paginate=False)
        self.assertEqual(len(providers), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.providers.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None, limit=None,
            sort_key=None, sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_provider_list_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)
        providers = self.providers.list()
        karborclient = self.stub_karborclient()
        karborclient.providers.list.return_value = providers

        ret_val, has_more_data, has_prev_data = karbor.provider_list_paged(
            self.request, paginate=True)
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.providers.list(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_provider_list_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        providers = self.providers.list()
        karborclient = self.stub_karborclient()
        karborclient.providers.list.return_value = providers

        ret_val, has_more_data, has_prev_data = karbor.provider_list_paged(
            self.request, paginate=True)
        self.assertEqual(len(providers), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.providers.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None,
            sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_provider_list_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        providers = self.providers.list()
        karborclient = self.stub_karborclient()
        karborclient.providers.list.return_value = \
            providers[:page_size + 1]
        ret_val, has_more_data, has_prev_data = karbor.provider_list_paged(
            self.request, paginate=True)

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.providers.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    def test_provider_get(self):
        provider = self.providers.first()
        karborclient = self.stub_karborclient()
        karborclient.providers.get.return_value = provider

        ret_provider = karbor.provider_get(self.request,
                                           provider_id="fake_provider_id")
        self.assertEqual(provider["name"], ret_provider["name"])
        karborclient.providers.get.assert_called_once_with(provider["id"])

    def test_checkpoint_create(self):
        checkpoint = self.checkpoints.first()
        karborclient = self.stub_karborclient()
        karborclient.checkpoints.create.return_value = checkpoint

        ret_checkpoint = karbor.checkpoint_create(
            self.request,
            provider_id="fake_provider_id",
            plan_id="fake_plan_id")
        self.assertEqual(checkpoint["id"], ret_checkpoint["id"])
        karborclient.checkpoints.create.assert_called_once_with(
            checkpoint["provider_id"],
            checkpoint["plan"]["plan_id"])

    def test_checkpoint_delete(self):
        checkpoint = self.checkpoints.first()
        karborclient = self.stub_karborclient()
        karborclient.checkpoints.delete.return_value = None

        karbor.checkpoint_delete(self.request,
                                 provider_id="fake_provider_id",
                                 checkpoint_id="fake_checkpoint_id")
        karborclient.checkpoints.delete.assert_called_once_with(
            checkpoint["provider_id"], checkpoint["id"])

    def test_checkpoint_list(self):
        checkpoints = self.checkpoints.list()
        karborclient = self.stub_karborclient()
        karborclient.checkpoints.list.return_value = checkpoints

        ret_checkpoints = karbor.checkpoint_list(self.request)
        self.assertEqual(len(checkpoints), len(ret_checkpoints))
        karborclient.checkpoints.list.assert_called_once_with(
            provider_id=None, search_opts=None, marker=None,
            limit=None, sort_key=None, sort_dir=None,
            sort=None)

    def test_checkpoint_list_paged_false(self):
        checkpoints = self.checkpoints.list()
        karborclient = self.stub_karborclient()
        karborclient.checkpoints.list.return_value = checkpoints

        ret_val, has_more_data, has_prev_data = karbor.checkpoint_list_paged(
            self.request, paginate=False)
        self.assertEqual(len(checkpoints), len(ret_val))
        karborclient.checkpoints.list.assert_called_once_with(
            provider_id=None, search_opts=None, marker=None,
            limit=None, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_checkpoint_list_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)
        checkpoints = self.checkpoints.list()
        karborclient = self.stub_karborclient()
        karborclient.checkpoints.list.return_value = checkpoints

        ret_val, has_more_data, has_prev_data = karbor.checkpoint_list_paged(
            self.request, paginate=True)
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.checkpoints.list.assert_called_once_with(
            provider_id=None, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None,
            sort_dir=None, sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_checkpoint_list_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        checkpoints = self.checkpoints.list()
        karborclient = self.stub_karborclient()
        karborclient.checkpoints.list.return_value = checkpoints

        ret_val, has_more_data, has_prev_data = karbor.checkpoint_list_paged(
            self.request, paginate=True)
        self.assertEqual(len(checkpoints), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.checkpoints.list.assert_called_once_with(
            provider_id=None, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_checkpoint_list_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        checkpoint2 = self.checkpoints.list()
        karborclient = self.stub_karborclient()
        karborclient.checkpoints.list.return_value = \
            checkpoint2[:page_size + 1]
        ret_val, has_more_data, has_prev_data = karbor.checkpoint_list_paged(
            self.request, paginate=True)

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.checkpoints.list.assert_called_once_with(
            provider_id=None, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    def test_checkpoint_get(self):
        checkpoint = self.checkpoints.first()
        karborclient = self.stub_karborclient()
        karborclient.checkpoints.get.return_value = checkpoint

        ret_checkpoint = karbor.checkpoint_get(
            self.request,
            provider_id="fake_provider_id",
            checkpoint_id="fake_checkpoint_id")
        self.assertEqual(checkpoint["id"], ret_checkpoint["id"])
        karborclient.checkpoints.get.assert_called_once_with(
            checkpoint["provider_id"], checkpoint["id"])

    def test_trigger_create(self):
        trigger = self.triggers.first()
        karborclient = self.stub_karborclient()
        karborclient.triggers.create.return_value = trigger

        ret_trigger = karbor.trigger_create(self.request,
                                            trigger["name"],
                                            trigger["type"],
                                            trigger["properties"])
        self.assertEqual(trigger["id"], ret_trigger["id"])
        karborclient.triggers.create.assert_called_once_with(
            trigger["name"], trigger["type"], trigger["properties"])

    def test_trigger_delete(self):
        trigger = self.triggers.first()
        karborclient = self.stub_karborclient()
        karborclient.triggers.delete.return_value = trigger["id"]

        karbor.trigger_delete(self.request, trigger["id"])
        karborclient.triggers.delete.assert_called_once_with(trigger["id"])

    def test_trigger_list(self):
        ret_triggers = self.triggers.list()
        karborclient = self.stub_karborclient()
        karborclient.triggers.list.return_value = ret_triggers

        ret_val = karbor.trigger_list(self.request)
        self.assertEqual(len(ret_triggers), len(ret_val))
        karborclient.triggers.list.assert_called_once_with(
            detailed=False, limit=None, marker=None, search_opts=None,
            sort=None, sort_dir=None, sort_key=None)

    def test_trigger_list_paged_false(self):
        ret_triggers = self.triggers.list()
        karborclient = self.stub_karborclient()
        karborclient.triggers.list.return_value = ret_triggers

        ret_val, has_more_data, has_prev_data = karbor.trigger_list_paged(
            self.request)
        self.assertEqual(len(ret_triggers), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.triggers.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=None, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=4)
    def test_trigger_list_paged_equal_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 4)
        ret_triggers = self.triggers.list()
        karborclient = self.stub_karborclient()
        karborclient.triggers.list.return_value = ret_triggers
        ret_val, has_more_data, has_prev_data = karbor.trigger_list_paged(
            self.request, paginate=True)
        self.assertEqual(page_size, len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.triggers.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=20)
    def test_trigger_list_paged_less_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)
        ret_triggers = self.triggers.list()
        karborclient = self.stub_karborclient()
        karborclient.triggers.list.return_value = ret_triggers
        ret_val, has_more_data, has_prev_data = karbor.trigger_list_paged(
            self.request, paginate=True)
        self.assertEqual(len(ret_triggers), len(ret_val))
        self.assertFalse(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.triggers.list.assert_called_once_with(
            detailed=False, search_opts=None, marker=None,
            limit=page_size + 1, sort_key=None, sort_dir=None,
            sort=None)

    @override_settings(API_RESULT_PAGE_SIZE=1)
    def test_trigger_list_paged_more_page_size(self):
        page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 1)
        trigger2 = self.triggers.list()
        karborclient = self.stub_karborclient()
        karborclient.triggers.list.return_value = trigger2[:page_size + 1]
        ret_val, has_more_data, has_prev_data = karbor.trigger_list_paged(
            self.request, paginate=True)

        self.assertEqual(page_size, len(ret_val))
        self.assertTrue(has_more_data)
        self.assertFalse(has_prev_data)
        karborclient.triggers.list.assert_called_once_with(
            detailed=False, search_opts=None,
            marker=None, limit=page_size + 1,
            sort_key=None, sort_dir=None, sort=None)

    def test_trigger_get(self):
        trigger = self.triggers.first()
        karborclient = self.stub_karborclient()
        karborclient.triggers.get.return_value = trigger

        ret_trigger = karbor.trigger_get(self.request,
                                         trigger_id="fake_trigger_id")
        self.assertEqual(trigger["id"], ret_trigger["id"])
        karborclient.triggers.get.assert_called_once_with(trigger["id"])
