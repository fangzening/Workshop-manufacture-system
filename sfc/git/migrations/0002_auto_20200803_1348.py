# Generated by Django 2.2.7 on 2020-08-03 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('git', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='casesn',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='mem',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='config',
            name='nic',
            field=models.CharField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='config',
            name='others',
            field=models.CharField(max_length=255, null=True),
        ),
    ]