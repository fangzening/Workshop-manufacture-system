# Generated by Django 2.2.7 on 2020-11-16 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0012_workorder_production_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='serialnumber',
            name='completed',
            field=models.IntegerField(choices=[(0, 'NOT COMPLETED'), (1, 'COMPLETED')], default=0, help_text='completed'),
        ),
        migrations.AddField(
            model_name='serialnumber',
            name='shipped',
            field=models.IntegerField(choices=[(0, 'NOT SHIPPED'), (1, 'SHIPPED')], default=0, help_text='shipped'),
        ),
    ]