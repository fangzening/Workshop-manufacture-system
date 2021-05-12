# Generated by Django 2.2.7 on 2020-08-03 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('assettag_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('application', models.CharField(max_length=30)),
                ('brand', models.CharField(max_length=20)),
                ('product_name', models.CharField(max_length=30)),
                ('serialnumber', models.CharField(max_length=50)),
                ('cpu', models.CharField(max_length=255)),
                ('mem', models.CharField(max_length=255)),
                ('nic', models.CharField(max_length=255)),
                ('raid', models.CharField(max_length=255)),
                ('disk', models.CharField(max_length=255)),
                ('gpu', models.CharField(max_length=255)),
                ('bmc', models.CharField(max_length=255)),
                ('baseboard', models.CharField(max_length=255)),
                ('bios', models.CharField(max_length=255)),
                ('casesn', models.CharField(max_length=255)),
                ('others', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Git',
            fields=[
                ('asset_no_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=30)),
                ('shipment', models.IntegerField()),
                ('deliver_date', models.DateTimeField(blank=True, null=True)),
                ('dest', models.CharField(max_length=20)),
                ('tracking_no', models.CharField(blank=True, max_length=30, null=True)),
                ('tracking_company', models.CharField(blank=True, max_length=30, null=True)),
                ('po_no', models.CharField(max_length=20)),
                ('etd', models.DateTimeField(blank=True, null=True)),
                ('eta', models.DateTimeField(blank=True, null=True)),
                ('vendor', models.CharField(max_length=20)),
                ('model', models.CharField(blank=True, max_length=30, null=True)),
                ('v_asset_no', models.CharField(max_length=50)),
                ('nsn', models.CharField(blank=True, max_length=50, null=True)),
                ('serialnumber', models.CharField(blank=True, max_length=50, null=True)),
                ('config', models.CharField(max_length=30)),
                ('sub_config', models.CharField(max_length=30)),
                ('config_description', models.CharField(max_length=30)),
                ('cpu', models.CharField(blank=True, max_length=255, null=True)),
                ('mem', models.CharField(blank=True, max_length=255, null=True)),
                ('nic', models.CharField(blank=True, max_length=255, null=True)),
                ('raid', models.CharField(blank=True, max_length=255, null=True)),
                ('disk', models.CharField(blank=True, max_length=255, null=True)),
                ('gpu', models.CharField(blank=True, max_length=255, null=True)),
                ('bmc_mac', models.CharField(blank=True, max_length=255, null=True)),
                ('baseboard', models.CharField(blank=True, max_length=255, null=True)),
                ('bios', models.CharField(blank=True, max_length=255, null=True)),
                ('other', models.CharField(blank=True, max_length=255, null=True)),
                ('updatetime', models.DateTimeField(blank=True, null=True)),
                ('actual_shipping_address', models.CharField(max_length=100)),
                ('receiver', models.CharField(default=None, max_length=30, null=True)),
                ('linkman', models.CharField(max_length=30)),
                ('telephone', models.CharField(max_length=30)),
                ('rdr_reason', models.CharField(default=None, max_length=30, null=True)),
            ],
        ),
    ]
