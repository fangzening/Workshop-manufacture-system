from django.db import models
from django.apps import apps


import uuid

class SalesOrder(models.Model):
    HOLD_TYPE = (
        (0, 'Not hold'),
        (1, 'Hold'),
    )

    CANCELLED_TYPE = (
        (0, 'Not cancelled'),
        (1, 'Cancelled'),
    )

    COMPLETED_TYPE = (
        (0, 'Not completed'),
        (1, 'Completed'),
    )

    salesorder_id = models.CharField(max_length=50, primary_key=True)
    plant_code = models.CharField('Plant Code', max_length=100)
    customer_shipto = models.CharField(max_length=100)
    customer_soldto = models.CharField(max_length=100)
    salesorder_type = models.CharField(max_length=255)
    customer_po = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    customer_name_alt = models.CharField(max_length=255)
    ship_priority = models.CharField(max_length=100)
    sap_create_date = models.DateTimeField('SAP Create Date', null=True, blank=True)
    sap_change_date = models.DateTimeField('SAP Change Date', null=True, blank=True)
    customer_reference = models.CharField(max_length=255)

    completed_date = models.DateTimeField('Completed Date', null=True, blank=True)

    completed = models.IntegerField(
        choices=COMPLETED_TYPE,
        null=True, blank=True,
        help_text='completed',
    )

    ship_hold = models.IntegerField(
        choices=HOLD_TYPE,
        null=True, blank=True,
        help_text='hold',
    )

    ship_cancelled = models.IntegerField(
        choices=CANCELLED_TYPE,
        null=True, blank=True,
        help_text='cancel',
    )
    purchase_order_date = models.DateTimeField(null=True, blank=True)
    ship_date = models.DateTimeField(null=True, blank=True)
    ship_method = models.CharField(max_length=255)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.salesorder_id

    def get_absolute_url(self):
        """Returns the url to access a detail record """
        # return reverse('manufacturing:home')
        return reverse('shipping:ship_out_station', args=[str(self.salesorder_id)])

class SalesOrderDetail(models.Model):
    row_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salesorder_id = models.ForeignKey('SalesOrder', db_column='salesorder_id', on_delete=models.CASCADE, null=False)
    skuno = models.ForeignKey('manufacturing.MaterialMaster', db_column='skuno_id', on_delete=models.CASCADE, null=False)
    salesorder_item = models.CharField(max_length=255)
    salesorder_qty = models.IntegerField(default=0, blank=True)
    ship_qty = models.IntegerField(default=0, blank=True)
    subtotal = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
    customer_po = models.CharField(max_length=255)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)
    unit_price = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.salesorder_id) + str(self.skuno) + str(self.salesorder_item)

    def get_absolute_url(self):
        """Returns the url to access a detail record """
        # return reverse('manufacturing:home')
        return reverse('shipping:ship_out_station', args=[str(self.salesorder_id)])

