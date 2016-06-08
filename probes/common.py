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

import psutil
import subprocess
import tempfile
import shutil
import os
import json
import StringIO
import re

from django.conf import settings

class Info():
    def status(self):
        suri_running = False
        return suri_running

    def disk(self):
        return psutil.disk_usage('/')

    def memory(self):
        return psutil.virtual_memory()

