from django.apps import apps
from django.db import connection
from django.db import IntegrityError
from django.db.utils import InternalError
from Internal.data import DataLayer
import json


'''
    func: validate if a serial number is in station layer
    params:
        data - dictionary that should contain param serial_number

    return:
        response from stored proc
'''
def validator(data):
        
    STORED_PROC = 'assy_validator'

    _cursor = connection.cursor()

    if 'serial_number' in data:
        serial_number = str(data['serial_number'])
    else:
        serial_number = ''

    response = None
    try:
        dbal = DataLayer()
        params = (serial_number, "")
        results =  dbal.runstoredprocedure(STORED_PROC, params)
    except Exception as e:
        print("Exception")
        results = e
    finally:
        _cursor.close()
    

    if results != None:
        print("results: ",results)
        payload = results
        try:

            payload = json.loads(results)
        except Exception as e:
            payload = {
                'message' : results,
                'status' : 401
                }
            print(e)
        response = payload
    else:
        response = {"status":420,"message":"Could Not Reach Host"}
    return response
