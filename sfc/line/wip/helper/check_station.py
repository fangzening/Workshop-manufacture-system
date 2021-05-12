from django.apps import apps
from .serialnumber_scan import serialnumber_scan


def check_station(request):
    data = request.POST

    response = False
    station = data.get('station')

    serial_number_ref = serialnumber_scan(request)

    if serial_number_ref and station:
        
        if serial_number_ref.station_id.pk == station:
            response = True

    return response