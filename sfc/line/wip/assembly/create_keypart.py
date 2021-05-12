from django.apps import apps
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render, redirect 
from ..helper.serialnumber_scan import serialnumber_scan
from ..helper.check_station import check_station
from ..helper.change_station import change_station
from ..helper.check_route import check_route
from .scan_keypart import scan_keypart
from .check_mask import check_mask
from datetime import datetime
from django.utils.timezone import make_aware

def create_keypart(request):
        data = request.POST
        part_number = data.get('part')
        kp_serialnumber = data.get('kp_serialnumber')
        
        response = False
        message = "Success"

        serial_number_ref = serialnumber_scan(request)
        MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')
        
        material_ref = MaterialMaster.objects.filter(pk=part_number)

       

        # very serial number and parts
            
        # check mask
        message = check_mask(request)

        

        if message == 'Success' and material_ref and serial_number_ref:
            material_ref = material_ref.first()
            KeyPart = apps.get_model('manufacturing','KeyPart')
            
            # try to insert keypart into db
            
            duplicate = KeyPart.objects.filter(serial_number=kp_serialnumber)

            if not duplicate:
                try:

                    keypart_ref = KeyPart.objects.filter(
                                                    part=material_ref,
                                                    serial_number='',
                                                    sn=serial_number_ref
                                                    )
                    keypart_ref = keypart_ref.first()
                    keypart_ref.serial_number = kp_serialnumber
                    keypart_ref.updater = str(request.user)
                    keypart_ref.update_date = make_aware(datetime.now())
                    

                    keypart_ref.clean()
                    keypart_ref.save()
                    response = True

                except IntegrityError:
                    message = "An Unexpected Error Has Occurred"
                    response = False

            else:
                message = "There Is A Duplicate Serial Number"
                response = False
                
            
        return (response,message)
