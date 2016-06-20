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

    def test_probe_index_should_have_no_error(self):
        response = self.client.get('/probes/%i/' % self.probe.id)
        self.assertEqual(response.context['error'], None)
        self.assertEqual(response.context['error_heading'], None)

    def test_should_delete_correct_probe_via_post(self):
        probe2 = Probes.objects.create(hostname='probe2',
                                       description='the probe description 2',
                                       output_directory='dir2',
                                       yaml_file='filename2',
                                       created_date='2016-02-01T12:23:34.000Z',
                                       updated_date='2016-02-02T12:23:34.000Z')

        self.client.post('/probes/%i/delete' % self.probe.id)
        self.assertEqual(len(Probes.objects.all()), 1)
        self.assertEqual(Probes.objects.get(id=probe2.id).hostname, 'probe2')

    def test_deleting_an_invalid_id_should_set_error_message(self):
        invalid_id = 9999999
        response = self.client.post('/probes/%i/delete' % invalid_id, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].extra_tags, 'alert-danger')
        self.assertEqual(str(messages[0]), 'The selected probe was not found.')

    def test_should_not_delete_probe_via_get(self):
        self.assertEqual(len(Probes.objects.all()), 1)
        self.client.get('/probes/%i/delete' % self.probe.id)
        self.assertEqual(len(Probes.objects.all()), 1)

    def test_should_edit_probe_data_via_post(self):
        valid_form_data = {
            'description': 'abc',
            'hostname': 'newhostname',
            'output_directory': '/dir1/dir2',
            'yaml_file': 'dummy.txt'
        }
        response = self.client.post('/probes/%i/edit' % self.probe.id, valid_form_data)
        self.assertEqual(response.status_code, 302)
        probe = Probes.objects.get(id=self.probe.id)
        self.assertEqual(probe.description, 'abc')
        self.assertEqual(probe.hostname, 'newhostname')
        self.assertEqual(probe.output_directory, '/dir1/dir2')
        self.assertEqual(probe.yaml_file, 'dummy.txt')

    def test_should_not_edit_probe_data_via_get(self):
        valid_form_data = {
            'description': 'abc',
            'hostname': 'newhostname',
            'output_directory': '/dir1/dir2',
            'yaml_file': 'dummy.txt'
        }
        response = self.client.get('/probes/%i/edit' % self.probe.id, valid_form_data)
        self.assertEqual(response.status_code, 302)
        probe = Probes.objects.get(id=self.probe.id)
        self.assertEqual(probe.hostname, 'probe1')

    def test_editing_an_invalid_id_should_set_error_message(self):
        invalid_id = 9999999
        response = self.client.post('/probes/%i/edit' % invalid_id, follow=True)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].extra_tags, 'alert-danger')
        self.assertEqual(str(messages[0]), 'The selected probe was not found.')

    def test_edit_with_incomplete_form_should_not_alter_probe_data(self):
        incomplete_form_data = {
            'description': 'abc',
            'hostname': 'newhostname',
            'output_directory': '/dir1/dir2'
            # 'yaml_file' field excluded.
        }
        response = self.client.post('/probes/%i/edit' % self.probe.id, incomplete_form_data)

        self.assertEqual(response.status_code, 200)
        probe = Probes.objects.get(id=self.probe.id)
        self.assertEqual(probe.description, 'the probe description')
        self.assertEqual(probe.hostname, 'probe1')
        self.assertEqual(probe.output_directory, 'dir')
        self.assertEqual(probe.yaml_file, 'filename')
        self.assertEqual(response.context['error'], {'yaml_file': [u'This field is required.']})

    def test_should_not_add_a_probe_via_get(self):
        valid_form_data = {
            'description': 'abc',
            'hostname': 'newhostname',
            'output_directory': '/dir1/dir2',
            'yaml_file': 'dummy.txt'
        }
        self.assertEqual(len(Probes.objects.all()), 1)
        response = self.client.get('/probes/add', valid_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Probes.objects.all()), 1)

    def test_should_add_a_probe_via_post(self):
        valid_form_data = {
            'description': 'abc',
            'hostname': 'newhostname',
            'output_directory': '/dir1/dir2',
            'yaml_file': 'dummy.txt'
        }
        self.assertEqual(len(Probes.objects.all()), 1)
        response = self.client.post('/probes/add', valid_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Probes.objects.all()), 2)
        probe = Probes.objects.get(id=response.url[-2:-1])
        self.assertEqual(probe.description, 'abc')
        self.assertEqual(probe.hostname, 'newhostname')
        self.assertEqual(probe.output_directory, '/dir1/dir2')
        self.assertEqual(probe.yaml_file, 'dummy.txt')

    def test_should_not_add_a_probe_with_incomplete_form_data(self):
        incomplete_form_data = {
            # 'description' field excluded
            'hostname': 'newhostname',
            'output_directory': '/dir1/dir2',
            'yaml_file': 'dummy.txt'
        }
        self.assertEqual(len(Probes.objects.all()), 1)
        response = self.client.post('/probes/%i/edit' % self.probe.id, incomplete_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Probes.objects.all()), 1)
        self.assertEqual(response.context['error'], {'description': [u'This field is required.']})
