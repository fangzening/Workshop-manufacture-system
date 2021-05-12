 from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Git(models.Model):
    asset_no_id = models.CharField(primary_key=True, max_length=50)
    status = models.CharField(max_length=30)
    shipment = models.IntegerField()
    deliver_date = models.DateTimeField(null=True, blank=True)
    dest =  models.CharField(max_length=20)
    tracking_no = models.CharField(max_length=30,null=True, blank=True)
    tracking_company = models.CharField(max_length=30,null=True, blank=True)
    po_no = models.CharField(max_length=20)
    etd = models.DateTimeField(null=True, blank=True)
    eta = models.DateTimeField(null=True, blank=True)
    vendor = models.CharField(max_length=20)
    model = models.CharField(max_length=30,null=True, blank=True)
    v_asset_no = models.CharField(max_length=50)
    nsn = models.CharField(max_length=50,null=True, blank=True)
    serialnumber = models.CharField(max_length=50,null=True, blank=True)

    config = models.CharField(max_length=30 )
    sub_config = models.CharField(max_length=30)
    config_description = models.CharField(max_length=30 )
    cpu = models.CharField(max_length=255,null=True, blank=True)
    mem = models.CharField(max_length=255, null=True, blank=True)
    nic = models.CharField(max_length=255, null=True ,blank=True)
    raid = models.CharField(max_length=255, null=True, blank=True)
    disk = models.CharField(max_length=255, null=True, blank=True)
    gpu = models.CharField(max_length=255, null=True, blank=True)
    bmc_mac= models.CharField(max_length=255, null=True,blank=True)
    baseboard = models.CharField(max_length=255, null=True, blank=True)
    bios = models.CharField(max_length=255, null=True, blank=True)
    other = models.CharField(max_length=255, null=True ,blank=True)
    updatetime = models.DateTimeField( null=True, blank=True)
    actual_shipping_address = models.CharField(max_length=100,blank=True)
    receiver = models.CharField(max_length=30, null=True,default=None,blank=True)
    linkman = models.CharField(max_length=30,blank=True)
    telephone = models.CharField(max_length=30,blank=True)
    rdr_reason = models.CharField(max_length=30, null=True, default=None,blank=True)
    

    def __str__(self):
        return self.asset_no_id

class Config(models.Model):
    assettag_id = models.CharField(primary_key=True, max_length=50)
    application = models.CharField(max_length=30)
    brand = models.CharField(max_length=20)
    product_name = models.CharField(max_length=30)
    serialnumber = models.CharField(max_length=50)
    cpu = models.CharField(max_length=255)
    mem = models.CharField(max_length=2000)
    nic = models.CharField(max_length=2000)
    raid = models.CharField(max_length=255)
    disk = models.CharField(max_length=255)
    gpu = models.CharField(max_length=255)
    bmc = models.CharField(max_length=255)
    baseboard = models.CharField(max_length=255)
    bios = models.CharField(max_length=255)
    casesn = models.CharField(max_length=255, null=True)
    others = models.CharField(max_length=255, null=True)
    ipmi = models.CharField(max_length=255,null=True,blank=True)