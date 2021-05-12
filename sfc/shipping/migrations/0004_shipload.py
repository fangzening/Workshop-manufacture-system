# Generated by Django 2.2.7 on 2020-08-17 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0003_auto_20200814_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShipLoad',
            fields=[
                ('row_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('billoflading_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='Bill of Lading')),
                ('carrier', models.CharField(blank=True, max_length=20, null=True, verbose_name='Carrier')),
                ('container_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='Container Number')),
                ('ship_method', models.CharField(blank=True, max_length=20, null=True, verbose_name='Ship Method')),
                ('ship_date', models.DateTimeField(blank=True, null=True, verbose_name='Ship Date')),
                ('creator', models.CharField(blank=True, max_length=100, null=True, verbose_name='Creator')),
                ('create_date', models.DateTimeField(blank=True, null=True, verbose_name='Create Date')),
                ('updater', models.CharField(blank=True, max_length=100, null=True, verbose_name='Updater')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Update Date')),
                ('deliverynumber_id', models.ForeignKey(db_column='deliverynumber_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.DeliveryNumber')),
                ('salesorder_id', models.ForeignKey(db_column='salesorder_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.SalesOrder')),
            ],
        ),
    ]
