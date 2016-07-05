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

from django.core.management.base import BaseCommand, CommandError
from probes.models import Probes


class Command(BaseCommand):
    help = 'Allows updating and building probe rules'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--update', action='store_true', help='update ruleset sources')
        parser.add_argument('-b', '--build', action='store_true', help='build rules')
        parser.add_argument('probe', nargs='*', help='space-separated probe hostnames')

    def handle(self, *args, **options):
        if (not options['update'] and not options['build']):
            raise CommandError('You must specify -u and/or -b')

        unique_probes = set(options['probe'])
        selected_probes = Probes.objects.filter(hostname__in=unique_probes)
        if (len(unique_probes) != len(selected_probes)):
            selected_probe_names = [p.hostname for p in selected_probes]
            raise CommandError('The following specified probes are invalid: %s' %
                               ", ".join(list(unique_probes - set(selected_probe_names))))

        if (not selected_probes):
            selected_probes = Probes.objects.all()

        if (options['update']):
            self.stdout.write('Updating sources...')
            for probe in selected_probes:
                if not probe.ruleset:
                    self.stderr.write(
                        'Warning: skipping update for probe "%s" because it has no ruleset' % probe.hostname)
                    continue

                try:
                    probe.ruleset.update()
                except Exception, e:
                    self.stderr.write('Ruleset for probe "%s" could not be updated' % probe.hostname)
                    raise e
            self.stdout.write('Update complete')

        if (options['build']):
            self.stdout.write('Building rules...')
            for probe in selected_probes:
                if not probe.ruleset:
                    self.stderr.write(
                        'Warning: skipping build for probe "%s" because it has no ruleset' % probe.hostname)
                    continue

                try:
                    probe.build_rules()
                except Exception, e:
                    self.stderr.write('Build for probe "%s" failed' % probe.hostname)
                    raise e
            self.stdout.write('Build complete')
