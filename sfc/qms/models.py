from django.db import models

# Create your models here.

class bs_inspection_free_list(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    manufacture_id = models.ForeignKey('bs_manufacture_data', on_delete=models.SET_NULL, null=True)
    model_id = models.ForeignKey('manufacturing.MaterialMaster', on_delete=models.SET_NULL, null=True,unique=True)
    creator = models.CharField(max_length=50,null=False, blank=False)
    create_date = models.DateField(auto_now=True,null=False,blank=False)
    updater = models.CharField(max_length=255, null=True)
    update_date = models.DateField('Update Date', null=True, blank=True)



class bs_manufacture_data(models.Model):
    manufacture_id = models.AutoField(auto_created=True, primary_key=True)
    manufacture_part_no = models.CharField(max_length=255,null=False, blank=False)
    manufacture_name = models.CharField(max_length=255, null=False, blank=False)
    creator = models.CharField(max_length=50,null=False, blank=False)
    create_date = models.DateField(auto_now=True,null=False,blank=False)

    def __str__(self):
        return str(self.manufacture_part_no)


class iqc_inspection(models.Model):
    inspection_form_id = models.CharField(max_length=255, null = False, primary_key=True)
    material_qty = models.IntegerField(default=0)
    inspection_date = models.DateField('Update Date', null=True, blank=True)

    IS_INSP_FREE_TYPE = (
        (0, 'NO'),
        (1, 'YES'),
    )
    is_inspection_free = models.IntegerField(
        choices=IS_INSP_FREE_TYPE,
        default=0,
    )

    inspection_operator= models.CharField(max_length=255,null=True)
    inspection_detail_id = models.ForeignKey('iqc_maintenance', on_delete=models.CASCADE, null=True)
    inspection_result = models.CharField(max_length=255,null=True)
    sampling_number = models.IntegerField(default=0)
    receiving_form = models.ForeignKey('wms.receiving_form', on_delete=models.CASCADE, null=True)
    creator = models.CharField(max_length=255, null = True)
    create_date = models.DateField(auto_now=True, null=False,blank=False)
    updater = models.CharField(max_length = 255, null = True)
    update_date = models.DateField('Update Date', null=True, blank=True)
    COMPLETE_TYPE = (
        (0, 'NOT COMPLETED'),
        (1, 'COMPLETED'),
    )
    status = models.IntegerField(
        choices = COMPLETE_TYPE,
        default=0,
    )
    document_sts = models.CharField(max_length=255,null=True)

    def __str__(self):
        return str(self.inspection_form_id)

class mrb(models.Model):
    mrb_form_id = models.CharField(max_length = 200, null = False, primary_key = True,  unique=True)
    inspection_form_id = models.ForeignKey('iqc_inspection', on_delete=models.CASCADE)
    mrb_result = models.CharField(max_length=255)
    selected_number = models.IntegerField(default=0)
    audit_person = models.CharField(max_length=255)
    audit_date = models.DateField()

    def __str__(self):
        """String for representing the Model object."""
        return self.mrb_form_id


class insp_param_catalogue(models.Model):  # qms_insp_param_catalogue
    inspect_parameters_id = models.CharField(max_length = 200, null = False, primary_key = True,  unique=True)
    creator = models.CharField(max_length=50,null=False, blank=False)
    create_date = models.DateField(auto_now=True,null=False,blank=False)
    updater = models.CharField(max_length=255, null=True)
    update_date = models.DateField('Update Date', null=True, blank=True)

class bs_aql_value(models.Model):
    aql_value = models.CharField(max_length = 200, null = False, primary_key = True,  unique=True)
    creator = models.CharField(max_length=50,null=False, blank=False)
    create_date = models.DateField(auto_now=True,null=False,blank=False)
    updater = models.CharField(max_length=255, null=True)
    update_date = models.DateField('Update Date', null=True, blank=True)

class bs_inspection_level(models.Model):
    inspection_level = models.CharField(max_length = 200, null = False, primary_key = True,  unique=True)
    creator = models.CharField(max_length=50,null=False, blank=False)
    create_date = models.DateField(auto_now=True,null=False,blank=False)
    updater = models.CharField(max_length=255, null=True)
    update_date = models.DateField('Update Date', null=True, blank=True)

    def __str__(self):
        return str(self.inspection_level)

class bs_inspection_tool(models.Model):
    inspection_tool = models.CharField(max_length = 200, null = False, primary_key = True,  unique=True)
    creator = models.CharField(max_length=50,null=False, blank=False)
    create_date = models.DateField(auto_now=True,null=False,blank=False)
    updater = models.CharField(max_length=255, null=True)
    update_date = models.DateField('Update Date', null=True, blank=True)

    def __str__(self):
        return str(self.inspection_tool)

class incoming_iqc_list(models.Model):
    incoming_list_id = models.CharField(max_length = 200, null = False, primary_key = True,  unique=True)
    model_id = models.ForeignKey('manufacturing.MaterialMaster', on_delete=models.SET_NULL, null=True)
    INSPECTED_TYPE = (
        (0, 'Not Inspected'),
        (1, 'Inspected'),
    )
    inspected = models.IntegerField(
        choices=INSPECTED_TYPE,
        null=True, blank=True,
        default='Not Inspected',
        help_text='Inspected',
    )
    material_qty = models.IntegerField(default=0, blank=True)
    create_date = models.DateField(auto_now=True, null=False, blank=False)

class iqc_maintenance(models.Model):
    inspection_detail_id = models.CharField(max_length=200, null=False, primary_key=True, unique=True)
    # should use uuid? or autofield
    model_id = models.ForeignKey('manufacturing.MaterialMaster', on_delete=models.SET_NULL, null=True,unique=False)
    inspection_method = models.CharField(max_length=255, null=False)
    aql_value = models.ForeignKey('bs_aql_value', on_delete=models.CASCADE, null=True)
    inspection_level = models.ForeignKey('bs_inspection_level', on_delete=models.CASCADE, null=True)
    # inspection_parameters = models.ForeignKey('TB_BS_INSPEC_PARAMETERS', on_delete=models.CASCADE, null=True)
    inspection_tool = models.ForeignKey('bs_inspection_tool', on_delete=models.CASCADE, null=True)
    inspection_standard = models.CharField(max_length=255)

    def __str__(self):
        return str(self.inspection_detail_id)

class material_inspection_parameter(models.Model):
    insp_model_parameter_id = models.AutoField(auto_created=True, primary_key=True)
    model_id = models.ForeignKey('manufacturing.MaterialMaster', on_delete=models.SET_NULL, null=True, unique=False)
    inspection_parameter_id = models.ForeignKey('insp_param_catalogue', on_delete=models.CASCADE, null=True)
    creator = models.CharField(max_length=50, null=False, blank=False)
    create_date = models.DateField(auto_now=True, null=False, blank=False)

class insp_reuslt(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    inspection_form_id = models.ForeignKey('iqc_inspection', on_delete=models.CASCADE)
    insp_model_parameter_id = models.ForeignKey('insp_param_catalogue', on_delete=models.CASCADE)

    INSPECTED_TYPE = (
        (0, 'FAIL'),
        (1, 'PASS'),
    )
    insp_reuslt = models.IntegerField(
        choices=INSPECTED_TYPE,
        null=True, blank=True,
        default='PASS'
    )





