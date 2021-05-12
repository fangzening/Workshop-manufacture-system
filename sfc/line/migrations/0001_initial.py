# Generated by Django 2.2.7 on 2020-07-23 15:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('action_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pack',
            fields=[
                ('pack_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('pack_type', models.CharField(choices=[('single', 'single'), ('multi', 'multi')], default='single', help_text='Pack Type', max_length=15)),
                ('status', models.CharField(max_length=50)),
                ('print_label', models.CharField(max_length=50)),
                ('country_kit', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PackSerialNumber',
            fields=[
                ('row_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('updater', models.CharField(blank=True, max_length=20, null=True, verbose_name='Updater')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('route_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('plant_code', models.CharField(max_length=50)),
                ('creator', models.CharField(max_length=20, verbose_name='Creator')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='Create Date')),
                ('updater', models.CharField(blank=True, max_length=20, null=True, verbose_name='Updater')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('station_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('desc', models.TextField(max_length=1000)),
                ('model_partition', models.CharField(default='n', max_length=1)),
                ('creator', models.CharField(max_length=20, verbose_name='Creator')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='Create Date')),
                ('updater', models.CharField(blank=True, max_length=20, null=True, verbose_name='Updater')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('template_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('desc', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateActions',
            fields=[
                ('row_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action_id', models.ForeignKey(db_column='action_id', on_delete=django.db.models.deletion.CASCADE, to='line.Action')),
                ('template_id', models.ForeignKey(db_column='template_id', on_delete=django.db.models.deletion.CASCADE, to='line.Template')),
            ],
        ),
        migrations.CreateModel(
            name='StationRoutes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('FAIL', 'FAIL'), ('PASS', 'PASS')], default='PASS', max_length=255, verbose_name='State')),
                ('sequence', models.IntegerField()),
                ('next_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_station', to='line.Station')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='line.Route')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='station', to='line.Station')),
            ],
        ),
        migrations.AddField(
            model_name='station',
            name='template_id',
            field=models.ForeignKey(db_column='template_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='line.Template'),
        ),
        migrations.AddField(
            model_name='route',
            name='first_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='line.Station'),
        ),
    ]
