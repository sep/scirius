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

from django import forms
from probes.models import Probes
from forms import *

class ProbesForm(forms.ModelForm):
    class Meta:
        model = Probes
        exclude = ('created_date', 'updated_date')

class ProbesUpdateForm(forms.Form):
    reload = forms.BooleanField(required=False)
    build = forms.BooleanField(required=False)
    push = forms.BooleanField(required=False)
