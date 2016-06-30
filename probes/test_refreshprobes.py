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
from probes.models import Probes


class BadSyntaxTestCase(TestCase):
    def test_should_require_update_or_build_action(self):
        out = StringIO()
        err = StringIO()
        with self.assertRaisesRegexp(CommandError, '''You\ must\ specify\ \-u\ and\/or\ \-b'''):
            call_command('refreshprobes', 'someprobe', stdout=out, stderr=err)
