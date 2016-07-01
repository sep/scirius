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


class SimpleTestCase(TestCase):
    def test_should_require_update_or_build_action(self):
        with self.assertRaisesRegexp(CommandError, '''You\ must\ specify\ \-u\ and\/or\ \-b'''):
            call_command('refreshprobes', 'someprobe')

    def test_should_display_missing_probe_error_when_referencing_unknown_probe(self):
        with self.assertRaisesRegexp(CommandError,
                                     '''The\ following\ specified\ probes\ are\ invalid\:\ p2, p1'''):
            call_command('refreshprobes', '-u', 'p1', 'p2')
