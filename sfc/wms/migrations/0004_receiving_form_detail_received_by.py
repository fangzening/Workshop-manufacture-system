# Generated by Django 2.2.7 on 2020-12-08 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wms', '0003_auto_20201207_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiving_form_detail',
            name='received_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
