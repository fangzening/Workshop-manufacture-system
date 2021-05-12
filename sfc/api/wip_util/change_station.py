import json

from django.apps import apps
from django.db import connection
from django.http import HttpRequest

from .serialnumber_scan import serialnumber_scan
from .create_log import create_log
from .change_status import change_status

from .get_wo_confirmation import getWOConfirmation


def change_station(data, state):

    # state = data.get('state')
    # should be the station id/route id
    station = data['stationid']
    
    if not state:
        state = 'PASS'

    # response to return false or the sn reference
    response = False
    # get models
    
    station_routes = apps.get_model('line', 'StationRoutes')

    # gets the reference we want from station routes
    station_ref = station_routes.objects.filter(station=station, state=state)
    next_station = None
    serial_number_ref = serialnumber_scan(data)
    if station_ref:
        station_ref = station_ref.first()
        if station_ref.next_station != None:
            next_station = station_ref.next_station
        else:
            if serial_number_ref:
                serialnumber = serial_number_ref.serial_number
                work_order_obj = serial_number_ref.workorder_id
                work_order = work_order_obj.workorder_id
                data_set = {"WO": work_order}
                req = HttpRequest()
                req.user = ''
                req.method = 'GET'
                req._body = json.dumps(data_set)
                response = getWOConfirmation(req)
                json_rep = json.loads(response.content)
                if json_rep['ReturnCode'] != '00':
                    print('CWO calling SAP error')
                    cursor = connection.cursor()
                    sql = '''CALL public.sap_record_insert(%s, %s, %s, %s)'''
                    cursor.execute(sql, [serialnumber, 'CWO', work_order, '01/01/1900'])

    if serial_number_ref and next_station:
        old_station = serial_number_ref.station_id
        if serial_number_ref.sn_status_category.name == 'Generated':
            change_status({'serial_number':serial_number_ref.serial_number,'status_name':'In-Line'})
            
        data['log'] = "{} moved from {} to {}".format(serial_number_ref,old_station,next_station)
        create_log(data)
        serial_number_ref.station_id = next_station

        # add event for ssn log
       

        
        serial_number_ref.save()
        
        response = True


    
    return response