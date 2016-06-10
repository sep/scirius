# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import probes.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0046_source_cert_verif'),
    ]

    operations = [
        migrations.CreateModel(
            name='Probes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=100, validators=[probes.models.validate_hostname])),
                ('description', models.CharField(max_length=400)),
                ('output_directory', models.CharField(max_length=400, verbose_name=b'Rules output directory')),
                ('yaml_file', models.CharField(max_length=400, verbose_name=b'Suricata configuration file')),
                ('created_date', models.DateTimeField(verbose_name=b'Date created')),
                ('updated_date', models.DateTimeField(verbose_name=b'Date updated', blank=True)),
                ('ruleset', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='rules.Ruleset', null=True)),
            ],
        ),
    ]
