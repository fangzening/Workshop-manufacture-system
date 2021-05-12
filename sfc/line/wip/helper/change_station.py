from django.apps import apps
from .serialnumber_scan import serialnumber_scan
from .create_log import create_log
from datetime import datetime


def change_station(request, state):
    
    data = request.POST

    # state = data.get('state')
    # should be the station id/route id
    station = data.get('station')
    route = data.get('route')
    
    if not state:
        state = 'PASS'

    # response to return false or the sn reference
    response = False
    # get models
    
    station_routes = apps.get_model('line', 'StationRoutes')

    # gets the reference we want from station routes
    

    
    station_ref = station_routes.objects.filter(station=station,route_id=route, state=state)
    
    

    if station_ref:
        station_ref = station_ref.first()
    

    next_station = None
    if station_ref and station_ref.next_station != None:
        next_station = station_ref.next_station
        

    # create scan serialnumber obj

    # Look up if sn exists and returns the serial number reference
    serial_number_ref = serialnumber_scan(request)

    

    if serial_number_ref and next_station:
        old_station = serial_number_ref.station_id
        serial_number_ref.station_id = next_station
        
        
        serial_number_ref.save()

        
        event = "{} moved from {} to {}".format(serial_number_ref,old_station,next_station)
        create_log(request,event)

        response = True
    
    return response