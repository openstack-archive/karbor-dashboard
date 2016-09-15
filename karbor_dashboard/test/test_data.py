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
    TEST.scheduled_operations = utils.TestDataContainer()
    TEST.restores = utils.TestDataContainer()
    TEST.protectables = utils.TestDataContainer()
    TEST.protectables_show = utils.TestDataContainer()
    TEST.protectables_list = utils.TestDataContainer()
    TEST.protectables_ins = utils.TestDataContainer()
    TEST.providers = utils.TestDataContainer()
    TEST.checkpoints = utils.TestDataContainer()
    TEST.triggers = utils.TestDataContainer()

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

    # scheduled_operation
    scheduled_operation_1 = {
        "id": "fake_scheduled_operation_1",
        "name": "My-scheduled-operation",
        "project_id": "fake_project_id",
        "operation_type": "protect",
        "operation_definition": {
            "trigger_id": "fake_trigger_id1",
            "plan_id": "fake_plan_id"
        }}
    scheduled_operation_2 = {
        "id": "fake_scheduled_operation_2",
        "name": "My_fake_name2",
        "project_id": "fake_project_id2",
        "operation_type": "protect",
        "operation_definition": {
            "trigger_id": "fake_trigger_id2",
            "plan_id": "fake_plan_id2"
        }}
    scheduled_operation_3 = {
        "id": "fake_scheduled_operation_3",
        "name": "My_fake_name3",
        "project_id": "fake_project_id3",
        "operation_type": "protect",
        "operation_definition": {
            "trigger_id": "fake_trigger_id3",
            "plan_id": "fake_plan_id3"
        }}
    scheduled_operation_4 = {
        "id": "fake_scheduled_operation_4",
        "name": "My_fake_name4",
        "project_id": "fake_project_id4",
        "operation_type": "protect",
        "operation_definition": {
            "trigger_id": "fake_trigger_id4",
            "plan_id": "fake_plan_id4"
        }}

    TEST.scheduled_operations.add(scheduled_operation_1,
                                  scheduled_operation_2)
    TEST.scheduled_operations.add(scheduled_operation_3,
                                  scheduled_operation_4)

    # restores

    resource_dict_1 = {
        "id": "fake_restore_id",
        "project_id": "fake_project_id",
        "provider_id": "fake_provider_id",
        "checkpoint_id": "fake_checkpoint_id",
        "restore_target": "192.168.0.1:8080/v2.0",
        "parameters": {},
        "restore_auth": {"type": "password", "username": "admin",
                         "password": "test"},
        "status": "IN PROGRESS"
    }
    resource_dict_2 = {
        "id": "fake_restore_id2",
        "project_id": "fake_project_id2",
        "provider_id": "fake_provider_id2",
        "checkpoint_id": "fake_checkpoint_id2",
        "restore_target": "192.168.0.1:8080/v2.0",
        "parameters": {},
        "restore_auth": {"type": "password", "username": "admin",
                         "password": "test"},
        "status": "IN PROGRESS"
    }
    resource_dict_3 = {
        "id": "fake_restore_id3",
        "project_id": "fake_project_id3",
        "provider_id": "fake_provider_id3",
        "checkpoint_id": "fake_checkpoint_id3",
        "restore_target": "192.168.0.1:8080/v2.0",
        "parameters": {},
        "restore_auth": {"type": "password", "username": "admin",
                         "password": "test"},
        "status": "IN PROGRESS"
    }
    resource_dict_4 = {
        "id": "fake_restore_id4",
        "project_id": "fake_project_id4",
        "provider_id": "fake_provider_id4",
        "checkpoint_id": "fake_checkpoint_id4",
        "restore_target": "192.168.0.1:8080/v2.0",
        "parameters": {},
        "restore_auth": {"type": "password", "username": "admin",
                         "password": "test"},
        "status": "IN PROGRESS"
    }

    TEST.restores.add(resource_dict_1, resource_dict_2,
                      resource_dict_3, resource_dict_4)

    # protectables

    protectable_show_1 = {
        "name": "OS::Nova::Server",
        "dependent_types": ["OS::Cinder::Volume",
                            "OS::Glance::Image"]
    }
    protectable_show_2 = {
        "name": "OS::Nova::Server2",
        "dependent_types": ["OS::Cinder2::Volume",
                            "OS::Glance2::Image"]
    }

    TEST.protectables_show.add(protectable_show_1, protectable_show_2)

    protectable_list_1 = ["OS::Nova1::Server",
                          "OS::Cinder1::Volume",
                          "OS::Nova2::Server",
                          "OS::Cinder2::Volume"]

    TEST.protectables_list.add(protectable_list_1)

    # protectables_ins
    protectable_ins1 = [
        {
            "id": "fake_protectable_ins_id",
            "type": "OS::Nova::Server",
            "name": "fake_name1",
            "dependent_resources": [
                {"id": "protectable_ins_resources_id",
                 "type": "OS::Cinder::Volume",
                 "name": "fake_dependent_name1"}
            ]
        },
        {
            "id": "fake_protectable_ins_id2",
            "type": "OS::Nova::Server",
            "name": "fake_name2",
            "dependent_resources": [
                {"id": "protectable_ins_resources_id2",
                 "type": "OS::Glance::Image",
                 "name": "fake_dependent_name2"}
            ]
        },
        {
            "id": "fake_protectable_ins_id3",
            "type": "OS::Nova::Server",
            "name": "fake_name3",
            "dependent_resources": [
                {"id": "protectable_ins_resources_id3",
                 "type": "OS::Glance3::Image",
                 "name": "fake_dependent_name3"}
            ]
        },
        {
            "id": "fake_protectable_ins_id4",
            "type": "OS::Nova::Server",
            "name": "fake_name4",
            "dependent_resources": [
                {"id": "protectable_ins_resources_id4",
                 "type": "OS::Glance4::Image",
                 "name": "fake_dependent_name4"}
            ]
        },
    ]

    TEST.protectables_ins.add(protectable_ins1[0], protectable_ins1[1],
                              protectable_ins1[2], protectable_ins1[3])

    # providers

    saved_info_schema = {
        "OS::Cinder::Volume": {
            "title": "N",
            "type": "object",
            "properties": {
                "backup_id": {
                    "type": "string",
                    "title": "Backup ID",
                    "description": "The backup volume id"
                }
            }
        }
    }
    options_schema = {
        "OS::Nova::Server": {
            "title": "Nova Server Backup Options",
            "type": "object",
            "properties": {
                "consistency": {
                    "enum": ["crash", "os", "application"],
                    "title": "Consistency Level",
                    "description": "The desired consistency level required"
                }
            }
        }
    }
    restore_schema = {
        "OS::Nova::Server": {
            "title": "Nova Server Restore Options",
            "type": "object",
            "properties": {
                "public_ip": {
                    "title": "Replacement public IP",
                    "type": "string",
                    "description":
                        "The public IP to use on the restore site for the VM"
                }
            }
        }
    }

    provider_dick_1 = {
        "id": "fake_provider_id",
        "name": "OS Infra Provider",
        "description": "This provider uses OpenStack's own services "
                       "(swift, cinder) as storage"
    }

    provider_dick_1.setdefault("saved_info_schema", saved_info_schema)
    provider_dick_1.setdefault("options_schema", options_schema)
    provider_dick_1.setdefault("restore_schema", restore_schema)

    provider_dick_2 = {
        "id": "fake_provider_id2",
        "name": "OS Infra Provider2",
        "description": "This provider uses OpenStack's own services "
                       "(swift, cinder) as storage"
    }

    provider_dick_2.setdefault("saved_info_schema", saved_info_schema)
    provider_dick_2.setdefault("options_schema", options_schema)
    provider_dick_2.setdefault("restore_schema", restore_schema)

    provider_dick_3 = {
        "id": "fake_provider_id3",
        "name": "OS Infra Provider3",
        "description": "This provider uses OpenStack's own services "
                       "(swift, cinder) as storage"
    }

    provider_dick_3.setdefault("saved_info_schema", saved_info_schema)
    provider_dick_3.setdefault("options_schema", options_schema)
    provider_dick_3.setdefault("restore_schema", restore_schema)

    provider_dick_4 = {
        "id": "fake_provider_id4",
        "name": "OS Infra Provider4",
        "description": "This provider uses OpenStack's own services "
                       "(swift, cinder) as storage"
    }

    provider_dick_4.setdefault("saved_info_schema", saved_info_schema)
    provider_dick_4.setdefault("options_schema", options_schema)
    provider_dick_4.setdefault("restore_schema", restore_schema)

    TEST.providers.add(provider_dick_1, provider_dick_2,
                       provider_dick_3, provider_dick_4)

    # checkpoints

    checkpoint_dict_1 = {
        "id": "fake_checkpoint_id",
        "project_id": "fake_project_id",
        "status": "committed",
        "plan": {"plan_id": "fake_plan_id"},
        "provider_id": "fake_provider_id"
    }
    checkpoint_dict_2 = [
        {
            "id": "fake_checkpoint_id_2",
            "project_id": "fake_project_id_2",
            "status": "committed",
            "plan": {
                "plan_id": "fake_plan_id_2",
                "name": "My 3 tier application",
                "description": "The protection plan for my application"
            },
            "provider_id": "fake_provider_id_2"
        },
    ]
    checkpoint_dict_3 = [
        {
            "id": "fake_checkpoint_id_3",
            "project_id": "fake_project_id_3",
            "status": "committed",
            "plan": {
                "plan_id": "fake_plan_id_3",
                "name": "My 33 tier application",
                "description": "The protection plan for my application"
            },
            "provider_id": "fake_provider_id_3"
        },
    ]
    checkpoint_dict_4 = [
        {
            "id": "fake_checkpoint_id_4",
            "project_id": "fake_project_id_4",
            "status": "committed",
            "plan": {
                "plan_id": "fake_plan_id_4",
                "name": "My 4 tier application",
                "description": "The protection plan for my application"
            },
            "provider_id": "fake_provider_id_4"
        },
    ]

    TEST.checkpoints.add(checkpoint_dict_1, checkpoint_dict_2)
    TEST.checkpoints.add(checkpoint_dict_3, checkpoint_dict_4)

    # triggers

    triggers_dict_1 = {
        "id": "fake_trigger_id",
        "name": "My_backup_trigger",
        "type": "TimeTrigger",
        "properties": {
            "trigger_window": "60",
            "recurrence": {"start": "2015-12-17T08:30:00",
                           "frequency": "weekly"}
        }
    }
    triggers_dict_2 = {
        "id": "fake_trigger_id2",
        "name": "My_backup_trigger2",
        "type": "TimeTrigger2",
        "properties": {
            "trigger_window": "60",
            "recurrence": {"start": "2015-12-17T08:30:00",
                           "frequency": "weekly"}
        }
    }
    triggers_dict_3 = {
        "id": "fake_trigger_id3",
        "name": "My_backup_trigger3",
        "type": "TimeTrigger3",
        "properties": {
            "trigger_window": "60",
            "recurrence": {"start": "2015-12-17T08:30:00",
                           "frequency": "weekly"}
        }
    }
    triggers_dict_4 = {
        "id": "fake_trigger_id4",
        "name": "My_backup_trigger4",
        "type": "TimeTrigger4",
        "properties": {
            "trigger_window": "60",
            "recurrence": {"start": "2015-12-17T08:30:00",
                           "frequency": "weekly"}
        }
    }

    TEST.triggers.add(triggers_dict_1, triggers_dict_2,
                      triggers_dict_3, triggers_dict_4)
