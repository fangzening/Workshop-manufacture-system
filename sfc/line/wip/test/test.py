from django.apps import apps
from django.shortcuts import render, redirect
from ..helper.serialnumber_scan import serialnumber_scan
from ..helper.check_station import check_station
from ..helper.change_station import change_station
from ..helper.check_route import check_route
from ..helper.create_log import create_log
from django.http import HttpRequest
import json
from api.views import testssn_function
import requests

Station = apps.get_model('line', 'Station')


def test(request):
    data = request.POST
    result = None
    message = None

    template = data.get('template')
    route_id = data.get('route')
    station_id = data.get('station')
    model = data.get('model')
    result = data.get('pass-fail')
    symptom = data.get('symptom')
    failure_code = data.get('failure_code')
    serial_number = data.get('serial_number')

    req = HttpRequest()
    req.META['REQUEST_METHOD'] = "POST"
    req.user = request.user

    req.method = "POST"
    payload = {
        "serial_number": serial_number,
        "stationid": station_id,
        "result": result,
        "symptom": symptom,
        "failure_code": failure_code
    }

    print(payload)
    payload = json.dumps(payload)

    req._body = payload

    response = testssn_function(req)
    json_resp = None

    # convert json to dict

    if response:
        try:
            json_resp = json.loads(response.content)
        except:
            result = 'Failed'
            message = 'Unknown error occured'

    # send json to return to page
    print(json_resp)
    if json_resp and 'status' in json_resp and 'message' in json_resp:
        result = 'success' if json_resp['status'] == '200' else 'Failed'
        message = json_resp['message']

    # add station name to page
    station_ref = Station.objects.filter(pk=station_id)
    if station_ref:
        station_ref = station_ref.first()


    
    context = {
        'template': template,
        'route_id': route_id,
        'station_id': station_id,
        'model': model,
        'result': result,
        'message' : message,
        'station_name': station_ref.pk
    }

    template_name = 'production/test.html'

    return render(request, template_name, context)