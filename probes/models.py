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

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

import os

from rules.models import Ruleset

def get_probe_hostnames(limit = 10):
    return None

def validate_hostname(value):
    if ' ' in value:
        raise ValidationError('"%s" cannot contain spaces' % value)

class Probes(models.Model):
    hostname = models.CharField(max_length=100, unique = True, validators = [validate_hostname], error_messages={'unique': 'The entered hostname already exists.'})
    description = models.CharField(max_length=400)
    output_directory = models.CharField('Rules output directory', max_length=400)
    yaml_file = models.CharField('Suricata configuration file', max_length=400)
    created_date = models.DateTimeField('Date created')
    updated_date = models.DateTimeField('Date updated', blank = True)
    ruleset = models.ForeignKey(Ruleset, blank = True, null = True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.hostname
