from django.db import models


# Create your models here.

class receiving_form(models.Model):
    receiving_form_id = models.CharField(max_length=255, primary_key=True)
    po_no = models.CharField(max_length=255, null=False, blank=True)
    supplier_id = models.CharField(max_length=255, null=False, blank=True)
    customer_id = models.CharField(max_length=255, null=False, blank=True)
    FINISHED_TYPE = (
        (0, 'Not Finished'),
        (1, 'Finished'),
    )
    receiving_form_status = models.IntegerField(
        choices=FINISHED_TYPE,
        blank=True,
        default=0,
    )
    plant_code = models.CharField(max_length=255, null=False, blank=True)
    creator = models.CharField('Creator', max_length=255, null=True, blank=False)
    create_date = models.DateField('Create Date', auto_now_add=True, null=False, blank=False)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        return str(self.receiving_form_id)


class receiving_form_detail(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    line_no = models.CharField(max_length=255, null=True)
    # po_no = models.CharField(max_length=255, null=False, blank=True)
    receiving_form_id = models.ForeignKey('receiving_form', db_column='receiving_form_id', on_delete=models.CASCADE, null=False)
    model_id = models.ForeignKey('manufacturing.MaterialMaster', db_column='skuno_id', on_delete=models.CASCADE, null=False)
    received_qty = models.IntegerField(default=0, blank=True)
    target_qty = models.IntegerField(default=0, blank=True)
    to_iqc_qty = models.IntegerField(default=0, blank=True)
    received_by = models.CharField( max_length=100, null=True, blank=True)
    RECEIVED_TYPE = (
            (0, 'Not Received'),
            (1, 'Received'),
        )
    receiving_status = models.IntegerField(
                choices=RECEIVED_TYPE,
                blank=True,
                default=0,
                help_text='Received',
            )

class gr_document_no(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    po_no = models.CharField(max_length=255, null=True)
    model_id = models.ForeignKey('manufacturing.MaterialMaster', db_column='skuno_id', on_delete=models.CASCADE, null=False)
    qty = models.IntegerField(default=0, blank=True)
    document_no_rtu = models.CharField(max_length=255, null=True)
    inspection_form_id = models.ForeignKey('qms.iqc_inspection', on_delete=models.CASCADE, null=True)
