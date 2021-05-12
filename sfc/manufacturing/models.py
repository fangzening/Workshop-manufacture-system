from django.db import models
from django.db import IntegrityError
from django.urls import reverse
import uuid
from django.apps import apps
# Create your models here.
from django.contrib.auth.models import Group
from django import template
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.utils.timezone import make_aware
from api.wip_util.change_status import change_status

register = template.Library()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # user = AutoOneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    create_date = models.DateTimeField('Create Date', auto_now=True, blank=True)
    department = models.CharField(max_length=100, blank=True)

    class Meta:
        permissions = (
            ("can_user_management", "User Manager"),
            ("can_user_view_user_list", "User Manager/ View user list"),
            ("can_add_user", "User Manager/ Add user"),
            ("can_add_permission", "User Manager/ Add permission"),
            ("can_add_profile", "User Manager/ Add profile"),

            ("can_user_delete_user", "User Manager/ Delete user"),
            ("can_user_update_user", "User Manager/ Update user"),

            ("can_add_user_group", "User Manager/ Add user group"),
            ("can_view_user_group_list", "User Manager/ View user group"),

        )

    # def __str__(self):
    #     return self.user
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        # return reverse('manufacturing:home')
        return reverse('manufacturing:users_profiles_list', args=[str(self.pk)])


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()


from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


#############################################################
class WorkOrderDetail(models.Model):
    class Meta:
        unique_together = (('workorder_id', 'model_id'),)

    row_id = models.AutoField(auto_created=True,primary_key=True)
    workorder_id = models.ForeignKey('WorkOrder', db_column='workorder_id', on_delete=models.CASCADE, null=False) #AUFNR
    model_id = models.ForeignKey('MaterialMaster', db_column='model_id', on_delete=models.CASCADE, null=False) #MATNR
    model_desc = models.CharField(max_length=100) #MAKTX
    mc_code = models.CharField(max_length=100)
    scan_mode = models.CharField(max_length=10)
    scanned = models.CharField(max_length=1, default='N')
    alternative_item_group = models.CharField(max_length=100, null=True) #ALPGR
    alternative_item_rank = models.CharField(max_length=100, null=True) #ALPRF    
    base_unit_of_measure = models.CharField(max_length=100, null=True) #MEINS
    batch_number = models.CharField(max_length=100, null=True) #CHARG
    bom_item_number = models.CharField(max_length=100, null=True) #POSNR
    bom_item_text_1 = models.CharField(max_length=100, null=True) #POTX1
    bom_item_text_2 = models.CharField(max_length=100, null=True) #POTX2
    debit_credit_indicator = models.CharField(max_length=100, null=True) #SHKZG
    item_category = models.CharField(max_length=100, null=True) #POSTP   
    item_number_of_reservation = models.IntegerField('Item number of reservation/dependent requirements', null=True) #RSPOS
    material_group = models.CharField(max_length=100, null=True) #MATKL
    parent_skuno = models.CharField(max_length=100, null=True) #BAUGR
    phantom_item_indicator = models.CharField(max_length=100, null=True, blank=True) #DUMPS
    quantity_withdrawn = models.IntegerField(null=True) #ENMNG    
    required_qty = models.IntegerField('Required qty', null=True) #BDMNG
    revision_level = models.CharField(max_length=100, null=True) #REVLV
    storage_location = models.CharField(max_length=100, null=True) #LGORT
    usage_probability_alt_item = models.FloatField('Usage Prob', null=True) #EWAHR
    keypart_group = models.CharField(max_length=100, blank=True) #PACKING_CODE
    installation_point = models.CharField(max_length=2000, blank=True) #EBORT
    bom_usage = models.CharField(max_length=100, blank=True) #MENGE 

    def __str__(self):
        """String for representing the Model object."""
        return str(self.model_id)

    # def get_absolute_url(self):
    #     """Returns the url to access a detail record for this book."""
    #     return reverse('manufacturing:workorder-detail', args=[str(self.id)])


