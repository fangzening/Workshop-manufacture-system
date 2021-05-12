from django.apps import apps
from .serialnumber_scan import serialnumber_scan




def create_log(data):
    response = 'Success'
    if 'log' in data:
        serial_number = data['serial_number']

        serial_number = serialnumber_scan(data)

        SerialNumberLog = apps.get_model('manufacturing', 'SerialNumberLog')
        # log_ref = SerialNumberLog
        #     .objects
        #     .filter(serial_number=serial_number_ref.serial_number,
        #             workorder=serial_number_ref.workorder,
        #             station=serial_number_ref.station.name
        #     )
        if serial_number:
            
            log = SerialNumberLog(
                        serial_number=serial_number.pk,
                        workorder=serial_number.workorder_id,
                        model=serial_number.model_id,
                        station=serial_number.station_id,
                        user=data['user'],
                        event=data['log'],
                        log_type=0
                        )
            log.full_clean()
            log.save()
        
        
    else:
        response = 'Failed'
    return response