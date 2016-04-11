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

from openstack_dashboard.test import helpers
from smaug_dashboard import api
from smaug_dashboard.test import test_data
from smaugclient.v1 import client as smaug_client


class APITestCase(helpers.APITestCase):
    """Extends the base Horizon APITestCase for smaugclient"""

    def setUp(self):
        super(APITestCase, self).setUp()
        self._original_smaugclient = api.smaug.smaugclient
        api.smaug.smaugclient = lambda request: self.stub_smaugclient()

    def _setup_test_data(self):
        super(APITestCase, self)._setup_test_data()
        test_data.data(self)

    def tearDown(self):
        super(APITestCase, self).tearDown()
        api.smaug.smaugclient = self._original_smaugclient

    def stub_smaugclient(self):
        if not hasattr(self, "smaugclient"):
            self.mox.StubOutWithMock(smaug_client, 'Client')
            self.smaugclient = self.mox.CreateMock(smaug_client.Client)
        return self.smaugclient
