# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import mock

import shade
from shade.tests.unit import base
from shade.tests import fakes


class TestQuotas(base.TestCase):

    def setUp(self):
        super(TestQuotas, self).setUp()
        self.cloud = shade.operator_cloud(validate=False)

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    @mock.patch.object(shade.OpenStackCloud, 'keystone_client')
    def test_update_quotas(self, mock_keystone, mock_nova):
        project = fakes.FakeProject('project_a')
        mock_keystone.tenants.list.return_value = [project]
        self.cloud.set_compute_quotas(project, cores=1)

        mock_nova.quotas.update.assert_called_once_with(
            cores=1, force=True, tenant_id='project_a')

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    @mock.patch.object(shade.OpenStackCloud, 'keystone_client')
    def test_get_quotas(self, mock_keystone, mock_nova):
        project = fakes.FakeProject('project_a')
        mock_keystone.tenants.list.return_value = [project]
        self.cloud.get_compute_quotas(project)

        mock_nova.quotas.get.assert_called_once_with(tenant_id='project_a')

    @mock.patch.object(shade.OpenStackCloud, 'nova_client')
    @mock.patch.object(shade.OpenStackCloud, 'keystone_client')
    def test_delete_quotas(self, mock_keystone, mock_nova):
        project = fakes.FakeProject('project_a')
        mock_keystone.tenants.list.return_value = [project]
        self.cloud.delete_compute_quotas(project)

        mock_nova.quotas.delete.assert_called_once_with(tenant_id='project_a')

    @mock.patch.object(shade.OpenStackCloud, 'cinder_client')
    @mock.patch.object(shade.OpenStackCloud, 'keystone_client')
    def test_cinder_update_quotas(self, mock_keystone, mock_cinder):
        project = fakes.FakeProject('project_a')
        mock_keystone.tenants.list.return_value = [project]
        self.cloud.set_volume_quotas(project, volumes=1)

        mock_cinder.quotas.update.assert_called_once_with(
            volumes=1, tenant_id='project_a')

    @mock.patch.object(shade.OpenStackCloud, 'cinder_client')
    @mock.patch.object(shade.OpenStackCloud, 'keystone_client')
    def test_cinder_get_quotas(self, mock_keystone, mock_cinder):
        project = fakes.FakeProject('project_a')
        mock_keystone.tenants.list.return_value = [project]
        self.cloud.get_volume_quotas(project)

        mock_cinder.quotas.get.assert_called_once_with(tenant_id='project_a')

    @mock.patch.object(shade.OpenStackCloud, 'cinder_client')
    @mock.patch.object(shade.OpenStackCloud, 'keystone_client')
    def test_cinder_delete_quotas(self, mock_keystone, mock_cinder):
        project = fakes.FakeProject('project_a')
        mock_keystone.tenants.list.return_value = [project]
        self.cloud.delete_volume_quotas(project)

        mock_cinder.quotas.delete.assert_called_once_with(
            tenant_id='project_a')

    @mock.patch.object(shade.OpenStackCloud, 'neutron_client')
    @mock.patch.object(shade.OpenStackCloud, 'keystone_client')
    def test_neutron_update_quotas(self, mock_keystone, mock_neutron):
        project = fakes.FakeProject('project_a')
        mock_keystone.tenants.list.return_value = [project]
        self.cloud.set_network_quotas(project, network=1)

        mock_neutron.update_quota.assert_called_once_with(
            body={'quota': {'network': 1}}, tenant_id='project_a')

    @mock.patch.object(shade.OpenStackCloud, 'neutron_client')
    @mock.patch.object(shade.OpenStackCloud, 'keystone_client')
    def test_neutron_get_quotas(self, mock_keystone, mock_neutron):
        project = fakes.FakeProject('project_a')
        mock_keystone.tenants.list.return_value = [project]
        self.cloud.get_network_quotas(project)

        mock_neutron.show_quota.assert_called_once_with(
            tenant_id='project_a')

    @mock.patch.object(shade.OpenStackCloud, 'neutron_client')
    @mock.patch.object(shade.OpenStackCloud, 'keystone_client')
    def test_neutron_delete_quotas(self, mock_keystone, mock_neutron):
        project = fakes.FakeProject('project_a')
        mock_keystone.tenants.list.return_value = [project]
        self.cloud.delete_network_quotas(project)

        mock_neutron.delete_quota.assert_called_once_with(
            tenant_id='project_a')
