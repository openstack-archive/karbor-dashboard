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

from karbor_dashboard import api
from karbor_dashboard.test import test_data
from karborclient.v1 import client as karbor_client
from openstack_dashboard.test import helpers


class APITestCase(helpers.APITestCase):
    """Extends the base Horizon APITestCase for karborclient"""

    def setUp(self):
        super(APITestCase, self).setUp()
        self._original_karborclient = api.karbor.karborclient
        api.karbor.karborclient = lambda request: self.stub_karborclient()

    def _setup_test_data(self):
        super(APITestCase, self)._setup_test_data()
        test_data.data(self)

    def tearDown(self):
        super(APITestCase, self).tearDown()
        api.karbor.karborclient = self._original_karborclient

    def stub_karborclient(self):
        if not hasattr(self, "karborclient"):
            self.mox.StubOutWithMock(karbor_client, 'Client')
            self.karborclient = self.mox.CreateMock(karbor_client.Client)
        return self.karborclient
