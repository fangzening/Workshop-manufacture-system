# Generated by Django 2.2.7 on 2020-09-10 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0005_auto_20200910_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pallet',
            old_name='created_date',
            new_name='create_date',
        ),
    ]
