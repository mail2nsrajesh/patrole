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

from tempest import config
from tempest.lib import decorators

from patrole_tempest_plugin import rbac_rule_validation
from patrole_tempest_plugin.rbac_utils import rbac_utils
from patrole_tempest_plugin.tests.api.compute import rbac_base

CONF = config.CONF


class InstanceActionsRbacTest(rbac_base.BaseV2ComputeRbacTest):

    @classmethod
    def setup_clients(cls):
        super(InstanceActionsRbacTest, cls).setup_clients()
        cls.client = cls.servers_client

    @classmethod
    def skip_checks(cls):
        super(InstanceActionsRbacTest, cls).skip_checks()
        if not CONF.compute_feature_enabled.api_extensions:
            raise cls.skipException(
                '%s skipped as no compute extensions enabled' % cls.__name__)

    @classmethod
    def resource_setup(cls):
        super(InstanceActionsRbacTest, cls).resource_setup()
        cls.server = cls.create_test_server(wait_until='ACTIVE')
        cls.request_id = cls.server.response['x-compute-request-id']

    def tearDown(self):
        rbac_utils.switch_role(self, switchToRbacRole=False)
        super(InstanceActionsRbacTest, self).tearDown()

    @decorators.idempotent_id('9d1b131d-407e-4fa3-8eef-eb2c4526f1da')
    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:os-instance-actions")
    def test_list_instance_actions(self):
        self.client.list_instance_actions(self.server['id'])

    @decorators.idempotent_id('eb04c439-4215-4029-9ccb-5b3c041bfc25')
    @rbac_rule_validation.action(
        service="nova",
        rule="os_compute_api:os-instance-actions:events")
    def test_get_instance_action(self):
        self.client.show_instance_action(
            self.server['id'], self.request_id)['instanceAction']