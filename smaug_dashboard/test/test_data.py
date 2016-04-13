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


from openstack_dashboard.test.test_data import utils


def data(TEST):
    # Test Data Containers
    # 'TEST.xxxs' to avoid Swift naming confusion
    TEST.plans = utils.TestDataContainer()

    # plan data
    resources = [
        {"id": "fake_resources_id1",
         "type": "OS::Nova::Server"},
        {"id": "fake_resources_id2",
         "type": "OS::Cinder::Volume"},
        {"id": "fake_resources_id3",
         "type": "OS::Cinder::Volume"}
    ]
    parameters = {"OS::Nova::Server": {"consistency": "crash"}}

    plan_dict_1 = {
        "id": "fake_plan_id1",
        "name": "fake_name_1",
        "provider_id": "fake_provider_id1"
    }
    plan_dict_1.setdefault("resources", resources)
    plan_dict_1.setdefault("parameters", parameters)

    plan_dict_2 = {
        "id": "fake_plan_id2",
        "name": "fake_name_new",
        "provider_id": "fake_provider_id2"
    }
    plan_dict_2.setdefault("resources", resources)
    plan_dict_2.setdefault("parameters", parameters)

    plan_dict_3 = {
        "id": "fake_plan_id3",
        "name": "fake_name_3",
        "provider_id": "fake_provider_id3"
    }
    plan_dict_3.setdefault("resources", resources)
    plan_dict_3.setdefault("parameters", parameters)

    plan_dict_4 = {
        "id": "fake_plan_id4",
        "name": "fake_name_4",
        "provider_id": "fake_provider_id4"
    }
    plan_dict_4.setdefault("resources", resources)
    plan_dict_4.setdefault("parameters", parameters)

    TEST.plans.add(plan_dict_1, plan_dict_2, plan_dict_3, plan_dict_4)
