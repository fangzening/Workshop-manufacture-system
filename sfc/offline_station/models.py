from django.db import models

class PhantomAssy(models.Model):
    #phantom serial number cpu serial number
    phantom_serialnumber = models.CharField(max_length=50, primary_key=True)
    #part number cpu part number
    phantom_partno = models.CharField(max_length=30, null=False)
    #generated serial number = same serial number for heat sink
    phantom_generated_sn = models.CharField(max_length=50, null=False)
    #part number, inside phantom assymbly heat sink serial number
    partno = models.CharField(max_length=30, null=False)
    #componnet serial number
    cserialno = models.CharField(max_length=50, null=False)
    offline_station = models.CharField(max_length=50, null=False)
    wh_confirmation = models.CharField(max_length=50, null=False)
    creator = models.CharField(max_length=50)
    creator_date = models.DateTimeField()
    updater = models.CharField(max_length=50, null=True)
    update_date = models.DateTimeField(auto_now=True)

# class PHANTOM_SETTING(models.Model):
#     p_sn = models.CharField(max_length=50, null=False, primary_key=True)
#     p_type = models.CharField(max_length=30, null=False, primary_key=True)
#     scan_type = models.CharField(max_length=30, null=False, primary_key=True)
#     new_sn = models.CharField(max_length=30, null=False, primary_key=True)
#     creator = models.CharField(max_length=50, null=False, primary_key=True)
#     date_code = models.DateField(auto_now=True)
#     updater = models.CharField(max_length=50, null=False, primary_key=True)
#     update_date = models.DateField(auto_now=True)

