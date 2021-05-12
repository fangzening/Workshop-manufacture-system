from django.apps import apps
from .serialnumber_scan import serialnumber_scan
from ..helper.check_station import check_station

def create_log(request,event):
    data = request.POST
    response = False
    serial_number_ref = serialnumber_scan(request)

    


    if serial_number_ref:
        SerialNumberLog = apps.get_model('manufacturing', 'SerialNumberLog')
        # log_ref = SerialNumberLog
        #     .objects
        #     .filter(serial_number=serial_number_ref.serial_number,
        #             workorder=serial_number_ref.workorder,
        #             station=serial_number_ref.station.name
        #     )
        
        log = SerialNumberLog(
                    serial_number=serial_number_ref.serial_number,
                    workorder=serial_number_ref.workorder_id.pk,
                    model=serial_number_ref.model_id.pk,
                    station=serial_number_ref.station_id.pk,
                    user=str(request.user),
                    event=event,
                    log_type=0
                    )
        log.full_clean()
        log.save()
        
        response = True

    return response
