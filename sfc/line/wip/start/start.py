from django.shortcuts import render, redirect
from django.apps import apps
from ..helper.check_station import check_station
from ..helper.change_station import change_station
from ..helper.check_route import check_route
from ..helper.serialnumber_scan import serialnumber_scan
from ..helper.create_log import create_log
from datetime import datetime


def start(request):
    data = request.POST

    template = data.get('template')
    route_id = data.get('route')
    station_id = data.get('station')
    model = data.get('model')
    result = 'FAIL'
    message = "Unknown error occured"
    

    Station = apps.get_model('line', 'Station')
    station_ref = Station.objects.filter(pk=station_id)
    station_ref = station_ref.first()

    template_name = 'production/start.html'

    serialnumber_ref = serialnumber_scan(request)

    if serialnumber_ref:
        if check_station(request) and check_route(request):
            create_log(request,"{} Has Started Production".format(serialnumber_ref))
            change_station(request,'PASS')
            serialnumber_ref = serialnumber_scan(request)
            serialnumber_ref.status = "In-Progress"
            
            result = "success"
            message = "Go To Next Station"
            serialnumber_ref.save()
        else:
            result = 'FAIL'
            message = 'This Serial Number Is Not At This Station'
    else:
        result = 'FAIL'
        message = 'Serial Number Was Not Found'
        
    context = {
        'template': template,
        'route_id': route_id,
        'station_id': station_id,
        'model': model,
        'station_name': station_ref.pk,
        'result': result,
        "message": message
    }

    return render(request, template_name, context)
