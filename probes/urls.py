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
    url(r'^$', views.greet, name='probes_greet'),
    url(r'^index/([0-9]+)$', views.index_n, name='probes_index_n'),
    url(r'^edit$', views.edit, name='probes_edit'),
    url(r'^edit/([0-9]+)$', views.edit_n, name='probes_edit_n'),
    url(r'^update/([0-9]+)$', views.update_n, name='probes_update_n'),
    url(r'^delete/([0-9]+)$', views.delete_n, name='probes_delete_n'),
    )
