from django.apps import apps
from django.shortcuts import render, redirect 
from ..helper.serialnumber_scan import serialnumber_scan
from ..helper.check_station import check_station
from ..helper.change_station import change_station
from ..helper.check_route import check_route
from ..helper.create_log import create_log
from .create_keypart import create_keypart
from itertools import chain
from django.http import HttpRequest
import json
from api.views import scankeypart_function


# user feedback
'''
sn not exist
wrong station
keypart isn't apart of the serialnumber
keypart sn doesnt match mask

'''

def assembly(request):

    data = request.POST
    template_name = 'production/key-part.html'
    serialnumber = data.get('serial_number')
    template = data.get('template')
    route_id = data.get('route')
    station_id = data.get('station')
    ver = data.get('ver')
    part_number = data.get('partnum')
    kp_serialnumber = data.get('kp_serialnumber')

    serialnumber_ref = None

    message = None
    result = None

    Label = apps.get_model("manufacturing", "Label")
    labels = Label.objects.all()
    # get station ref
    Station = apps.get_model('line', 'Station')
    station_ref = Station.objects.filter(pk=station_id)
    if station_ref:
        station_ref = station_ref.first()
    
    # get route ref
    Route = apps.get_model('line', 'Route')
    route_ref = Route.objects.filter(pk=route_id)
    if route_ref:
        route_ref = route_ref.first()
    if serialnumber:
        serialnumber_ref = serialnumber_scan(request)
    else:
        message = "Please Enter A Serial Number"

    if serialnumber_ref:
        # if kp_serialnumber and part_number:
        # format request for scankeypart api
        req = HttpRequest()
        req.META['REQUEST_METHOD'] = "POST"
        req.user = request.user

        payload = None
    
        req.method = "POST"

        if (part_number == "" or part_number == " " or part_number == None) and kp_serialnumber and len(kp_serialnumber) > 0:
            
            payload = {
                "serial_number" : data.get('serial_number'),
                "stationid" : data.get('station'),
                "partsn" : [
                    {
                        "PartSN" : data.get('kp_serialnumber')
                    }
                ]
            }
        elif kp_serialnumber and part_number:
            payload = {
                "serial_number" : data.get('serial_number'),
                "stationid" : data.get('station'),
                "partsn" : [
                    {
                        "PartNo" : data.get('partnum'),
                        "PartSN" : data.get('kp_serialnumber')
                    }
                ]
            }
        elif part_number:
            payload = {
                "serial_number" : data.get('serial_number'),
                "stationid" : data.get('station'),
                "partsn" : [
                    {
                        "PartNo" : data.get('partnum'),
                        "PartSN" : data.get('partnum')
                    }
                ]
            }

        if payload:
            payload = json.dumps(payload)
            req._body = payload

        response = None
        if payload:
            response = scankeypart_function(req)
            
        json_resp = None
        
        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                result='Failed'
                message='Unknown error occured'
       
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            result = 'success' if json_resp['status'] == '200' else 'Failed'
            message = json_resp['message']

        unfinished = serialnumber_ref.get_unfinished_keyparts(station_id)

        filtered_parts = serialnumber_ref.get_filtered_keyparts(station_id)
        
        keyparts = []

        WorkOrderDetail = apps.get_model("manufacturing", "WorkOrderDetail")

        for kp in filtered_parts:
            desc = WorkOrderDetail.objects.filter(model_id=kp.model_id)
            if desc:
                desc = desc.first().model_desc
            else:
                desc = "No Description"
            temp = {
                "part" : kp.model_id,
                "desc" : desc,
                "serial_number" : kp.cserialnumber 
            }
            alt_group = ""
            if kp.alt_group:
                
                for _kp in master_parts:
                    alt_group = alt_group + ", " + _kp.model_id
            temp['alt'] = alt_group
               
            keyparts.append(temp)

        

        finished = False

        if not unfinished and len(unfinished) == 0:
            
            finished = True

        elif finished:
            # reset values to keep scanning in station
            keypart_list = []
            serialnumber = ''
            
            message = 'Move to Next Station!'
            result = 'success'
            
        elif kp_serialnumber == '' and part_number != '':
            message = 'Please Enter In A Key Part Serial Number'
        elif keyparts and kp_serialnumber == '' and part_number == '' :
            result = None
            message = None        
        
        scan_types = []
        if station_ref:
            scan_types = station_ref.get_scantypes()

        context = {
            'keyparts' : keyparts,
            'sn': serialnumber,
            'template': template,
            'route_id': route_id,
            'station_id': station_id,
            'ver': ver,
            'station_name': station_ref,
            'scan_types' : scan_types,
            'message' : message,
            'result' : result,
            'labels': labels,
        }
        
        return render(request, template_name, context)
    else:
        
        message = "Serial Number doesn't exist"
        context = {
            'sn': serialnumber,
            'template': template,
            'route_id': route_id,
            'station_id': station_id,
            'ver': ver,
            'station_name': station_ref,
            'message' : message,
            'result' : result,
            'labels': labels,
        }
        return render(request, template_name, context)
