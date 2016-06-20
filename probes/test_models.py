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

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TransactionTestCase
from django.utils import timezone
from probes.models import Probes


class ModelTestCase(TransactionTestCase):
    def tearDown(self):
        Probes.objects.all().delete()

    def test_probe_should_disallow_spaces_in_hostname(self):
        with self.assertRaises(ValidationError):
            probe = Probes(hostname='with space',
                           description='desc',
                           output_directory='dir',
                           yaml_file='filename',
                           created_date=timezone.now(),
                           updated_date=timezone.now())
            probe.full_clean()

    def test_probe_should_enforce_unique_hostname(self):
        probe1 = Probes(hostname='hostA',
                        description='desc1',
                        output_directory='dir1',
                        yaml_file='filename1',
                        created_date=timezone.now(),
                        updated_date=timezone.now())

        probe2 = Probes(hostname='hostA',
                        description='desc2',
                        output_directory='dir2',
                        yaml_file='filename2',
                        created_date=timezone.now(),
                        updated_date=timezone.now())

        probe1.save()
        self.assertRaises(IntegrityError, probe2.save)

    def test_should_return_most_recently_created_hostnames_reverse_sorted_by_creation_date(self):
        probe1 = Probes(hostname='hostA',
                        description='descA',
                        output_directory='dirA',
                        yaml_file='filenameA',
                        created_date=timezone.now(),
                        updated_date=timezone.now())
        probe1.save()

        probe2 = Probes(hostname='hostB',
                        description='descB',
                        output_directory='dirB',
                        yaml_file='filenameB',
                        created_date=timezone.now(),
                        updated_date=timezone.now())
        probe2.save()

        probe3 = Probes(hostname='hostC',
                        description='descC',
                        output_directory='dirC',
                        yaml_file='filenameC',
                        created_date=timezone.now(),
                        updated_date=timezone.now())
        probe3.save()

        ruleset_middleware = 'probes'
        Probe = __import__(ruleset_middleware)
        self.assertEqual(Probe.models.get_probe_hostnames(), ['hostA', 'hostB', 'hostC'])
        self.assertEqual(Probe.models.get_probe_hostnames(limit=2), ['hostB', 'hostC'])
        self.assertEqual(Probe.models.get_probe_hostnames(limit=1), ['hostC'])
