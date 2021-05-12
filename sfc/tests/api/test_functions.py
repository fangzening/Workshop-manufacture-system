from django.urls import reverse, resolve
from mixer.backend.django import mixer
import pytest
import json
from django.http import HttpRequest, QueryDict
from api.views import getpart_function
from api.views import checkkeypart_function

@pytest.mark.django_db
class TestGetPartAPI:
    

    '''
    function: test_missing_station_403
    params: self
    desc: test GetPart endpoint for 403 error(missing stationid)  
    
    '''
    def test_missing_station_403(self):
        model = mixer.blend('manufacturing.MaterialMaster', model_id='123')
        serial_number = mixer.blend('manufacturing.Serialnumber',serial_number='abc123', model_id=model)

        req = HttpRequest()
        req.META['REQUEST_METHOD'] = "GET"
        req.user = 'james'
        payload = None
        req.method = "GET"
        payload = {
            "serial_number" : 123,
            }
            
        if payload:
            req.GET = payload

        response = None
        message = None
        status = None
        if payload:
            response = getpart_function(req)

        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                message='Unknown error occured'
        
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            message = json_resp['message']
            status = json_resp['status']
       
        assert message == 'serial_number and stationid are required.' and status == 403

    def test_missing_serialnumber_403(self):

        model = mixer.blend('manufacturing.MaterialMaster', model_id='123')
        serial_number = mixer.blend('manufacturing.Serialnumber',serial_number='abc123', model_id=model)

        req = HttpRequest()
        req.META['REQUEST_METHOD'] = "GET"
        req.user = 'james'
        payload = None
        req.method = "GET"
        payload = {
            "serial_number" : 123,
            }
            
        if payload:
            req.GET = payload

        response = None
        message = None
        status = None
        if payload:
            response = getpart_function(req)

        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                message='Unknown error occured'
        
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            message = json_resp['message']
            status = json_resp['status']
       
        assert message == 'serial_number and stationid are required.' and status == 403

    def test_serialnumber_exist_404(self):
        model = mixer.blend('manufacturing.MaterialMaster', model_id='123')
        
        station = mixer.blend('line.station',station_id='test')
        serial_number = mixer.blend('manufacturing.Serialnumber',serial_number='abc123', model_id=model, station_id=station)

        req = HttpRequest()
        req.META['REQUEST_METHOD'] = "GET"
        req.user = 'james'
        payload = None
        req.method = "GET"
        payload = {
            "serial_number" : 123,
            "stationid" : station.station_id
            }

        if payload:
            req.GET = payload

        response = None
        message = None
        status = None
        if payload:
            response = getpart_function(req)

        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                message='Unknown error occured'
        
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            message = json_resp['message']
            status = json_resp['status']
        
        assert message == 'Serial number does not exist.' and status == 404

    def test_sn_not_in_station_405(self):
        model = mixer.blend('manufacturing.MaterialMaster', model_id='123')
        
        station_curr = mixer.blend('line.station',station_id='test')
        station_next = mixer.blend('line.station',station_id='complete')
        serial_number = mixer.blend('manufacturing.Serialnumber',serial_number='abc123', model_id=model, station_id=station_curr)

        req = HttpRequest()
        req.META['REQUEST_METHOD'] = "GET"
        req.user = 'james'
        payload = None
        req.method = "GET"
        payload = {
            "serial_number" : serial_number.serial_number,
            "stationid" : station_next.station_id
            }

        if payload:
            req.GET = payload

        response = None
        message = None
        status = None
        if payload:
            response = getpart_function(req)

        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                message='Unknown error occured'
        
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            message = json_resp['message']
            status = json_resp['status']
        
        assert message == 'Serial Number not at this station.' and status == 405

    def test_success_200(self):
        model = mixer.blend('manufacturing.MaterialMaster', model_id='123')
        station = mixer.blend('line.station',station_id='test')
        serial_number = mixer.blend('manufacturing.Serialnumber',serial_number='abc123', model_id=model, station_id=station)

        req = HttpRequest()
        req.META['REQUEST_METHOD'] = "GET"
        req.user = 'james'
        payload = None
        req.method = "GET"
        payload = {
            "serial_number" : serial_number.serial_number,
            "stationid" : station.station_id
            }
            
        if payload:
            req.GET = payload

        response = None
        message = None
        status = None
        if payload:
            response = getpart_function(req)

        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                message='Unknown error occured'
        
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            message = json_resp['message']
            status = json_resp['status']
       
        assert message == 'Success' and status == 200

