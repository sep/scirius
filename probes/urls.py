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

from django.conf.urls import patterns, url

from probes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='probes_index'),
    url(r'^(?P<probe_id>\d+)/$', views.probe_index, name='probes_probe'),
    url(r'^(?P<probe_id>\d+)/build$', views.build_probe, name='probes_build'),
    url(r'^(?P<probe_id>\d+)/edit$', views.edit_probe, name='probes_edit'),
    url(r'^(?P<probe_id>\d+)/delete$', views.delete_probe, name='probes_delete'),
    url(r'^(?P<probe_id>\d+)/update$', views.update_ruleset, name='probes_update_ruleset'),
    url(r'^add$', views.add_probe, name='probes_add'),
    )
