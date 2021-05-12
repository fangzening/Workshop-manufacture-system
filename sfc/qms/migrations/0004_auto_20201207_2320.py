# Generated by Django 2.2.7 on 2020-12-07 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0013_auto_20201116_1006'),
        ('wms', '0002_auto_20201201_1153'),
        ('qms', '0003_TB_INCOMING_IQC_LIST'),
    ]

    operations = [
        migrations.CreateModel(
            name='bs_aql_value',
            fields=[
                ('aql_value', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('creator', models.CharField(max_length=50)),
                ('create_date', models.DateField(auto_now=True)),
                ('updater', models.CharField(max_length=255, null=True)),
                ('update_date', models.DateField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.CreateModel(
            name='bs_inspection_free_list',
            fields=[
                ('row_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('creator', models.CharField(max_length=50)),
                ('create_date', models.DateField(auto_now=True)),
                ('updater', models.CharField(max_length=255, null=True)),
                ('update_date', models.DateField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.CreateModel(
            name='bs_inspection_level',
            fields=[
                ('inspection_level', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('creator', models.CharField(max_length=50)),
                ('create_date', models.DateField(auto_now=True)),
                ('updater', models.CharField(max_length=255, null=True)),
                ('update_date', models.DateField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.CreateModel(
            name='bs_inspection_tool',
            fields=[
                ('inspection_tool', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('creator', models.CharField(max_length=50)),
                ('create_date', models.DateField(auto_now=True)),
                ('updater', models.CharField(max_length=255, null=True)),
                ('update_date', models.DateField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.CreateModel(
            name='bs_manufacture_data',
            fields=[
                ('manufacture_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('manufacture_part_no', models.CharField(max_length=255)),
                ('manufacture_name', models.CharField(max_length=255)),
                ('creator', models.CharField(max_length=50)),
                ('create_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='incoming_iqc_list',
            fields=[
                ('incoming_list_id', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('inspected', models.IntegerField(blank=True, choices=[(0, 'Not Inspected'), (1, 'Inspected')], default='Not Inspected', help_text='Inspected', null=True)),
                ('material_qty', models.IntegerField(blank=True, default=0)),
                ('create_date', models.DateField(auto_now=True)),
                ('model_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manufacturing.MaterialMaster')),
            ],
        ),
        migrations.CreateModel(
            name='insp_param_catalogue',
            fields=[
                ('inspect_parameters_id', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('creator', models.CharField(max_length=50)),
                ('create_date', models.DateField(auto_now=True)),
                ('updater', models.CharField(max_length=255, null=True)),
                ('update_date', models.DateField(blank=True, null=True, verbose_name='Update Date')),
            ],
        ),
        migrations.CreateModel(
            name='insp_reuslt',
            fields=[
                ('row_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('insp_reuslt', models.IntegerField(blank=True, choices=[(0, 'FAIL'), (1, 'PASS')], default='PASS', null=True)),
                ('insp_model_parameter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qms.insp_param_catalogue')),
            ],
        ),
        migrations.CreateModel(
            name='iqc_inspection',
            fields=[
                ('inspection_form_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('material_qty', models.IntegerField(default=0)),
                ('inspection_date', models.DateField(blank=True, null=True, verbose_name='Update Date')),
                ('is_inspection_free', models.IntegerField(choices=[(0, 'NO'), (1, 'YES')], default=0)),
                ('inspection_operator', models.CharField(max_length=255, null=True)),
                ('inspection_result', models.CharField(max_length=255, null=True)),
                ('sampling_number', models.IntegerField(default=0)),
                ('creator', models.CharField(max_length=255, null=True)),
                ('create_date', models.DateField(auto_now=True)),
                ('updater', models.CharField(max_length=255, null=True)),
                ('update_date', models.DateField(blank=True, null=True, verbose_name='Update Date')),
                ('status', models.IntegerField(choices=[(0, 'NOT COMPLETED'), (1, 'COMPLETED')], default=0)),
                ('document_sts', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='iqc_maintenance',
            fields=[
                ('inspection_detail_id', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('inspection_method', models.CharField(max_length=255)),
                ('inspection_standard', models.CharField(max_length=255)),
                ('aql_value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qms.bs_aql_value')),
                ('inspection_level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qms.bs_inspection_level')),
                ('inspection_tool', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qms.bs_inspection_tool')),
                ('model_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manufacturing.MaterialMaster')),
            ],
        ),
        migrations.CreateModel(
            name='material_inspection_parameter',
            fields=[
                ('insp_model_parameter_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('creator', models.CharField(max_length=50)),
                ('create_date', models.DateField(auto_now=True)),
                ('inspection_parameter_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qms.insp_param_catalogue')),
                ('model_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manufacturing.MaterialMaster')),
            ],
        ),
        migrations.CreateModel(
            name='mrb',
            fields=[
                ('mrb_form_id', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('mrb_result', models.CharField(max_length=255)),
                ('selected_number', models.CharField(max_length=255)),
                ('audit_person', models.CharField(max_length=255)),
                ('audit_date', models.DateField()),
                ('inspection_form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qms.iqc_inspection')),
            ],
        ),
        migrations.RemoveField(
            model_name='tb_incoming_iqc_list',
            name='material_hh_part_number',
        ),
        migrations.RemoveField(
            model_name='tb_iqc_inspection',
            name='inspection_aql_value',
        ),
        migrations.RemoveField(
            model_name='tb_iqc_inspection',
            name='inspection_level',
        ),
        migrations.RemoveField(
            model_name='tb_iqc_inspection',
            name='inspection_parameters',
        ),
        migrations.RemoveField(
            model_name='tb_iqc_inspection',
            name='inspection_tool',
        ),
        migrations.RemoveField(
            model_name='tb_iqc_inspection',
            name='is_inspection_free',
        ),
        migrations.RemoveField(
            model_name='tb_iqc_inspection',
            name='material_hh_part_number',
        ),
        migrations.RemoveField(
            model_name='tb_material_inspection_free_list',
            name='material_hh_part_number',
        ),
        migrations.RemoveField(
            model_name='tb_material_inspection_free_list',
            name='material_manufacture_data',
        ),
        migrations.RemoveField(
            model_name='tb_mrb',
            name='inspection_form_id',
        ),
        migrations.DeleteModel(
            name='TB_BS_INSPEC_AQL_VALUE',
        ),
        migrations.DeleteModel(
            name='TB_BS_INSPEC_LEVEL',
        ),
        migrations.DeleteModel(
            name='TB_BS_INSPEC_PARAMETERS',
        ),
        migrations.DeleteModel(
            name='TB_BS_INSPECTION_TOOL',
        ),
        migrations.DeleteModel(
            name='TB_INCOMING_IQC_LIST',
        ),
        migrations.DeleteModel(
            name='TB_IQC_INSPECTION',
        ),
        migrations.DeleteModel(
            name='TB_MANUFACTURE_DATA',
        ),
        migrations.DeleteModel(
            name='TB_MATERIAL_INSPECTION_FREE_LIST',
        ),
        migrations.DeleteModel(
            name='TB_MRB',
        ),
        migrations.AddField(
            model_name='iqc_inspection',
            name='inspection_detail_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qms.iqc_maintenance'),
        ),
        migrations.AddField(
            model_name='iqc_inspection',
            name='receiving_form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wms.receiving_form'),
        ),
        migrations.AddField(
            model_name='insp_reuslt',
            name='inspection_form_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qms.iqc_inspection'),
        ),
        migrations.AddField(
            model_name='bs_inspection_free_list',
            name='manufacture_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='qms.bs_manufacture_data'),
        ),
        migrations.AddField(
            model_name='bs_inspection_free_list',
            name='model_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manufacturing.MaterialMaster', unique=True),
        ),
    ]