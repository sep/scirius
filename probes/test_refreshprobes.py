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

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.six import StringIO
from unittest import skipIf

from probes.models import Probes
from rules.models import Ruleset

try:
    from mock import Mock, MagicMock, patch, call

    no_mock_support = False
except ImportError:
    no_mock_support = True


class SimpleTestCase(TestCase):
    def setUp(self):
        Probes.objects.create(hostname='probe1',
                              description='the probe description',
                              output_directory='dir',
                              yaml_file='filename',
                              created_date='2016-01-01T12:23:34.000Z',
                              updated_date='2016-01-02T12:23:34.000Z')

    def tearDown(self):
        Probes.objects.all().delete()

    def test_should_require_update_or_build_action(self):
        with self.assertRaisesRegexp(CommandError, '''You\ must\ specify\ \-u\ and\/or\ \-b'''):
            call_command('refreshprobes', 'someprobe')

    def test_should_display_missing_probe_error_when_referencing_unknown_probe(self):
        with self.assertRaisesRegexp(CommandError,
                                     '''The\ following\ specified\ probes\ are\ invalid\:\ p2, p1'''):
            call_command('refreshprobes', '-u', 'p1', 'p2')

    def test_should_warn_about_update_skipping_probe_that_has_no_assigned_ruleset(self):
        out = StringIO()
        err = StringIO()
        call_command('refreshprobes', '-u', 'probe1', stdout=out, stderr=err)
        self.assertIn('Warning: skipping update for probe "probe1" because it has no ruleset', err.getvalue())

    def test_should_warn_about_build_skipping_probe_that_has_no_assigned_ruleset(self):
        out = StringIO()
        err = StringIO()
        call_command('refreshprobes', '-b', 'probe1', stdout=out, stderr=err)
        self.assertIn('Warning: skipping build for probe "probe1" because it has no ruleset', err.getvalue())


@skipIf(no_mock_support, "Mock support not found; please run 'pip install mock'.")
class AdvancedTestCase(TestCase):
    def setUp(self):
        self.ruleset1 = Ruleset.objects.create(name='ruleset1',
                                               descr='rulseset description',
                                               created_date='2016-01-01T12:23:34.000Z',
                                               updated_date='2016-01-02T12:23:34.000Z')

        self.probe1 = Probes.objects.create(hostname='probe1',
                                            description='the probe description',
                                            output_directory='dir',
                                            yaml_file='filename',
                                            created_date='2016-01-01T12:23:34.000Z',
                                            updated_date='2016-01-02T12:23:34.000Z',
                                            ruleset=self.ruleset1)

    def tearDown(self):
        Probes.objects.all().delete()
        Ruleset.objects.all().delete()

    def test_should_build_rules(self):
        out = StringIO()
        err = StringIO()
        build_mock = Mock()
        with patch('probes.models.Probes.build_rules', build_mock):
            call_command('refreshprobes', '-b', 'probe1', stdout=out, stderr=err)

        build_mock.assert_called_once()
        self.assertIn('Build complete', out.getvalue())
        self.assertEqual('', err.getvalue())

    def test_should_update_ruleset(self):
        out = StringIO()
        err = StringIO()
        update_mock = Mock()
        with patch('rules.models.Ruleset.update', update_mock):
            call_command('refreshprobes', '-u', 'probe1', stdout=out, stderr=err)

        update_mock.assert_called_once()
        self.assertIn('Update complete', out.getvalue())
        self.assertEqual('', err.getvalue())

    def test_should_update_before_building(self):
        out = StringIO()
        err = StringIO()
        parent_mock = Mock()
        build_mock = Mock()
        update_mock = Mock()
        parent_mock.build = build_mock
        parent_mock.update = update_mock
        with patch('probes.models.Probes.build_rules', build_mock), patch('rules.models.Ruleset.update', update_mock):
            call_command('refreshprobes', '-bu', 'probe1', stdout=out, stderr=err)

        parent_mock.assert_has_calls([call.update(), call.build()])
