from django.apps import apps
from django.utils import timezone
from django.db import IntegrityError
from django.shortcuts import render, redirect 
from ..wip_util.serialnumber_scan import serialnumber_scan
from ..wip_util.check_station import check_station
from ..wip_util.change_station import change_station
from ..wip_util.check_route import check_route
from ..wip_util.create_log import create_log
from .check_mask import check_mask

from datetime import datetime
from django.utils.timezone import make_aware

def create_keypart(data,keypart):
        
            
    part_number = None
    kp_serialnumber = None

    # check which data is passed
    if 'PartNo' in keypart and 'PartSN' in keypart:
        part_number = keypart['PartNo']
        kp_serialnumber = keypart['PartSN']
    elif 'PartSN' in keypart:
        kp_serialnumber = keypart['PartSN']
    elif 'PartNo' in keypart:
        part_number = keypart['PartNo']
    else:
        response = 512
        message = "Missing Data"
        return (response,message)
    
    response = 200
    message = "Success"

    serial_number_ref = serialnumber_scan(data)
    MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')
    material_ref = None

    if part_number:
        material_ref = MaterialMaster.objects.filter(pk=part_number)
        if material_ref:
            material_ref = material_ref.first()

    

    # very serial number and parts
        
    # check mask
    Mask = apps.get_model('maskconfig', 'Mask')
    

    if part_number and kp_serialnumber:
        mask_ref = Mask.objects.filter(model=part_number)
        
        if mask_ref:
            mask_ref = mask_ref.first()
            keypart['mask'] = mask_ref
            message = check_mask(keypart)
           
        else:
            
            
            message = None
    elif kp_serialnumber:     

        masks = Mask.objects.all()
        Station = apps.get_model('line', 'Station')
        station_ref = Station.objects.filter(pk=data['stationid'])


        mask_arr = []
        if not station_ref:
            mask_arr = masks
        else:
            station_ref = station_ref.first()
            rule_arr = station_ref.get_rules()
            full_keyparts = serial_number_ref.get_keyparts()
            _model_list = [_kp.model_id for _kp in full_keyparts] 

            for mask in masks:
                if mask.model.keypart_group in rule_arr:
                    if mask.model_id in _model_list:
                        mask_arr.append(mask)

            

        # find mask for keypart sn
        for mask_ref in mask_arr:
            keypart['mask'] = mask_ref
            message = check_mask(keypart)
            
            keypart['PartNo'] = mask_ref.model.model_id
            if message == 'Success':
               
                material_ref = mask_ref.model
                break
    

    if message == 'Success' and material_ref and serial_number_ref:
       
        KeyPart = apps.get_model('manufacturing','KeyPart')

        
        # try to insert keypart into db

        # get scan type
        keypart_group = material_ref.keypart_group
        station_id = data['stationid']

        Station = apps.get_model("line", "Station")
        Rule = apps.get_model("rules", "Rule")

        # get station ref
        station_ref = Station.objects.filter(pk=station_id)
        station_ref = station_ref.first()

        # find rule
        rule_ref = Rule.objects.filter(station=station_ref,material_group=keypart_group)

        scan_type = ""
        if rule_ref:
            rule_ref = rule_ref.first()
            scan_type = rule_ref.scan_type


        if scan_type == "CSERIALNO":
            duplicate = KeyPart.objects.filter(cserialnumber=kp_serialnumber)
            if duplicate:

                message = "There Is A Duplicate Serial Number"
                response = 508

            else:
                
                unfinished_parts = serial_number_ref.get_unfinished_keyparts(data['stationid'])

                unfinished_keyparts = []
                if unfinished_parts:
                    for kp in unfinished_parts:
                        unfinished_keyparts.append(kp.model_id)

                
                if keypart['PartNo'] in unfinished_keyparts:

                    pass

                elif serial_number_ref:
                    resp = serial_number_ref.swap_keyparts(keypart)
                    
                    if not resp:
                        response = 513
                        message = "Part Can Not Be Used In SerialNumber"
                        return (response,message)
                        

                else:
                    response = 513
                    message = "Part Not In SerialNumber"
                    return (response,message)

                try:

                    keypart_ref = KeyPart.objects.filter(
                                                    model_id=material_ref,
                                                    cserialnumber='',
                                                    serialnumber=serial_number_ref
                                                    )

                    if keypart_ref:

                        keypart_ref = keypart_ref.first()

                        keypart_ref.cserialnumber = kp_serialnumber
                        keypart_ref.updater = data['user']
                        keypart_ref.update_date = make_aware(datetime.now())
                        keypart_ref.scanned_station = data['stationid']

                        keypart_ref.clean()
                        keypart_ref.save()
                        response = 200

                        data['log'] = "Assembly SN: {}, Keypart: {} ".format(keypart_ref.cserialnumber,keypart_ref.model_id)
                        create_log(data)

                    else:
                        message = "No Part Available in Serial Number for {}".format(part_number)
                        response = 510
                except IntegrityError:
                    message = "An Unexpected Error Has Occurred"
                    response = 507
        
        elif scan_type == "CUSTPARTNO":
            
            unfinished_parts = serial_number_ref.get_unfinished_keyparts(data['stationid'])

            unfinished_keyparts = []
            if unfinished_parts:
                for kp in unfinished_parts:
                    unfinished_keyparts.append(kp.model_id)

            
            if keypart['PartNo'] in unfinished_keyparts:

                pass

            elif serial_number_ref:
                resp = serial_number_ref.swap_keyparts(keypart)
                
                if not resp:
                    response = 513
                    message = "Part Can Not Be Used In SerialNumber"
                    return (response,message)
                    

            else:
                response = 513
                message = "Part Not In SerialNumber"
                return (response,message)

            try:

                keypart_ref = KeyPart.objects.filter(
                                                model_id=material_ref,
                                                cserialnumber='',
                                                serialnumber=serial_number_ref
                                                )

                if keypart_ref:

                    keypart_ref = keypart_ref.first()

                    keypart_ref.cserialnumber = part_number
                    keypart_ref.updater = data['user']
                    keypart_ref.update_date = make_aware(datetime.now())
                    keypart_ref.scanned_station = data['stationid']

                    keypart_ref.clean()
                    keypart_ref.save()
                    response = 200

                    data['log'] = "Assembly SN: {}, Keypart: {} ".format(keypart_ref.cserialnumber,keypart_ref.model_id)
                    create_log(data)
                else:
                    message = "No Part Available in Serial Number for {}".format(part_number)
                    response = 510
            except IntegrityError:
                message = "An Unexpected Error Has Occurred"
                response = 507
        
        elif scan_type == "OFFLINE":
            duplicate = KeyPart.objects.filter(cserialnumber=kp_serialnumber)
            
            if duplicate:

                message = "There Is A Duplicate Serial Number"
                response = 508

            else:



                htsk_pn = None
                htsk_sn = None

                cpu_pn = None
                cpu_sn = None 
                    
                unfinished_parts = serial_number_ref.get_unfinished_keyparts(data['stationid'])

                unfinished_keyparts = []
                
                if unfinished_parts:
                    for kp in unfinished_parts:
                        unfinished_keyparts.append(kp.model_id)

                
                if keypart['PartNo'] in unfinished_keyparts:
                    pass



                elif serial_number_ref:
                    resp = serial_number_ref.check_swappable(keypart)
                    
                    if not resp:
                        
                        response = 513
                        message = "Part Can Not Be Used In SerialNumber"
                        

                else:
                    response = 513
                    message = "Part Not In SerialNumber"

                phantom = apps.get_model("offline_station","PhantomAssy")
                phantom_ref = phantom.objects.filter(phantom_generated_sn=keypart['PartSN'])
                
                if not phantom_ref:
                    response = 514
                    message = "No Available Part With SerialNumber"
                else:
                    phantom_ref = phantom_ref.first()
                    htsk_pn = phantom_ref.partno
                    htsk_sn = phantom_ref.phantom_generated_sn

                    cpu_pn = phantom_ref.phantom_partno
                    cpu_sn = phantom_ref.phantom_serialnumber

                 
                try:

                    keypart_ref = KeyPart.objects.filter(
                                                    model_id=material_ref,
                                                    cserialnumber='',
                                                    serialnumber=serial_number_ref
                                                    )
                    keypart_cpu_ref = KeyPart(
                                            model_id=MaterialMaster.objects.filter(pk=cpu_pn).first(),
                                            cserialnumber=cpu_sn,
                                            serialnumber=serial_number_ref,
                                            creator = data['user'],
                                            create_date=make_aware(datetime.now()),
                                            updater = data['user'],
                                            update_date =  make_aware(datetime.now()),
                                            scanned_station = data['stationid']
                    )
                    
                    if keypart_ref and keypart_cpu_ref:
                       
                        keypart_ref = keypart_ref.first()

                        keypart_ref.cserialnumber = kp_serialnumber
                        keypart_ref.updater = data['user']
                        keypart_ref.update_date = make_aware(datetime.now())
                        keypart_ref.scanned_station = data['stationid']
                        
                        

                        keypart_ref.clean()
                        keypart_ref.save()
                        keypart_cpu_ref.clean()
                        keypart_cpu_ref.save()
                        response = 200

                        data['log'] = "Assembly SN: {}, Keypart: {}, Keypart: {}  ".format(keypart_ref.cserialnumber,keypart_ref.model_id, keypart_cpu_ref.model_id)
                        create_log(data)
                    else:
                        message = "No Part Available in Serial Number for {}".format(part_number)
                        response = 510
                except IntegrityError:
                    message = "An Unexpected Error Has Occurred"
                    response = 507
        else:
            response = 515
            message = "Part Can Not Be Used In This Station"
    else:
        message = "No Part Available in Serial Number for"
        response = 504

    
    return (response,message)