@pytest.mark.django_db
class TestCheckKeyPartAPI:

    # pass dictionary to return http get req
    def gen_get_req(self, payload):
        req = HttpRequest()
        req.META['REQUEST_METHOD'] = "GET"
        req.user = 'james'
        req.method = "GET"    
        query_dict = QueryDict('', mutable=True)
        query_dict.update(payload)

        # payload = {}
        req.GET = query_dict

        return req

    def test_missing_data_503(self):
        model = mixer.blend('manufacturing.MaterialMaster', model_id='123')
        station = mixer.blend('line.station',station_id='test')
        serial_number = mixer.blend('manufacturing.Serialnumber',serial_number='abc123', model_id=model, station_id=station)

        payload = {
            "serial_number" : serial_number.serial_number,
            "stationid" : station.station_id
            }

        req = self.gen_get_req(payload)

        response = None
        message = None
        status = None
        json_resp = None

        response = checkkeypart_function(req)

        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                message='Unknown error occured'
        
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            message = json_resp['message']
            status = json_resp['status']
       
        assert message == 'Missing Data' and status == 503

    def test_no_json_506(self):
        payload = {}
        req = self.gen_get_req(payload)

        response = None
        message = None
        status = None
        json_resp = None

        response = checkkeypart_function(req)

        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                message='Unknown error occured'
        
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            message = json_resp['message']
            status = json_resp['status']
       
        assert message == 'No JSON was received' and status == 506


    def test_sn_not_exist_505(self):
        payload = {
            "serial_number" : 123,
            "stationid" : 123,
            "partno" : 456,
            "partsn" : 456,
            }

        req = self.gen_get_req(payload)

        response = None
        message = None
        status = None
        json_resp = None

        response = checkkeypart_function(req)

        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                message='Unknown error occured'
        
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            message = json_resp['message']
            status = json_resp['status']
       
        assert message == 'No Serial Number Found' and status == 505

    def test_sn_not_exist_501(self):
        model = mixer.blend('manufacturing.MaterialMaster', model_id='123')
        station_curr = mixer.blend('line.station',station_id='test')
        station_next = mixer.blend('line.station',station_id='test2')
        serial_number = mixer.blend('manufacturing.Serialnumber',serial_number='abc123', model_id=model, station_id=station_curr)

        payload = {
            "serial_number" : serial_number.serial_number,
            "stationid" : station_next.station_id,
            "partno" : 456,
            "partsn" : 456,
            }
            

        req = self.gen_get_req(payload)

        response = None
        message = None
        status = None
        json_resp = None

        response = checkkeypart_function(req)

        if response:
            try:
                json_resp = json.loads(response.content)
            except:
                message='Unknown error occured'
        
        if json_resp and 'status' in json_resp and 'message' in json_resp:
            message = json_resp['message']
            status = json_resp['status']
       
        assert message == 'Serial Number Not At Station' and status == 501

    '''TEST CASE IS NOT REACHABLE'''
    # def test_sn_not_exist_502(self):
    #     model = mixer.blend('manufacturing.MaterialMaster', model_id='123')
    #     station_curr = mixer.blend('line.station',station_id='test')
    #     serial_number = mixer.blend('manufacturing.Serialnumber',serial_number='abc123', model_id=model, station_id=station_curr)

    #     payload = {
    #         "serial_number" : serial_number.serial_number,
    #         "stationid" : 22,
    #         "partno" : 456,
    #         "partsn" : 456,
    #         }

    #     req = self.gen_get_req(payload)

    #     response = None
    #     message = None
    #     status = None
    #     json_resp = None

    #     response = checkkeypart_function(req)

    #     if response:
    #         try:
    #             json_resp = json.loads(response.content)
    #         except:
    #             message='Unknown error occured'
        
    #     if json_resp and 'status' in json_resp and 'message' in json_resp:
    #         message = json_resp['message']
    #         status = json_resp['status']
       
    #     assert message == "Station doesn't exist" and status == 502