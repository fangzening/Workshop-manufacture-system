# Generated by Django 2.2.7 on 2020-08-13 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0007_auto_20200727_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keypart',
            name='cserialnumber',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
