# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import probes.models


class Migration(migrations.Migration):

    dependencies = [
        ('probes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='probes',
            name='elasticsearch_node',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Elasticsearch node (optional)', validators=[probes.models.validate_hostname]),
        ),
    ]
