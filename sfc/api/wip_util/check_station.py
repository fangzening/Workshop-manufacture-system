from django.apps import apps
from .serialnumber_scan import serialnumber_scan

def check_station(data):
        
    
    response = False
    status = 200

    station = data['stationid']

    
    serial_number_ref = serialnumber_scan(data)

   

    if serial_number_ref and station:

        if serial_number_ref.station_id.pk == station:
            response = True
        else:
            response = "Serial Number Not At Station"
            status = 501
    else:
        response = "Station doesn't exist"
        status = 502
    return response, status