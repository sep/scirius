"""
This file is part of Scirius.

Scirius is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Scirius is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Scirius.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from django.utils import timezone

from probes.models import Probes


class NoProbesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('user', 'user@example.com', 'password')
        self.client = Client()
        self.client.login(username='user', password='password')

    def tearDown(self):
        User.objects.all().delete()

    def test_index_should_show_probe_count(self):
        response = self.client.get('/probes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You currently have 0 probes defined.')

    def test_probe_index_should_redirect_to_index_for_nonexistent_probes(self):
        response = self.client.get('/probes/1/')
        self.assertRedirects(response, '/probes/')


class WithProbeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('user', 'user@example.com', 'password')
        self.client = Client()
        self.client.login(username='user', password='password')

        self.probe = Probes.objects.create(hostname='probe1',
                                           description='the probe description',
                                           output_directory='dir',
                                           yaml_file='filename',
                                           created_date='2016-01-01T12:23:34.000Z',
                                           updated_date='2016-01-02T12:23:34.000Z')

    def tearDown(self):
        User.objects.all().delete()
        Probes.objects.all().delete()

    def test_index_should_show_nonzero_probe_count(self):
        response = self.client.get('/probes/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You currently have 1 probe defined.')

    def test_probe_index_should_show_probe_info(self):
        response = self.client.get('/probes/%i/' % self.probe.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Probe probe1')
        self.assertContains(response, 'the probe description')
        self.assertContains(response, 'Created on Jan. 1, 2016, 12:23 p.m.')
        self.assertContains(response, 'Last modified on Jan. 2, 2016, 12:23 p.m.')
