from django.apps import apps
from django.db import connection
from django.db import IntegrityError
from django.db.utils import InternalError
from Internal.data import DataLayer

'''
    func: update status of serial numbers
    params:
        data - dictionary that should contain param serial_number, status_name

    return:
        response from stored proc
'''
def change_status(data):
        
    STORED_PROC = 'sn_status_update'
    response = None
    results = None
    _cursor = connection.cursor()

    if 'serial_number' in data and 'status_name' in data:
        serial_number = str(data['serial_number'])
        status_name = str(data['status_name'])
    else:
        serial_number = ''

    try:
        dbal = DataLayer()
        params = (serial_number, status_name)
        results =  dbal.runstoredprocedure(STORED_PROC, params)
    except Exception as e:
        print("Exception")
        results = e
    finally:
        _cursor.close()

    if results != None:

        response = results
    else:
        response = "Could Not Reach Host"
    return response
