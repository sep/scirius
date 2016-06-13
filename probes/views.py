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

from django.contrib import messages
from django.contrib.messages import get_messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.utils import timezone
from scirius.utils import scirius_render
from probes.models import Probes
from probes.forms import ProbeForm

def process_messages(values):
    for message in values:
        if message.level == messages.ERROR:
            message.extra_tags = 'alert-danger'
        elif message.level == messages.SUCCESS:
            message.extra_tags = 'alert-success'
        elif message.level == messages.WARNING:
            message.extra_tags = 'alert-warning'
        else:
            message.extra_tags = 'alert-info'
    return values

def get_context(request):
    return {
        'probes': Probes.objects.all(),
        'addProbeForm': ProbeForm(),
        'messages': process_messages(get_messages(request))
    }

def index(request, error = None, error_heading = None):
    context = get_context(request)
    context['error'] = error
    context['error_heading'] = error_heading
    return scirius_render(request, 'probes/index.html', context)

def probe(request, probe_id, error = None, error_heading = None):
    context = get_context(request)
    context['current_id'] = int(probe_id)

    try:
        probe = context['probes'].get(id = probe_id)
    except Probes.DoesNotExist:
        messages.error(request, 'The selected probe could not be loaded.')
        return redirect(index)

    context['probe'] = probe
    context['editProbeForm'] = ProbeForm(instance = probe)
    context['error'] = error
    context['error_heading'] = error_heading

    return scirius_render(request, 'probes/probe.html', context)

def delete_probe(request, probe_id):
    if request.method != 'POST':
        return redirect(index)

    try:
        Probes.objects.get(id = probe_id).delete()
    except Probes.DoesNotExist:
        messages.error(request, 'The selected probe was not found.')

    return redirect(index)

def edit_probe(request, probe_id):
    if request.method != 'POST':
        return redirect(index)

    try:
        probe_object = Probes.objects.get(id = probe_id)
    except Probes.DoesNotExist:
        messages.error(request, 'The selected probe was not found.')
        return redirect(index)

    form = ProbeForm(request.POST, instance = probe_object)
    if form.is_valid():
        form.save()
        messages.success(request, 'Update succeeded.')
    else:
        return probe(request, probe_id, form.errors, 'This probe could not be modified because of the following errors:')

    return redirect('probes_probe', probe_id = probe_id)

def add_probe(request):
    if request.method != 'POST':
        return redirect(index)

    form = ProbeForm(request.POST)
    if form.is_valid():
        try:
            probeObject = Probes.objects.create(hostname = form.cleaned_data['hostname'],
                                                description = form.cleaned_data['description'],
                                                output_directory = form.cleaned_data['output_directory'],
                                                created_date = timezone.now(),
                                                updated_date = timezone.now(),
                                                ruleset = form.cleaned_data['ruleset'],
                                                yaml_file = form.cleaned_data['yaml_file'],
                                               )
            return redirect('probes_probe', probe_id = probeObject.id)
        except IntegrityError, error:
            return index(request, error)
    else:
        return index(request, form.errors, 'The probe could not be added because of the following errors:')
