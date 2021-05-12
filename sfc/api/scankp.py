from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .wip_util.serialnumber_scan import serialnumber_scan
from .wip_util.check_station import check_station
from .wip_util.change_station import change_station
from .keypart.create_keypart import create_keypart
from .keypart.check_keypart import check_keypart
from django.http import HttpResponse
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpRequest
import requests
from django.http import HttpRequest, QueryDict, HttpResponse, Http404
import base64
from datetime import datetime
from django.http import QueryDict
from django.utils.timezone import make_aware

# model imports
SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
TestingResult = apps.get_model('manufacturing', 'TestingResult')
FailureCode = apps.get_model('manufacturing', 'FailureCode')
RepairMain = apps.get_model('manufacturing', 'RepairMain')

Station = apps.get_model('line', 'Station')
Route = apps.get_model('line', 'Route')
KeyPart = apps.get_model('manufacturing', 'KeyPart')
MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')
Rule = apps.get_model('rules', 'Rule')
Bom = apps.get_model('manufacturing', 'Bom')
Stationroutes = apps.get_model('line', 'Stationroutes')


def scankeypart_function(request):
    serial_number = None
    station_id = None

    checkkeypart_payload = None

    parts = []
    post_data = None
    json_data = None
    message = "Success"
    status = 200

    def json_config():
        data = {"status": status, "message": message}
        return JsonResponse(data)

    def data_integrity_check():
        nonlocal
        json_data, status, message, post_data
        if request.method == 'POST':

            if isinstance(request.body, str):

                try:
                    json_data = json.loads(request.body)
                except:

                    status = 505
                    message = "Error loading JSON"
                    return json_config()

            else:

                try:
                    post_data = request.body.decode('utf-8')
                    json_data = json.loads(post_data)
                except:
                    status = 505
                    message = "Error loading JSON"
                    return json_config()
        else:

            message = "Only Post Requests Allowed"
            status = 509

            return json_config()

    def call_checkkeypart():
        nonlocal
        message, status, checkkeypart_payload

        if json_data:

            # get parts from other endpoint
            try:

                checkkeypart_payload = checkkeypart_function(POST_request_parser(request))
                checkkeypart_payload = checkkeypart_payload.content
                checkkeypart_payload = json.loads(checkkeypart_payload)
            except:
                status = 505
                message = "Error loading JSON"
                return json_config()
        else:
            status = 506
            message = "No JSON was received"
            return json_config()

        if 'message' in checkkeypart_payload and 'status' in checkkeypart_payload:
            if payload['status'] != 200:
                message = payload['message']
                status = payload['status']
                return json_config()

    # format parts for kp insertion
    def format_parts():
        nonlocal
        serial_number, station_id, parts

        serial_number = json_data['serial_number']
        station_id = json_data['station_id']
        parts = json_data['partsn']

        json_data['user'] = str(request.user)
        if parts and 'PartSN' not in parts[0]:
            # implement later
            status = 511
            message = "CustPartNo Not implemented yet"
            return json_config()

    # iterate through parts and try to create
    def create_keyparts():
        nonlocal
        status, message
        response = "success"
        counter = 0

        while counter < len(parts):
            response = create_keypart(json_data, parts[counter])

            counter += 1
            if response != "Success":
                status, message = response

                break
        return json_config()

    data_integrity_check()
    call_checkkeypart()
    format_parts()
    create_keyparts()

    return json_config()


'''

##########################
check if all data is there
check sn
check route
check station
##########################

'''


# done
def checkkeypart_function(request):
    serial_number = None
    station_id = None
    parts = None
    part_list = None
    partsn_list = None
    parts = []
    post_data = None
    message = "Success"
    status = 200

    def json_config():
        data = {"status": status, "message": message}
        resp = JsonResponse(data)

        return resp

    if request.method == 'GET':
        post_data = request.GET


    else:
        message = "Only GET Requests Allowed"
        status = 509

    def data_integrity_check():

        if post_data:

            serial_number = None
            station_id = None
            parts = None
            if 'serial_number' in post_data and 'stationid' in post_data and 'partsn' in post_data or 'partno' in post_data:

                serial_number = post_data['serial_number']
                station_id = post_data['stationid']

                part_list = post_data.getlist('partno')
                partsn_list = post_data.getlist('partsn')
                parts = []

            else:
                status = 503
                message = "Missing Data"
                return json_config()

        else:
            status = 506
            message = "No JSON was received"
            return json_config()

    def check_sn():
        serialnumber_ref = None
        if serial_number:
            serialnumber_ref = serialnumber_scan(post_data)

            if not serialnumber_ref:
                status = 505
                message = "No Serial Number Found"
                json_config()

        else:
            message = "No Serial Number in Request"
            status = 504
            json_config()
        return serialnumber_ref

    def check_station():
        station_check = check_station(post_data)

        if station_check[1] != 200:
            message = station_check[0]
            status = station_check[1]
            return json_config()

        return station_check

    def format_parts():

        if len(part_list) == len(partsn_list):
            for element in range(len(part_list)):
                parts.append({
                    'PartNo': part_list[element],
                    'PartSN': partsn_list[element]
                })
            post_data['user'] = str(request.user)

    elif 'serial_number' in post_data and 'stationid' in post_data and 'partsn' in post_data:
    serial_number = post_data['serial_number']
    station_id = post_data['stationid']
    for element in range(len(partsn_list)):
        parts.append({
            'PartSN': partsn_list[element]
        })

    post_data['user'] = str(request.user)

else:
# implement later
status = 511
message = "CustPartNo Not implemented yet"
return json_config()


# pass

def check_parts():
    response = "success"
    counter = 0

    while counter < len(parts):
        response = check_keypart(post_data, parts[counter])

        counter += 1
        if response != "Success":
            status, message = response
            break


# call all functions
data_integrity_check()
check_sn()
check_station()
format_parts()
check_parts()

return json_config()