class SerialNumberLog(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    serial_number = models.CharField(max_length=50)
    workorder = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    station = models.CharField(max_length=100)
    in_station_time = models.DateTimeField(auto_now=True)
    user = models.CharField(max_length=50)
    event = models.TextField()
    log_type = models.CharField(max_length=50,null=True)
    sn_status_category =  models.CharField(max_length=50,null=True, default='0')
    sequence = models.IntegerField(default=0)
    result = models.IntegerField(default=0)
    
    def __str__(self):
        return self.serial_number


##################################################################################################


class SerialNumber(models.Model):
    class Meta:
        unique_together = (('serial_number', 'workorder_id'),)
    serial_number = models.CharField(max_length=255, primary_key=True)
    workorder_id = models.ForeignKey('WorkOrder', on_delete=models.SET_NULL, null=True, db_column='workorder_id')
    model_id = models.ForeignKey('MaterialMaster', on_delete=models.SET_NULL, null=True, db_column='model_id')
    station_id = models.ForeignKey('line.Station', on_delete=models.SET_NULL, null=True, db_column='station_id')
    rework = models.IntegerField(null=True)
    rework_id = models.CharField(max_length=100)
    generated_date = models.DateTimeField(null=True)
    assy_date = models.DateTimeField(null=True)
    complete_date = models.DateTimeField(null=True)
    pack_date = models.DateTimeField(null=True)
    ship_date = models.DateTimeField(null=True)
    failed = models.IntegerField(default=0)
    sn_status_category = models.ForeignKey('SN_Status_Category', on_delete=models.SET_NULL, null=True, db_column='sn_status_category')
    updater = models.CharField(max_length=255,null=True)
    update_date = models.DateTimeField(null=True)

    COMPLETED_TYPE = (
        (0, 'NOT COMPLETED'),
        (1, 'COMPLETED'),
    )
    completed = models.IntegerField(
        choices=COMPLETED_TYPE,
        help_text='completed',
        default=0
    )

    SHIPPED_TYPE = (
        (0, 'NOT SHIPPED'),
        (1, 'SHIPPED'),
    )
    shipped = models.IntegerField(
        choices=SHIPPED_TYPE,
        help_text='shipped',
        default=0
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.serial_number

    """
    @params
        self
        _keypart {
            PartNo : part no
            PartSN : keypart_sn
        } 

    """

    def check_swappable(self, _keypart):

        alt_string = ""
        response = False

        wo_detail_ref = WorkOrderDetail.objects.filter(workorder_id=self.workorder_id)

        if wo_detail_ref:

            for entry in wo_detail_ref:

                if str(entry.model_id) == str(_keypart['PartNo']):
                    alt_string = entry.alternative_item_group

                    break
        else:
            response = False

        serialnumbers = SerialNumber.objects.filter(workorder_id=self.workorder_id)

        if alt_string:
            for sn in serialnumbers:
                keyparts = sn.get_keyparts()
                for keypart_ref in keyparts:

                    if keypart_ref.alt_group == alt_string and str(_keypart['PartNo']) == keypart_ref.model_id and keypart_ref.cserialnumber == "":
                        _keypart_ref = KeyPart.objects.filter(serialnumber=self, cserialnumber="",alt_group=alt_string)

                        if _keypart_ref:
                            _keypart_ref = _keypart_ref.first()
                            response = (keypart_ref, _keypart_ref)

        return response

    """
    @params
        self
        _keypart {
            part : materialmaster_ref
            sn : keypart_sn
        } 

    """

    def swap_keyparts(self, _keypart):

        response = False

        request = self.check_swappable(_keypart)

        if request:
            keypart_ref, _keypart_ref = request

            try:

                temp = keypart_ref.serialnumber
                keypart_ref.sn = _keypart_ref.serialnumber
                _keypart_ref.serialnumber = temp

                keypart_ref.save()
                _keypart_ref.save()
                response = True
                return response
            except:
                return response

        return response

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        # return reverse('manufacturing:home')
        return reverse('manufacturing:serialnumber_detail', args=[str(self.pk)])

    def get_stations(self):
        print("how")
        Route = apps.get_model('line', 'Route')

        route_ref = Route.objects.filter(prod_version=self.workorder_id.production_version)

        if route_ref:
            route_ref = route_ref.first()

            return route_ref.get_stations()
        else:
            return None

    def get_keyparts(self):
        return KeyPart.objects.filter(serialnumber=self)

    def get_all_unfinished_keyparts(self):

        return KeyPart.objects.filter(serialnumber=self, cserialnumber="")

    def get_filtered_keyparts(self, station_id):

        keyparts = self.get_keyparts()
        keypart_list = []

        Station = apps.get_model("line", "Station")
        station_ref = None
        rules = None
        no_rules = False

        try:
            station_ref = Station.objects.get(pk=station_id)
        except:
            return []

        if station_ref:
            rules = station_ref.get_rules()

        if not rules:
            no_rules = True
            Route = apps.get_model("line", "Route")

            route_ref = Route.objects.filter(prod_version=self.workorder_id.production_version)

            if route_ref:
                route_ref = route_ref.first()
                stations = route_ref.get_stations()

                for station_item in stations:
                    temp_rules_set = station_item.get_rules()
                    for temp_rule in temp_rules_set:
                        if temp_rule not in rules:
                            rules += temp_rule
        # staton w/ no rules
        if no_rules:
            if keyparts:
                for kp in keyparts:
                    wo_detail_ref = WorkOrderDetail.objects.filter(workorder_id=self.workorder_id, model_id=kp.model_id)
                    if wo_detail_ref and wo_detail_ref.first().keypart_group not in rules:
                        keypart_list.append(kp)
            else:
                pass
        else:
            # station with rules
            if keyparts:
                for kp in keyparts:
                    wo_detail_ref = WorkOrderDetail.objects.filter(workorder_id=self.workorder_id,model_id=kp.model_id)
                    
                    if wo_detail_ref and wo_detail_ref.first().keypart_group in rules:
                        keypart_list.append(kp)
            else:
                pass

        print(keypart_list)
        return keypart_list

    # will run into problems if stations are used in multiple stations
    def get_unfinished_keyparts(self, station_id):

        keyparts = KeyPart.objects.filter(serialnumber=self,cserialnumber="")
        keypart_list = []

        Station = apps.get_model("line", "Station")
        station_ref = None
        rules = None
        no_rules = False

        
        try:
            station_ref = Station.objects.get(pk=station_id)
        except:
            return []

        if station_ref:

            
            rules = station_ref.get_rules()

        if not rules:
            no_rules = True
            Route = apps.get_model("line", "Route")

            route_ref = Route.objects.filter(prod_version=self.workorder_id.production_version)

            if route_ref:
                route_ref = route_ref.first()
                stations = route_ref.get_stations()

                for station_item in stations:
                    temp_rules_set = station_item.get_rules()
                    for temp_rule in temp_rules_set:
                        if temp_rule not in rules:
                            rules += temp_rule
        # station w/ no rules
        if no_rules:
            if keyparts:
                for kp in keyparts:
                    wo_detail_ref = WorkOrderDetail.objects.filter(workorder_id=self.workorder_id,model_id=kp.model_id)
                    if wo_detail_ref and wo_detail_ref.first().keypart_group not in rules:
                        keypart_list.append(kp)
            else:
                pass
        else:
            # station with rules
            
            if keyparts:
                for kp in keyparts:
                    wo_detail_ref = WorkOrderDetail.objects.filter(workorder_id=self.workorder_id,model_id=kp.model_id)


                    if wo_detail_ref and wo_detail_ref.first().keypart_group in rules:
                        keypart_list.append(kp)
            else:
                pass

        return keypart_list


class SN_Status_Category(models.Model):
    status_id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    seq_no = models.CharField(max_length=255)
    updater = models.CharField(max_length=255)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class KeyPart(models.Model):
    # id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    # part = models.CharField(max_length=255)
    # sn = models.ForeignKey('SerialNumber', on_delete=models.CASCADE, null=True)
    # serial_number = models.CharField(max_length=40, blank=True)
    # creator = models.CharField('Creator', max_length=20)
    # create_date = models.DateTimeField('Create Date', auto_now=True, blank = True)
    # updater = models.CharField('Updater', max_length=20, null = True)
    # update_date = models.DateTimeField('Update Date', null = True, blank = True)
    # alt_group = models.CharField('Alt Groups', max_length=255, blank=True, null=True)
    # scanned_station = models.CharField(max_length=255, null=True,default=None)

    row_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    model_id = models.CharField(max_length=255)
    serialnumber = models.ForeignKey('SerialNumber', on_delete=models.CASCADE, null=True)
    cserialnumber = models.CharField(max_length=80, blank=True)
    creator = models.CharField('Creator', max_length=20)
    create_date = models.DateTimeField('Create Date', auto_now=True, blank=True)
    updater = models.CharField('Updater', max_length=20, null=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)
    alt_group = models.CharField('Alt Groups', max_length=255, blank=True, null=True)
    scanned_station = models.CharField(max_length=255, null=True,default=None)


    
    def __str__(self):
        """String for representing the Model object."""
        return "Parent SN: {} Material Master: {} SerialNumber: {}".format(str(self.serialnumber),str(self.model_id),self.cserialnumber)


    # def get_absolute_url(self):
    #     """Returns the url to access a detail record for this book."""
    #     return reverse('manufacturing:workorder-sn', args=[str(self.id)])


##################################################################################################


class WorkOrder(models.Model):
    workorder_id = models.CharField(max_length=25, primary_key=True)
    workorder_type = models.CharField(max_length=50)
    status_id = models.ForeignKey('WoStatusCategory', db_column='status_id', on_delete=models.CASCADE, null=False)   
    skuno = models.ForeignKey('MaterialMaster', db_column='skuno', on_delete=models.CASCADE, null=False)
    production_version = models.ForeignKey('line.Prod_Version', db_column='production_version', on_delete=models.SET_NULL, null=True)
    model_desc = models.CharField('Model Description', max_length=100)
    line_name = models.CharField('Line Name', max_length=100, null=True)
    sap_release_date = models.DateTimeField(null=False)
    schedule_date = models.DateTimeField(null=False)
    plant_code = models.CharField('Plant Code', max_length=100)
    labor_time = models.CharField('Labor time', max_length=100, null=True)
    route_id = models.IntegerField(blank=True, null=True)
    target_qty = models.IntegerField('Target QTY', default=0)
    finished_qty = models.IntegerField('Finished QTY', default=0)
    pick_status = models.CharField(max_length=1, default='n')
    hold_flag = models.CharField('Hold Flag', max_length=100)
    mc_code = models.CharField('MC Code', max_length=100)    
    pack_count = models.IntegerField(default=1)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.pk

    def get_serial_numbers(self):
        serial_numbers = SerialNumber.objects.filter(workorder_id=self)

        return serial_numbers

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        # return reverse('manufacturing:home')
        return reverse('workordermanager-wo-detail', args=[str(self.pk)])

    def generate_serial_number(self, mask, quantity, user):
        error_level = 0
        counter = self.finished_qty

        response = True

        while counter < quantity:

            serial_number = ''
            serial_number, pattern = mask.generate_sn()

            print(serial_number)

            materials = apps.get_model('manufacturing', 'MaterialMaster')

            model_ref = materials.objects.filter(pk=self.skuno)


            if model_ref and serial_number != '':
                model_ref = model_ref.first()

                Route = apps.get_model('line', 'Route')

                route_ref = Route.objects.filter(prod_version_id=self.production_version)

                if route_ref.first() and route_ref.first().first_station:
                    station = route_ref.first().first_station

                    serial_number_instance = SerialNumber(serial_number=serial_number,
                                                    workorder_id=self,
                                                    model_id=model_ref,
                                                    station_id=station,
                                                    generated_date=make_aware(datetime.now()),
                                                    sn_status_category=None,
                                                    updater=str(user),
                                                    update_date=make_aware(datetime.now())
                                                    )
                    
                    

                    keyparts = None
                    


                    if serial_number_instance:
                        serial_number_instance.save()
                        _temp_sn = serial_number_instance.serial_number
                        _status = "Generated"

                        change_status({"serial_number":_temp_sn,"status_name":_status})



                        keyparts = self.create_keyparts(serial_number_instance,user)
                        
                        log = SerialNumberLog(
                                            serial_number=serial_number_instance.serial_number,
                                            workorder = self.workorder_id,
                                            model=serial_number_instance.model_id,
                                            station="No Station",
                                            user=user,
                                            event="SerialNumber: {} assigned to Workorder: {}".format(serial_number_instance.serial_number, self.workorder_id),
                                            log_type=0
                                            

                        )
                        log.save()

                        '''
                        serial_number = models.CharField(max_length=50)
                        workorder = models.CharField(max_length=50)
                        model = models.CharField(max_length=50)
                        station = models.CharField(max_length=100)
                        in_station_time = models.DateTimeField(auto_now=True)
                        user = models.CharField(max_length=50)
                        event = models.TextField()
                        '''
                        
                    
                    if keyparts:
                        
                        self.finished_qty = self.finished_qty + 1
                        
                        self.save()
                    else:
                        serial_number_instance.delete()

                        response = False

                        # self.generate_key_parts(serial_number_instance,part_list)






                else:
                    response = False
                    error_level += 1
            else:
                response = False
                error_level =  (self.target_qty - self.finished_qty)
                return response,error_level
            counter += 1

        return response, error_level

    def create_keyparts(self, serialnumber, user):

        parts = self.get_parts()
        keyparts = []

        if parts:
            response = True
            
            for part in parts:

                try:
                    keypart_instance = apps.get_model('manufacturing', 'Keypart')
                    
                    keypart_instance = keypart_instance(
                                                        model_id=part['part'],
                                                        serialnumber=serialnumber,
                                                        cserialnumber='',
                                                        creator=user,
                                                        create_date=make_aware(datetime.now()),
                                                        updater=user,
                                                        update_date=make_aware(datetime.now()),
                    )
                    keyparts.append(keypart_instance)
                except IntegrityError as e:
                    print(e)
                    response = False

            if response:
                for keypart in keyparts:
                    keypart.clean()
                    keypart.save()

            return response

    def generate_serial_numbers(self, user):

        wo_detail = apps.get_model('manufacturing', 'WorkOrderDetail')

        part_list = wo_detail.objects.filter(workorder_id=self)

        if part_list:
            mask_model = apps.get_model('maskconfig', 'Mask')

            count = self.target_qty

            # get mask ref
            mask = mask_model.objects.filter(model=self.skuno)

            if mask:
                mask = mask.first()

                # check if serial numbers were all generated error level TODO later
                generated = None
                try:

                    generated,errorlevel = self.generate_serial_number(mask, count, user)
                except Exception as e:
                    print("error: ",e)
                
                if generated:

                    status_ref = WoStatusCategory.objects.filter(name="Generated SN")
                    if status_ref:
                        self.status_id = status_ref.first()
                    
                    self.clean()
                    self.save()

            else:
                return False, (self.target_qty - self.finished_qty)     

    def get_parts(self):

        # get model references
        wo_detail = apps.get_model('manufacturing', 'WorkOrderDetail')
        part_list = wo_detail.objects.filter(workorder_id=self)

        error = False
        parts = []
        
        if part_list:
            for part in part_list:
                try:
                    _bom_usage = int(float(part.bom_usage))
                    print(_bom_usage)
                    print(part.required_qty != None and part.required_qty > 0 and part.keypart_group!="")
                    if part.required_qty != None and part.required_qty > 0 and part.keypart_group != "" :

                        temp = {
                                    'part' : part.model_id, 
                                    'keypart_group' : part.keypart_group,
                                    'usage' :  part.usage_probability_alt_item,
                                    'qty' : _bom_usage
                                    } 
                                    
                        parts.append(temp)
                except Exception as e:
                    print("error: ",e)
                    pass

        
        full_part_list = []

        for part in parts:
            if 'qty' in part and int(part['qty'] or 0) > 0:
                for i in range(part['qty']):
                    full_part_list.append(
                        {
                            'part': part['part'],
                            'keypart_group': part['keypart_group']
                        }
                    )

        # verified_part_list = self.verify_parts(full_part_list)

        # verified_part_list = self.filter_parts(verified_part_list)

        return full_part_list

    # verify that parts are in material master
    # def verify_parts(self,part_list):
    #     response = True

    #     materials = apps.get_model('manufacturing', 'MaterialMaster')
    #     materials = materials.objects.all()

    #     material_names = []

    #     for material in materials:
    #         material_names.append(material.model)

    #     for part in part_list:
    #         if part['part'] not in material_names:
    #             response = False
    #             return response

    #     if part_list:
    #         response = part_list
    #     else:
    #         response = False
    #     return response

    # return filtered keyparts based on mg's
    # def filter_parts(self, part_list):

    #     Route = apps.get_model('line', 'Route')
    #     Rule = apps.get_model('rules', 'Rule')
    #     filtered_parts = []

    #     material_instance = MaterialMaster.objects.filter(model=self.model)

    #     if material_instance and part_list:
    #         material_instance = material_instance.first()

    #         # collect rules
    #         Route = Route.objects.filter(model=material_instance)

    #         if Route:
    #             Route = Route.first()

    #             rules = Rule.objects.filter(route=Route)

    #             keypart_groups = []
    #             if rules:
    #                 for rule_item in rules:
    #                     if rule_item.material_group not in keypart_groups:
    #                         keypart_groups.append(rule_item.material_group)

    #             for part in part_list:

    #                 if part['keypart_group'] in keypart_groups:
    #                     filtered_parts.append(part)

    #     return filtered_parts

class WoStatusCategory(models.Model):
    status_id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    seq_no = models.IntegerField()
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)


    def __str__(self):
        return self.name

class MaterialMaster(models.Model):
    
    model_id = models.CharField(max_length=255, primary_key=True)
    plant_code = models.CharField(max_length=255)
    material_group = models.CharField(max_length=255)
    material_type = models.CharField(max_length=255)
    model_desc = models.CharField(max_length=255)
    unit_of_measure = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    gross_weight = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    net_weight = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    length = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    width = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    height = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    unit_of_dimension = models.CharField(max_length=255)
    package_limit = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True)
    temperature = models.CharField(max_length=255)
    stock_type = models.CharField(max_length=255)
    storage_bin = models.CharField(max_length=255)
    keypart_group = models.CharField(max_length=255, blank=True)
    pallet_limit = models.IntegerField(null=True, default=None)
    alternative_pn = models.CharField(max_length=255, null=True, default=None)
    sap_create_date = models.DateTimeField(null=True, default=None)
    sap_change_date = models.DateTimeField(null=True, default=None)
    sap_change_time = models.TimeField(null=True, default=None)
    model_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.model_id)


