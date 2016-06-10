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

def index(request):
    return scirius_render(request, 'probes/index.html', get_context(request))

def probe(request, probe_id):
    context = get_context(request)
    context['current_id'] = int(probe_id)

    try:
        probe = context['probes'].get(id = probe_id)
    except Probes.DoesNotExist:
        messages.error(request, 'The selected probe could not be loaded.')
        return redirect(index)

    context['probe'] = probe

    return scirius_render(request, 'probes/probe.html', context)

def add_probe(request):
    if request.method != 'POST':
        redirect(index)

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
            context = get_context(request)
            context['error'] = error
            return scirius_render(request, 'probes/index.html', context)
    else:
        context = get_context(request)
        context['error'] = form.errors
        context['error_heading'] = 'The probe could not be added because of the following errors:'
        return scirius_render(request, 'probes/index.html', context)