class SalesOrderShipInfo(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    salesorder_id = models.ForeignKey('SalesOrder', db_column='salesorder_id', on_delete=models.CASCADE, null=False)
    ship_street = models.CharField(max_length=255)
    ship_city = models.CharField(max_length=255)
    ship_state = models.CharField(max_length=255)
    ship_zip = models.CharField(max_length=10)
    ship_country = models.CharField(max_length=100)
    ship_primary_phone = models.CharField(max_length=50)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

class SalesOrderReturnInfo(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    salesorder_id = models.ForeignKey('SalesOrder', db_column='salesorder_id', on_delete=models.CASCADE, null=False)
    return_name = models.CharField(max_length=255)
    return_name_alternative = models.CharField(max_length=255)
    return_street = models.CharField(max_length=255)
    return_city = models.CharField(max_length=255)
    return_state = models.CharField(max_length=255)
    return_zip = models.CharField(max_length=10)
    return_country = models.CharField(max_length=100)
    return_primary_phone = models.CharField(max_length=50)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)



# Create your models here.

class Pallet(models.Model):
    TYPE_MEASURE = (
        ('in', 'in'),
        ('cm', 'cm'),

    )
    TYPE_WEIGHT = (
        ('lbs', 'lbs'),
        ('kg', 'kg'),

    )
    TYPE_STATUS = (
        ( 1, 'open'),
        ( 0, 'closed')
    )

    weight_unit = models.CharField(
        max_length=15,
        choices=TYPE_WEIGHT,
        default='lbs',
        help_text='Weight',
    )

    measure_unit = models.CharField(
        max_length=15,
        choices=TYPE_MEASURE,
        default='in',
        help_text='Dimensions',
    )

    pallet_id = models.CharField(max_length = 200, null = False, primary_key = True,  unique=True)
    status = models.IntegerField(
        choices=TYPE_STATUS,
        default=1,
        help_text='status'
    )

    # model = models.CharField(max_length=255, unique=True)


    create_date = models.DateTimeField('Create Date', null = True, blank = True)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    current_qty = models.IntegerField()
    FULL_TYPE = (
        (0, 'NOT FULL'),
        (1, 'FULL'),
    )
    full = models.IntegerField(
        choices=FULL_TYPE,
        null = True, blank = True,
        help_text='full',
    )
    full_date = models.DateTimeField('Full Date', null = True, blank = True)
    wh_id = models.CharField(max_length = 200, null = False)
    height = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
    length = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
    width = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
    weight = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
    gross_weight = models.DecimalField(max_digits=12, decimal_places=2, default = 0, blank = True)
    net_weight = models.DecimalField(max_digits=12, decimal_places=2, default = 0, blank = True)
    volume_weight = models.DecimalField(max_digits=12, decimal_places=2, default = 0, blank = True)
    updater = models.CharField(max_length = 200, null = False)
    update_date = models.DateTimeField('Update Date', null = True, blank = True)

    # def __str__(self):
    #     return str(self.id)
    def __str__(self):
        """String for representing the Model object."""
        return self.pallet_id

    def get_absolute_url(self):
        """Returns the url to access a detail record """
        # return reverse('manufacturing:home')
        return reverse('shipping:pallet_station', args=[str(self.pallet_id)])

class PalletSerialNumber(models.Model):
    # row_id = models.UUIDField(
    #     primary_key=True, default=uuid.uuid4, editable=False)
    row_id = models.AutoField(auto_created=True, primary_key=True)
    serialnumber = models.ForeignKey('manufacturing.SerialNumber', db_column='serial_number', on_delete=models.CASCADE)
    pallet_id = models.ForeignKey('Pallet', db_column='pallet_id', on_delete=models.CASCADE, null=False)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField(max_length = 200, null = True)
    update_date = models.DateTimeField('Update Date', null = True, blank = True)

    def get_absolute_url(self):
        """Returns the url to access a detail record """
        # return reverse('manufacturing:home')
        return reverse('shipping:pallet_station', args=[str(self.row_id)])




# ##########################################################################################
class PalletDnLog(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    pallet_id = models.CharField(max_length=255)
    deliverynumber_id = models.IntegerField()
    transportation_id = models.CharField(max_length=255)
    carrier = models.CharField(max_length=255)
    scac = models.CharField(max_length=255)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)


class PalletDeliveryNumber(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    pallet_id = models.ForeignKey('Pallet', db_column='pallet_id', on_delete=models.CASCADE, null=False)
    deliverynumber_id = models.ForeignKey('DeliveryNumber', db_column='deliverynumber_id', on_delete=models.CASCADE, null=False)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __int__(self):
        """String for representing the Model object."""
        return self.row_id

    def get_absolute_url(self):
        """Returns the url to access a detail record """
        # return reverse('manufacturing:home')
        return reverse('shipping:ship_out_station', args=[str(self.pallet_id)])


class DeliveryNumber(models.Model):


    SHIPPED_TYPE = (
        (0, 'NOT SHIPPED'),
        (1, 'SHIPPED'),
    )
    shipped = models.IntegerField(
        choices=SHIPPED_TYPE,
        help_text='shipped',
    )

    invoice_no = models.CharField(max_length=250)

    CONFIRMED_TYPE = (
        (0, 'NOT CONFIRMED'),
        (1, 'CONFIRMED'),
    )
    confirmed = models.IntegerField(
        choices=CONFIRMED_TYPE,
        help_text='confirmed',
    )

    confirmed_date = models.DateTimeField(null=True, blank=True)

    CANCELLED_TYPE = (
        (0, 'NOT CANCELLED'),
        (1, 'CANCELLED'),
    )
    cancelled = models.IntegerField(
        choices=CANCELLED_TYPE,
        help_text='cancelled',
    )

    CONFIRMED_856_TYPE = (
        (0, 'NOT CONFIRMED_856'),
        (1, 'CONFIRMED_856'),
    )
    confirmed_856 = models.IntegerField(
        choices=CONFIRMED_856_TYPE,
        help_text='confirmed_856',
    )
    deliverynumber_id = models.CharField(primary_key=True, max_length=255)
    salesorder_id = models.ForeignKey('SalesOrder', db_column='salesorder_id', on_delete=models.CASCADE, null=False)
    customer_po = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    confirmed_856_date = models.DateTimeField(null=True, blank=True)
    ship_date = models.DateTimeField(null=True, blank=True)
    customer_soldto = models.CharField(max_length=255)
    order_type = models.CharField(max_length=255)
    customer_no = models.CharField(max_length=255)
    bill_of_landing = models.CharField(max_length=255)
    plant_code = models.CharField('Plant Code', max_length=100)
    delivery_type = models.CharField(max_length=255)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.deliverynumber_id

    def get_absolute_url(self):
        """Returns the url to access a detail record """
        # return reverse('manufacturing:home')
        return reverse('shipping:deliverynumber_detail', args=[str(self.deliverynumber_id)])


class DeliveryNumberDetail(models.Model):
    row_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skuno = models.ForeignKey('manufacturing.MaterialMaster', db_column='skuno_id', on_delete=models.CASCADE, null=False)
    salesorder_id = models.ForeignKey('SalesOrder', db_column='salesorder_id', on_delete=models.CASCADE, null=False)
    deliverynumber_id = models.ForeignKey('DeliveryNumber', db_column='deliverynumber_id', on_delete=models.CASCADE, null=False)
    salesorder_item = models.CharField(max_length=255)
    request_qty = models.IntegerField(default=0, blank=True)
    current_qty = models.IntegerField(default=0, blank=True)
    ship_qty = models.IntegerField(default=0, blank=True)
    customer_pn = models.CharField(max_length=255)
    customer_po = models.CharField(max_length=255)
    customer_line_item = models.CharField(max_length=255)
    net_weight = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
    net_price = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __int__(self):
        """String for representing the Model object."""
        return self.deliverynumber_id



######################## truck load #####################################
class SapUploadProcess(models.Model):
    sap_reference_id = models.CharField(primary_key=True, max_length=30)
    sap_reference_date = models.DateTimeField('SAP Reference Date', null=True, blank=True)
    transaction_type = models.CharField('Transaction Type', max_length=100, null=True, blank=True)
    total_qty = models.IntegerField()
    sap_value_id = models.CharField('SAP Value', max_length=100, null=True, blank=True)
    failed = models.IntegerField()
    returncode = models.IntegerField()
    message =  models.CharField('Error Message', max_length=255, null=True, blank=True)
    errorcount = models.IntegerField()
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

class SapUploadData(models.Model):
    class Meta:
       indexes = [
            models.Index(fields=['transaction_type',]),
            models.Index(fields=['sap_reference_id',]),
            models.Index(fields=['sap_value_id',]),
        ]

    row_id = models.AutoField(auto_created=True, primary_key=True)
    sap_value_id = models.CharField('SAP Value', max_length=50, null=True, blank=True)
    transaction_type = models.CharField('Transaction Type', max_length=100, null=True, blank=True)
    value_type = models.CharField('Value Type', max_length=100, null=True, blank=True)
    transaction_date = models.DateTimeField('Update Date', null=True, blank=True)
    sap_reference_id = models.CharField('SAP Reference Id', max_length=30, null=True, blank=True)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

class ShipLoad(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    salesorder_id = models.ForeignKey('SalesOrder', db_column='salesorder_id', on_delete=models.CASCADE, null=False)
    deliverynumber_id = models.ForeignKey('DeliveryNumber', db_column='deliverynumber_id', on_delete=models.CASCADE, null=False)
    billoflading_id = models.CharField('Bill of Lading', max_length=50, null=True, blank=True)
    carrier = models.CharField('Carrier', max_length=20, null=True, blank=True)
    seal_value = models.CharField('Container Number', max_length=50, null=True, blank=True)
    container_number = models.CharField('Container Number', max_length=50, null=True, blank=True)
    ship_method = models.CharField('Ship Method', max_length=20, null=True, blank=True)
    ship_date = models.DateTimeField('Ship Date', null=True, blank=True)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)