class Bom(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    model_id = models.CharField(max_length=1008)  # MATNR
    model_desc = models.CharField(max_length=1000)  # MAKTX
    plant_code = models.CharField(max_length=100)  # WERKS
    alternative_bom = models.CharField(max_length=100)  # STLAL
    bom_usage = models.CharField(max_length=100)  # STLAN
    bill_of_material = models.CharField(max_length=100)  # STLNR
    created_on = models.DateTimeField()  # ANDAT
    base_quantity = models.IntegerField()  # BMENG
    bom_item_node_number = models.CharField(max_length=100)  # STLKN
    internal_counter = models.CharField(max_length=100)  # STPOZ
    bom_component = models.CharField(max_length=1008)  # IDNRK
    component_material_description = models.CharField(max_length=1000)  # IDNRK_NM
    bom_item_number = models.CharField(max_length=100)  # POSTP
    item_category = models.CharField(max_length=100)  # MENGE
    component_quantity = models.IntegerField()  # MENGE
    component_unit_of_measure = models.CharField(max_length=100)  # MEINS
    bom_item_text_1 = models.CharField(max_length=1000)  # POTX1
    bom_item_text_2 = models.CharField(max_length=1000)  # POTX2
    language = models.CharField(max_length=100)  # LTXSP
    long_text = models.CharField(max_length=200)  # POTX
    main_material_code = models.CharField(max_length=100)  # MAIN
    is_main_material = models.CharField(max_length=100)  # IF_MAIN
    alternative_item_group = models.CharField(max_length=100)  # ALPGR
    alternative_item_ranking_order = models.CharField(max_length=100)  # ALPRF
    installation_point = models.CharField(max_length=2000)  # EBORT
    creator = models.CharField('Creator', max_length=20)
    create_date = models.DateTimeField('Create Date', auto_now=True, blank=True)
    updater = models.CharField('Updater', max_length=20, null=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.model_id


# Added By JMACIEL - Repair Process 06112020, Begin


class FailureCategory(models.Model):
    category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    creator = models.CharField(
        'Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField(
        'Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        return self.name


class FailureGroup(models.Model):
    group_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    category_id = models.ForeignKey(
        'FailureCategory', db_column='category_id', on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    creator = models.CharField(
        'Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField(
        'Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        return self.name


class FailureCode(models.Model):
    failure_code = models.CharField(primary_key=True, max_length=10)
    group_id = models.ForeignKey(
        'FailureGroup', db_column='group_id', on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=255)
    creator = models.CharField(
        'Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField(
        'Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.failure_code


class TestingResult(models.Model):
    serial_number = models.ForeignKey('SerialNumber', db_column='serial_number', on_delete=models.CASCADE)
    station = models.CharField(max_length=50)
    testing_date = models.DateTimeField('Testing Date')
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)

    RESULT_TYPE = (
        (0, 'FAIL'),
        (1, 'PASS'),
    )
    result = models.IntegerField(choices=RESULT_TYPE, help_text='result')
    rowid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    # def __str__(self):
    #     return self.serial_number


class RepairMain(models.Model):
    failure_sequence = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    serial_number = models.ForeignKey('SerialNumber', db_column='serial_number', on_delete=models.CASCADE)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    station = models.CharField(max_length=50)
    failure_code = models.ForeignKey(
        'FailureCode', db_column='failure_code', on_delete=models.CASCADE)
    failure_description = models.CharField(max_length=100)
    creator = models.CharField(
        'Creator', max_length=100, null=True, blank=True)

    REPAIR_TYPE = (
        (0, 'NOT REPAIRED'),
        (1, 'REPAIRED'),
    )

    result = models.IntegerField(
        choices=REPAIR_TYPE,
        help_text='repaired',
    )
    repaired_date = models.DateTimeField('Repaired Date', null=True, blank=True)


class RepairDetail(models.Model):
    failure_sequence = models.ForeignKey(
        'RepairMain', db_column='failure_sequence', on_delete=models.CASCADE)
    repaired_code = models.ForeignKey(
        'RepairCode', db_column='repair_code', on_delete=models.CASCADE)
    repaired_description = models.CharField(max_length=100)

    REPLACEMENT_TYPE = (
        (0, 'NOT REPLACED'),
        (1, 'REPLACED'),
    )

    replacement = models.IntegerField(
        choices=REPLACEMENT_TYPE, help_text='replaced')

    in_part_no = models.CharField(max_length=30, null=True, blank=True)
    out_part_no = models.CharField(max_length=30, null=True, blank=True)
    in_cserialno = models.CharField(max_length=100, null=True, blank=True)
    out_cserialno = models.CharField(max_length=100, null=True, blank=True)

    creator = models.CharField(
        'Creator', max_length=100, null=True, blank=True)
    repaired_date = models.DateTimeField('Repaired Date')

    def __int__(self):
        return self.failure_sequence.serial_number


class RepairGroup(models.Model):
    group_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    IS_REPLACEMENT_TYPE = (
        (0, 'NOT A REPLACEMENT'),
        (1, 'REPLACEMENT'),
    )

    replacement = models.IntegerField(choices=IS_REPLACEMENT_TYPE, default=0, help_text='Is replacement')

    creator = models.CharField(
        'Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField(
        'Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        return self.name


class RepairCode(models.Model):
    repair_code = models.CharField(primary_key=True, max_length=10)
    group_id = models.ForeignKey(
        'RepairGroup', db_column='group_id', on_delete=models.CASCADE, null=False)
    description = models.CharField(max_length=255)
    creator = models.CharField(
        'Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField(
        'Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.repair_code


class Label(models.Model):
    name = models.CharField(max_length=100)
    zpl = models.TextField()


# Added By JMACIEL - Hold Station Model, Begin


class HoldTypes(models.Model):
    type_id = models.CharField(primary_key=True, max_length=50, db_index=True)
    name = models.CharField('Type Name', max_length=50, null=False)
    updater = models.CharField(
        'Updater', max_length=100, null=False, blank=True)
    update_date = models.DateTimeField('Update Date', null=False, blank=True)

    def __str__(self):
        return self.name


class Hold(models.Model):
    hold_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    hold_value = models.CharField(max_length=100, null=False)
    type_id = models.ForeignKey('HoldTypes', db_column='type_id',
                                on_delete=models.CASCADE, null=False)
    hold_by = models.CharField(max_length=100, null=False)
    hold_date = models.DateTimeField('Hold Date', null=False, blank=True)
    hold_reason = models.CharField(max_length=255, null=False)
    HOLD_STATUS = (
        (0, 'Hold'),
        (1, 'UnHold'),
    )
    hold_status = models.IntegerField(
        choices=HOLD_STATUS, help_text='Hold Status', null=False)
    station = models.CharField(max_length=100, null=False)
    unhold_by = models.CharField(max_length=100, null=True, blank=True)
    unhold_date = models.DateTimeField('Hold Date', null=True, blank=True)
    unhold_reason = models.CharField(max_length=255, null=True, blank=True)
    updater = models.CharField(
        'Updater', max_length=100, null=False)
    update_date = models.DateTimeField('Update Date', null=False)

    def __str__(self):
        return self.hold_value
# Added By JMACIEL - Hold Station Model, End

# class ScanType(models.Model):

#     rowid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     material_group = models.CharField('Material Group', max_length=30, null=False, blank=False)

#     TYPE_CHOICES = (
#         ('CSERIALNO','CSERIALNO'),
#         ('CUSTPARTNO','CUSTPARTNO'),
#         ('HHPNCSERIALNO','HHPNCSERIALNO'),
#         ('FAKECSERIALNO','FAKECSERIALNO'))
#     scan_type = models.CharField(max_length=30, null=False, blank=False)
#     description = models.CharField(max_length=30, null=False, blank=False)
#     created_by = models.CharField('Creator', max_length=30, null=False)
#     create_date = models.DateTimeField('Create Date', auto_now=True)
#     updater = models.CharField('Updater', max_length=30, null = True, blank=True)
#     update_date = models.DateTimeField('Update Date', null = True, blank = True)
class SerializationRule(models.Model):
    rule_id = models.AutoField(auto_created=True, primary_key=True)
    rule_type = models.CharField('Rule Type', max_length=20, null=True, blank=True)
    rule_length = models.IntegerField()
    start_sequence = models.IntegerField()
    current_sequence = models.IntegerField()
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

class SerializationRuleValues(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    rule_id = models.ForeignKey('SerializationRule', db_column='rule_id', on_delete=models.CASCADE, null=False)
    sequence = models.IntegerField()
    value_name = models.CharField('Value Name', max_length=30, null=True, blank=True)
    value = models.CharField('Value', max_length=50, null=True, blank=True)
    rule_length = models.IntegerField()
    start_sequence = models.IntegerField()
    current_sequence = models.IntegerField()
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

class ControlApp(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    control_name = models.CharField('Value Name', max_length=30, null=True, blank=True)
    control_description = models.CharField('Control Description', max_length=50, null=True, blank=True)
    control_value = models.CharField('Control Value', max_length=255, null=True, blank=True)
    creator = models.CharField('Creator', max_length=100, null=True, blank=True)
    create_date = models.DateTimeField('Create Date', null=True, blank=True)
    updater = models.CharField('Updater', max_length=100, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)