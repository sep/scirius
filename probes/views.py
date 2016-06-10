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

from django.shortcuts import redirect
from django.utils import timezone
from django.db import IntegrityError

from scirius.utils import scirius_render
from probes.models import Probes
from rules.models import dependencies_check
from forms import *

from django.conf import settings
from rules.views import complete_context


def get_probes():
    return Probes.objects.all()

def get_probe(n):
    try:
        return get_probes().get(id=n)
    except Probes.DoesNotExist:
        return None

def index_n(request, n = -1, error = None):
    probes = get_probes()
    context = {'probes': probes}

    suri = get_probe(n)
    if suri:
        context['suricata'] = suri
        if error:
            context['error'] = error
        if suri.ruleset:
            supp_rules = list(suri.ruleset.suppressed_rules.all())
            if len(supp_rules):
                suppressed = ",".join([ str(x.sid) for x in supp_rules])
                context['suppressed'] = suppressed

        if settings.USE_ELASTICSEARCH:
            context['rules'] = True
            complete_context(request, context)

        return scirius_render(request, 'probes/index.html', context)
    else:
        return redirect(greet)


def greet(request, error = None):
    probes = get_probes()
    context = { 'probes' : probes }
    if error:
        context['error'] = error
    return scirius_render(request, 'probes/greet.html', context)


def edit_n(request, n):

    if not request.user.is_staff:
        return redirect('/')

    probe = get_probe(n)
    if request.method == 'POST':
        if probe:
            probe.updated_date = timezone.now()
            form = ProbesForm(request.POST, instance = probe)
        else:
            form = ProbesForm(request.POST)
        if form.is_valid():
            if probe:
                form.save()
                return redirect(greet)
            try:
                probe = Probes.objects.create(hostname=form.cleaned_data['hostname'],
                                              description=form.cleaned_data['description'],
                                              output_directory=form.cleaned_data['output_directory'],
                                              created_date=timezone.now(),
                                              updated_date=timezone.now(),
                                              ruleset=form.cleaned_data['ruleset'],
                                              yaml_file=form.cleaned_data['yaml_file'],
                                             )
            except IntegrityError, error:
                return scirius_render(request, 'probes/edit.html', { 'form': form, 'error': error })
            return redirect(greet)
        else:
            return scirius_render(request, 'probes/edit.html', { 'form': form, 'error': 'Invalid form' })
    else:
        if probe:
            form = ProbesForm(instance = probe)
        else:
            form = ProbesForm()
    missing = dependencies_check(Probes)

    return scirius_render(request, 'probes/edit.html', { 'form': form, 'missing': missing })


def edit(request):
    return edit_n(request, -1)


def update_n(request, n):
    if not request.user.is_staff:
        return redirect('/')

    suri = get_probe(n)

    if suri == None:
        form = ProbesForm()
        context = { 'creation': True , 'form': form}
        return scirius_render(request, 'probes/edit.html', context)
    if request.method == 'POST':
        form = ProbesUpdateForm(request.POST)
        if not form.is_valid():
            return scirius_render(request, 'probes/update.html', { 'suricata': suri, 'error': "Invalid form"})
        message = []
        if form.cleaned_data['reload']:
            try:
                suri.ruleset.update()
            except IOError, errors:
                return greet(request, error="Can not fetch data: %s" % (errors))
            message.append("Rule downloaded at %s. " % (suri.ruleset.updated_date))
        if form.cleaned_data['build']:
            suri.generate()
            suri.updated_date = timezone.now()
            suri.save()
            message.append("Successful ruleset build at " + str(suri.updated_date))
        if form.cleaned_data['push']:
            ret = suri.push()
            suri.updated_date = timezone.now()
            suri.save()
            if ret:
                message.append("Successful asked ruleset reload at " + str(suri.updated_date))
            else:
                message.append("Suricata restart already asked.")
        context =  { 'message': message, 'suricata': suri }
        return scirius_render(request, 'probes/update.html', context)
    else:
        return scirius_render(request, 'probes/update.html', { 'suricata': suri })


def delete_n(request, n):
    if not request.user.is_staff:
        return redirect('/')

    probe = get_probe(n)

    if request.method == 'POST':
        probe.delete()
        return redirect(greet)
    else:
        context = {'object': probe, 'delfn': 'probes_delete_n'}
        return scirius_render(request, 'probes/delete.html', context)
