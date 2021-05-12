# Generated by Django 2.2.7 on 2020-09-10 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0004_shipload'),
    ]

    operations = [
        migrations.CreateModel(
            name='SapUploadData',
            fields=[
                ('row_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('sap_value_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='SAP Value')),
                ('transaction_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Transaction Type')),
                ('value_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Value Type')),
                ('transaction_date', models.DateTimeField(blank=True, null=True, verbose_name='Update Date')),
                ('sap_reference_id', models.CharField(blank=True, max_length=30, null=True, verbose_name='SAP Reference Id')),
                ('creator', models.CharField(blank=True, max_length=100, null=True, verbose_name='Creator')),
                ('create_date', models.DateTimeField(blank=True, null=True, verbose_name='Create Date')),
                ('updater', models.CharField(blank=True, max_length=100, null=True, verbose_name='Updater')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.CreateModel(
            name='SapUploadProcess',
            fields=[
                ('sap_reference_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('sap_reference_date', models.DateTimeField(blank=True, null=True, verbose_name='SAP Reference Date')),
                ('transaction_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Transaction Type')),
                ('total_qty', models.IntegerField()),
                ('sap_value_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='SAP Value')),
                ('failed', models.IntegerField()),
                ('returncode', models.IntegerField()),
                ('message', models.CharField(blank=True, max_length=255, null=True, verbose_name='Error Message')),
                ('errorcount', models.IntegerField()),
                ('creator', models.CharField(blank=True, max_length=100, null=True, verbose_name='Creator')),
                ('create_date', models.DateTimeField(blank=True, null=True, verbose_name='Create Date')),
                ('updater', models.CharField(blank=True, max_length=100, null=True, verbose_name='Updater')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.AddField(
            model_name='salesorderdetail',
            name='unit_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='shipload',
            name='seal_value',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Container Number'),
        ),
        migrations.AlterField(
            model_name='deliverynumber',
            name='salesorder_id',
            field=models.ForeignKey(db_column='salesorder_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.SalesOrder'),
        ),
        migrations.AlterField(
            model_name='deliverynumberdetail',
            name='deliverynumber_id',
            field=models.ForeignKey(db_column='deliverynumber_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.DeliveryNumber'),
        ),
        migrations.AlterField(
            model_name='deliverynumberdetail',
            name='salesorder_id',
            field=models.ForeignKey(db_column='salesorder_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.SalesOrder'),
        ),
        migrations.AlterField(
            model_name='deliverynumberdetail',
            name='skuno',
            field=models.ForeignKey(db_column='skuno_id', on_delete=django.db.models.deletion.CASCADE, to='manufacturing.MaterialMaster'),
        ),
        migrations.AlterField(
            model_name='palletdeliverynumber',
            name='deliverynumber_id',
            field=models.ForeignKey(db_column='deliverynumber_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.DeliveryNumber'),
        ),
        migrations.AlterField(
            model_name='palletdeliverynumber',
            name='pallet_id',
            field=models.ForeignKey(db_column='pallet_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.Pallet'),
        ),
        migrations.AlterField(
            model_name='palletserialnumber',
            name='pallet_id',
            field=models.ForeignKey(db_column='pallet_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.Pallet'),
        ),
        migrations.AlterField(
            model_name='palletserialnumber',
            name='serialnumber',
            field=models.ForeignKey(db_column='serial_number', on_delete=django.db.models.deletion.CASCADE, to='manufacturing.SerialNumber'),
        ),
        migrations.AlterField(
            model_name='salesorderdetail',
            name='salesorder_id',
            field=models.ForeignKey(db_column='salesorder_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.SalesOrder'),
        ),
        migrations.AlterField(
            model_name='salesorderdetail',
            name='salesorder_qty',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='salesorderdetail',
            name='ship_qty',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='salesorderdetail',
            name='skuno',
            field=models.ForeignKey(db_column='skuno_id', on_delete=django.db.models.deletion.CASCADE, to='manufacturing.MaterialMaster'),
        ),
        migrations.AlterField(
            model_name='salesorderreturninfo',
            name='salesorder_id',
            field=models.ForeignKey(db_column='salesorder_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.SalesOrder'),
        ),
        migrations.AlterField(
            model_name='salesordershipinfo',
            name='salesorder_id',
            field=models.ForeignKey(db_column='salesorder_id', on_delete=django.db.models.deletion.CASCADE, to='shipping.SalesOrder'),
        ),
        migrations.AddIndex(
            model_name='sapuploaddata',
            index=models.Index(fields=['transaction_type'], name='shipping_sa_transac_9a7b9b_idx'),
        ),
        migrations.AddIndex(
            model_name='sapuploaddata',
            index=models.Index(fields=['sap_reference_id'], name='shipping_sa_sap_ref_8c249c_idx'),
        ),
        migrations.AddIndex(
            model_name='sapuploaddata',
            index=models.Index(fields=['sap_value_id'], name='shipping_sa_sap_val_293b58_idx'),
        ),
    ]
