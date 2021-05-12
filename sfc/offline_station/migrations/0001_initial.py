# Generated by Django 2.2.7 on 2020-07-23 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhantomAssy',
            fields=[
                ('phantom_serialnumber', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('phantom_partno', models.CharField(max_length=30)),
                ('phantom_genereated_sn', models.CharField(max_length=50)),
                ('partno', models.CharField(max_length=30)),
                ('cserialno', models.CharField(max_length=50)),
                ('offline_station', models.CharField(max_length=50)),
                ('wh_confirmation', models.CharField(max_length=50)),
                ('creator', models.CharField(max_length=50)),
                ('creator_date', models.DateTimeField()),
                ('updater', models.CharField(max_length=50, null=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]