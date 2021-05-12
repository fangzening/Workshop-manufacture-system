from django.shortcuts import render, redirect
from django.apps import apps
from ..helper.check_station import check_station
from ..helper.change_station import change_station
from ..helper.check_route import check_route
from ..helper.serialnumber_scan import serialnumber_scan
from ..helper.create_log import create_log
from django.db import transaction
from datetime import datetime
from django.utils.timezone import make_aware
import json
from django.core import serializers


def repair(request):
    template_name = 'production/repair/repair.html'

    data = request.POST

    submit_type = data.get('submit-type')

    template = data.get('template')
    route_id = data.get('route')
    station_id = data.get('station')
    model = data.get('model')  

    Station = apps.get_model('line', 'Station')
    RepairDetail = apps.get_model('manufacturing', 'RepairDetail')
    RepairMain = apps.get_model('manufacturing', 'RepairMain')    
    RepairCode = apps.get_model('manufacturing', 'RepairCode')

    station_ref = Station.objects.filter(pk=station_id)
    station_ref = station_ref.first()
    serialnumber_ref = serialnumber_scan(request)

    context = {
        'template': template,
        'route_id': route_id,
        'station_id': station_id,
        'model': model,
        'station_name': station_ref.pk
    }

    if serialnumber_ref:
        # serialnumber_ref = serialnumber_ref.first()
        if check_station(request) and check_route(request):          

            SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
            sn = request.POST['serial_number']

            sn_list = SerialNumber.objects.filter(serial_number=sn)
            
            KeyPart = apps.get_model('manufacturing', 'KeyPart')
            key_parts = KeyPart.objects.filter(serialnumber=serialnumber_ref)

            key_parts_list = []

            for part in key_parts:
                key_part = dict()
                key_part['part_no'] = part.model_id
                key_part['serial_number'] = part.cserialnumber
                key_parts_list.append(key_part)

            key_parts_list = json.dumps(key_parts_list)            

            repairmain = RepairMain.objects.order_by('failure_sequence')
            if repairmain:
                repairmain = repairmain.first()

            context.update({
                'serialnumber_list': sn_list,
                'serial_number': serialnumber_ref,
                'repairdetail_list': RepairDetail.objects.order_by('-id'),
                'more_context': RepairDetail.objects.all(),
                'repairmain': repairmain,
                'testingresult': serialnumber_ref.testingresult_set.all(),
                'repaircodeonly_list': RepairCode.objects.order_by('create_date'),
                'repaircode_context': RepairCode.objects.all(),
                'key_parts': key_parts_list,
            })

            if submit_type == 'repair-unit':
                repair_result = "Unit was succesfully repaired and moved to the next station."
                repaired = True
                context['repair_result'] = repair_result
                context['repaired'] = repaired

                failure_sequence = data.get('failure_sequence')
                repaired_code = data.get('repaired_code')
                repaired_description = data.get('repaired_description')
        
                RepairMain = apps.get_model('manufacturing', 'RepairMain')
                repairmain_ref = RepairMain.objects.filter(failure_sequence=failure_sequence)
                if repairmain_ref:
                    
                    try:

                        repairmain_ref = repairmain_ref.first()
                        repairmain_ref.result = 1
                        repairmain_ref.repaired_date = make_aware(datetime.now())
                        repairmain_ref.save()

                    except Exception as e:
                        print(e.message)

                change_station(request, 'PASS')

                return render(request, template_name, context)

                # create_log(request)
            # change_station(request, "PASS")
            # serialnumber_ref.status = "Repaired"
            # serialnumber_ref.end_time = datetime.now().time()
            # result = "success"
            # serialnumber_ref.save()
        else:
            result = 'This Serial Number Is Not At This Station'
            context['result'] = result
    else:
        result = 'Serial Number Was Not Found'
        context['result'] = result

    return render(request, template_name, context)
