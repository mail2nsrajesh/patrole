#    Copyright 2017 AT&T Corporation.
#    All Rights Reserved.
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

from tempest.lib import decorators
from tempest import test

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.tests.api.compute import rbac_base


class ServerPasswordRbacTest(rbac_base.BaseV2ComputeRbacTest):

    @classmethod
    def setup_clients(cls):
        super(ServerPasswordRbacTest, cls).setup_clients()
        cls.client = cls.servers_client

    @classmethod
    def skip_checks(cls):
        super(ServerPasswordRbacTest, cls).skip_checks()
        if not test.is_extension_enabled('os-server-password', 'compute'):
            msg = "%s skipped as os-server-password extension not enabled." \
                  % cls.__name__
            raise cls.skipException(msg)

    @classmethod
    def resource_setup(cls):
        super(ServerPasswordRbacTest, cls).resource_setup()
        cls.server = cls.create_test_server()

    def tearDown(self):
        self.rbac_utils.switch_role(self, switchToRbacRole=False)
        super(ServerPasswordRbacTest, self).tearDown()

    @decorators.idempotent_id('43ad7995-2f12-41cd-8ef1-bae9ffc36818')
    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:os-server-password")
    def test_delete_password(self):
        self.rbac_utils.switch_role(self, switchToRbacRole=True)
        self.client.delete_password(self.server['id'])
