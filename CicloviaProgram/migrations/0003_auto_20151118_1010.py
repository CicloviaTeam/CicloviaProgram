# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CicloviaProgram', '0002_ciclovia_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='hasSlope',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='track',
            name='number_of_semaphores',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='track',
            name='quality_of_track',
            field=models.IntegerField(default=1),
        ),
    ]
