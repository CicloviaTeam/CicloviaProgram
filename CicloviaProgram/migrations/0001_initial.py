# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArrivalsProportionPerHour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hour', models.FloatField(default=1)),
                ('proportion', models.FloatField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Ciclovia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('place', models.CharField(max_length=20)),
                ('start_hour', models.FloatField(default=0)),
                ('end_hour', models.FloatField(default=0)),
                ('num_tracks', models.IntegerField(default=1)),
                ('reference_track', models.IntegerField(default=0)),
                ('reference_hour', models.IntegerField(default=0)),
                ('reference_arrival_rate', models.FloatField(default=0)),
                ('arrivals_loaded', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=100)),
                ('docfile', models.FileField(upload_to=b'documents/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='NeighboorInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('neighboorId', models.IntegerField(default=1)),
                ('probability', models.FloatField(default=1)),
                ('direction', models.CharField(max_length=10)),
                ('fromDirection', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity', models.CharField(max_length=30)),
                ('velocity', models.FloatField(default=1)),
                ('percentage', models.FloatField(default=1)),
                ('ciclovia', models.ForeignKey(to='CicloviaProgram.Ciclovia')),
            ],
        ),
        migrations.CreateModel(
            name='SimulationParameters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('replications', models.FloatField(default=1)),
                ('arrivals_probability_distribution', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SimulationResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name=b'date executed')),
                ('sim_time', models.FloatField(default=0)),
                ('total_arrivals', models.IntegerField(default=0)),
                ('average_time', models.FloatField(default=0)),
                ('standard_deviation_time', models.FloatField(default=0)),
                ('average_number_system', models.FloatField(default=0)),
                ('is_validation', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SimulationResultsCompiled',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(verbose_name=b'date executed')),
                ('num_runs', models.FloatField(default=0)),
                ('avg_total_arrivals', models.IntegerField(default=0)),
                ('stdev_total_arrivals', models.IntegerField(default=0)),
                ('hw_total_arrivals', models.IntegerField(default=0)),
                ('average_number_system', models.FloatField(default=0)),
                ('stdev_number_system', models.FloatField(default=0)),
                ('hw_number_system', models.FloatField(default=0)),
                ('is_validation', models.BooleanField(default=False)),
                ('ciclovia', models.ForeignKey(to='CicloviaProgram.Ciclovia')),
            ],
        ),
        migrations.CreateModel(
            name='SimulationResultsCompiledFlowTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hour', models.IntegerField(default=0)),
                ('avg_flow_hour', models.FloatField(default=0)),
                ('stdev_flow_hour', models.FloatField(default=0)),
                ('hw_flow_hour', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SimulationResultsCompiledPerTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('track', models.IntegerField(default=0)),
                ('average_number_track', models.IntegerField(default=0)),
                ('stdev_number_track', models.IntegerField(default=0)),
                ('hw_number_track', models.IntegerField(default=0)),
                ('average_total_arrivals', models.IntegerField(default=0)),
                ('stdev_total_arrivals', models.IntegerField(default=0)),
                ('hw_total_arrivals', models.IntegerField(default=0)),
                ('average_total_flow', models.IntegerField(default=0)),
                ('stdev_total_flow', models.IntegerField(default=0)),
                ('hw_total_flow', models.IntegerField(default=0)),
                ('simulation_compiled', models.ForeignKey(to='CicloviaProgram.SimulationResultsCompiled')),
            ],
        ),
        migrations.CreateModel(
            name='SimulationResultsFlowPerTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hour', models.IntegerField(default=0)),
                ('flow_hour', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SimulationResultsPerTrack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('track', models.IntegerField(default=0)),
                ('total_arrivals', models.IntegerField(default=0)),
                ('total_flow', models.FloatField(default=0)),
                ('average_number_track', models.IntegerField(default=0)),
                ('simulation', models.ForeignKey(to='CicloviaProgram.SimulationResults')),
            ],
        ),
        migrations.CreateModel(
            name='TimeInSystemDistribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.FloatField(default=1)),
                ('percentage', models.FloatField(default=1)),
                ('ciclovia', models.ForeignKey(to='CicloviaProgram.Ciclovia')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_track', models.IntegerField(default=100)),
                ('distance', models.FloatField(default=1)),
                ('probability', models.FloatField(default=1)),
                ('probabilityBegin', models.FloatField(default=1)),
                ('probabilityEnd', models.FloatField(default=1)),
                ('arrival_proportion', models.FloatField(default=1)),
                ('ciclovia', models.ForeignKey(to='CicloviaProgram.Ciclovia')),
            ],
        ),
        migrations.AddField(
            model_name='simulationresultsflowpertrack',
            name='track_simulation',
            field=models.ForeignKey(to='CicloviaProgram.SimulationResultsPerTrack'),
        ),
        migrations.AddField(
            model_name='simulationresultscompiledflowtrack',
            name='track_simulation',
            field=models.ForeignKey(to='CicloviaProgram.SimulationResultsCompiledPerTrack'),
        ),
        migrations.AddField(
            model_name='simulationresults',
            name='ciclovia',
            field=models.ForeignKey(to='CicloviaProgram.SimulationResultsCompiled'),
        ),
        migrations.AddField(
            model_name='neighboorinfo',
            name='track',
            field=models.ForeignKey(to='CicloviaProgram.Track'),
        ),
        migrations.AddField(
            model_name='arrivalsproportionperhour',
            name='ciclovia',
            field=models.ForeignKey(to='CicloviaProgram.Ciclovia'),
        ),
    ]
