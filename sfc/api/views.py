import uuid

from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework import permissions

from .wip_util.serialnumber_scan import serialnumber_scan
from .wip_util.check_station import check_station
from .wip_util.change_station import change_station
from .wip_util.create_log import create_log
from .keypart.create_keypart import create_keypart
from .keypart.check_keypart import check_keypart
from django.http import HttpResponse
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpRequest
import requests
from django.http import HttpRequest, QueryDict, HttpResponse, Http404
import base64
from datetime import datetime, date
from django.http import QueryDict
from django.utils.timezone import make_aware
from .wip_util.assembly_validator import validator
from pyrfc import Connection

# model imports
SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
TestingResult = apps.get_model('manufacturing', 'TestingResult')
FailureCode = apps.get_model('manufacturing', 'FailureCode')
RepairMain = apps.get_model('manufacturing', 'RepairMain')

Station = apps.get_model('line', 'Station')
Route = apps.get_model('line', 'Route')
KeyPart = apps.get_model('manufacturing', 'KeyPart')
MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')
Rule = apps.get_model('rules', 'Rule')
Bom = apps.get_model('manufacturing', 'Bom')
Stationroutes = apps.get_model('line', 'Stationroutes')


## truck load API start ##
def updateTruckLoadDetail(request):
    # truck_format = {  #input json format
    #     'container' : '001510',
    #     'seal' : '49480940',
    #     'dn_list' : ['600010045', '600010046', '600010047']
    # }
    dataBuffer = request._body  # request._body will return a str of dict
    dataBuffer = eval(dataBuffer)  # convert str of dict into a dict
    container = dataBuffer['container']
    seal = dataBuffer['seal']
    dn_list = dataBuffer['dn_list']


## truck load API end ##

## get delivery detail API #
class SAPConnection():
    def __init__(self, ASHOST, SYSNR, CLIENT, USER, PASSWD, LANG='EN'):
        # from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
        self.connection = Connection(ashost=ASHOST, sysnr=SYSNR, client=CLIENT, user=USER, passwd=PASSWD, lang=LANG)
        # self.connection = Connection(ashost='10.18.222.152', sysnr='00', client='902', user='FIIWSYS', passwd='foxcnn1',

####################################################
## confirm with SAP with work order confirmation API
## input: {'WO' : '000000000000'}
####################################################


@api_view(['POST', 'GET'])
@permission_classes((permissions.AllowAny,))
@permission_classes([IsAuthenticated])
def getDeliveryNumber(request):
    dataBuffer = request._body  # request._body will return a str of dict
    dataBuffer = eval(dataBuffer)  # convert str of dict into a dict

    sales_order = dataBuffer['salesorder']
    part_number = dataBuffer['sku']
    qty = dataBuffer['qty']
    user = dataBuffer['username']
    pallet_id = dataBuffer['palletlist']

    from django.db import connection
    cursor = connection.cursor()
    line_item_get_query = '''SELECT salesorder_item FROM public.shipping_salesorderdetail where salesorder_id = '%s' and skuno_id = '%s' LIMIT 1;''' % (
        str(sales_order), part_number)
    cursor.execute(line_item_get_query)
    item_number = cursor.fetchall()
    if len(item_number) == 0:
        return HttpResponse("Model ID did not find!")
    item_number = item_number[0][0]
    SAP = SAPConnection(ASHOST='10.18.222.152', SYSNR='00', CLIENT='902', USER='FIIWSYS', PASSWD='foxcnn1', LANG='EN')
    IT_SO_H = [
        {
            "VBELN": str(sales_order),
            "ZSHPNO": "",
            "ZDATE": date.today(),
            "ZTIME": "",
            "ZCARR": "",
            "LICENSE": ""
        }
    ]
    IT_SO_D = [
        {
            "VBELN": str(sales_order),
            "ZCGN": "",
            "ZCGNS": str(item_number),
            "ZPN": str(part_number),
            "ZQTY": str(qty),
            "REF1": "",
            "REF2": ""
        }
    ]
    try:
        ### CALL RFC ZRFC_SD_RDS_0003a
        SAP_call = SAP.connection.call('ZRFC_SD_RDS_0003A', IT_SO_H=IT_SO_H, IT_SO_D=IT_SO_D)

        SAP_return_detail = SAP_call['RETURN'][0]
        vbeln_a, vbeln_l, returncode, mess = SAP_return_detail.values()
        workorder = sales_order
        user = str(user)
        if returncode != "00":
            for pallet in pallet_id:
                serialnumber = pallet
                json_manufacturing_serialnumberlog = {
                    'serial_number': serialnumber,
                    'workorder': workorder,
                    'model': part_number,
                    'station': 'shipping',
                    'in_station_time': str(date.today()),
                    '"user"': user,
                    'event': '',
                    'log_type': ''
                }
                serialnumberlog_insertion = list(json_manufacturing_serialnumberlog.values())
                query_manufacturing_serialnumberlog = 'INSERT INTO public.manufacturing_serialnumberlog(serial_number, workorder, model, station, in_station_time, "user", event, log_type) ' \
                                                      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
                cursor.execute(query_manufacturing_serialnumberlog, tuple(serialnumberlog_insertion))
        else:
            serialnumber = vbeln_l
            json_manufacturing_serialnumberlog = {
                'serial_number': serialnumber,
                'workorder': workorder,
                'model': part_number,
                'station': 'shipping',
                'in_station_time': str(date.today()),
                '"user"': user,
                'event': '',
                'log_type': ''
            }
            serialnumberlog_insertion = list(json_manufacturing_serialnumberlog.values())
            query_manufacturing_serialnumberlog = 'INSERT INTO public.manufacturing_serialnumberlog(serial_number, workorder, model, station, in_station_time, "user", event, log_type) ' \
                                                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'
            cursor.execute(query_manufacturing_serialnumberlog, tuple(serialnumberlog_insertion))
        if returncode == '00':
            ### CALL ZMES_MAINDATA_029
            sap_ZMES_MAINDATA_029_ret = SAP.connection.call("ZMES_MAINDATA_029", I_VBELN='5100019917', I_WERKS='FII6',
                                                            I_VSTEL='FII6')
            shiporderdetail = sap_ZMES_MAINDATA_029_ret['SHIPORDERDETAIL'][0]
            shiporderheader = sap_ZMES_MAINDATA_029_ret['SHIPORDERHEADER'][0]
            json_shipping_deliverynumber = {
                'deliverynumber_id': vbeln_l,
                'customer_po': shiporderheader['BSTKD'],
                'customer_name': shiporderheader['NAME1SALE'],
                'shipped': 0,
                'invoice_no': '',
                'confirmed': 0,
                'confirmed_date ': str(date.today()),
                'cancelled': 0,
                'confirmed_856': 0,
                'confirmed_856_date': str(date.today()),
                'ship_date': str(date.today()),
                'customer_soldto': shiporderheader['KUNAG'],
                'order_type': '',
                'customer_no': shiporderheader['KUNNR'],
                'bill_of_landing': shiporderheader['BOLNR'],
                'plant_code': shiporderheader['WERKS'],
                'delivery_type': shiporderheader['LFART'],
                'creator': str(user),
                'create_date': str(datetime.today()),
                'updater': str(user),
                'update_date': str(datetime.today()),
                'salesorder_id': vbeln_a
            }
            shipping_deliverynumber_insertion = list(json_shipping_deliverynumber.values())
            query_shipping_deliverynumber = 'INSERT INTO public.shipping_deliverynumber(deliverynumber_id, customer_po, ' \
                                            'customer_name, shipped, invoice_no, confirmed, confirmed_date, cancelled, ' \
                                            'confirmed_856, confirmed_856_date, ship_date, customer_soldto, order_type, ' \
                                            'customer_no, bill_of_landing, plant_code, delivery_type, creator, ' \
                                            'create_date, updater, update_date, salesorder_id) ' \
                                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ' \
                                            '%s, %s, %s, %s, %s, %s);'
            cursor.execute(query_shipping_deliverynumber, tuple(shipping_deliverynumber_insertion))

            for single_pallet in pallet_id:
                json_shipping_palletdeliverynumber = {
                    'creator': user,
                    'create_date': str(date.today()),
                    'updater': user,
                    'update_date': str(date.today()),
                    'deliverynumber_id': vbeln_l,
                    'pallet_id': single_pallet
                }
                shipping_palletdeliverynumber_insertion = list(json_shipping_palletdeliverynumber.values())
                query_shipping_palletdeliverynumber = 'INSERT INTO public.shipping_palletdeliverynumber(creator, ' \
                                                      'create_date, updater, update_date, deliverynumber_id, ' \
                                                      'pallet_id) VALUES (%s, %s, %s, %s, %s, %s);'
                cursor.execute(query_shipping_palletdeliverynumber, shipping_palletdeliverynumber_insertion)

            json_shipping_deliverynumberdetail = {
                'row_id': uuid.uuid1(),
                'salesorder_item': vbeln_a,
                'request_qty': shiporderdetail['LFIMG'],
                'current_qty': str(qty),  # pallet1, pallet2, pallet3
                'ship_qty': '0',
                'customer_pn': shiporderdetail['KDMAT'],
                'customer_po': shiporderdetail['BSTKD'],
                'customer_line_item': shiporderdetail['POSEX'],
                'net_weight': shiporderdetail['NTGEW'],
                'net_price': shiporderdetail['NETPR'],
                'creator': user,
                'create_date': str(date.today()),
                'updater': user,
                'update_date': str(date.today()),
                'skuno_id': part_number,
                'deliverynumber_id': vbeln_l,
                'salesorder_id': vbeln_a,
            }
            shipping_deliverynumberedtail_insertion = list(json_shipping_deliverynumberdetail.values())
            query_shipping_deliverynumberdetail = "INSERT INTO public.shipping_deliverynumberdetail(" \
                                                  "row_id, " \
                                                  "salesorder_item, " \
                                                  "request_qty, " \
                                                  "current_qty, " \
                                                  "ship_qty, " \
                                                  "customer_pn, " \
                                                  "customer_po, " \
                                                  "customer_line_item," \
                                                  "net_weight, " \
                                                  "net_price, " \
                                                  "creator, " \
                                                  "create_date, " \
                                                  "updater, " \
                                                  "update_date, " \
                                                  "skuno_id, " \
                                                  "deliverynumber_id, " \
                                                  "salesorder_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(query_shipping_deliverynumberdetail, shipping_deliverynumberedtail_insertion)
        res_temp = {
            "DeliveryNumber": vbeln_l,
            "ReturnCode": returncode,
            "ErrorMessage": mess
        }
        res = json.dumps(res_temp)
        return HttpResponse(res)
    except Exception as e:
        res_temp = {
            "DeliveryNumber": "0000",
            "ReturnCode": "01",
            "ErrorMessage": str(e)
        }
        res = json.dumps(res_temp)
        return HttpResponse(res)


## Get Delivery Detal API END

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkssn(request):
    return checkssn_function(request)


def checkssn_function(request):
    post_data = request.GET

    serial_number = None
    station_id = None

    if post_data:
        if 'serial_number' in post_data and 'stationid' in post_data:
            serial_number = post_data['serial_number']
            station_id = post_data['stationid']

    if serial_number and station_id:

        serial_number_obj = serialnumber_scan(post_data)

        station_ref = check_station(post_data)

        if serial_number_obj:

            if station_ref:

                if station_ref[1] == 200:

                    keyparts = KeyPart.objects.filter(serialnumber=serial_number_obj)

                    # collect keyparts based on rules

                    rules_list = []
                    keypart_list = []

                    station_ref = Station.objects.filter(pk=station_id).first()

                    route_ref = Route.objects.filter(model=serial_number_obj.model_id)
                    if route_ref:
                        route_ref = route_ref.first()

                    if station_ref and route_ref:
                        rules_list = Rule.objects.filter(route=route_ref, station=station_ref)

                    keypart_list = KeyPart.objects.filter(serialnumber=serial_number_obj.pk)

                    # collect keyparts with rules applied

                    if rules_list and keypart_list:
                        keypart_list = serial_number_obj.get_filtered_keyparts(station_ref.pk)

                    elif route_ref and keypart_list:

                        keypart_list = serial_number_obj.get_filtered_keyparts(station_ref.pk)

                    if keypart_list:

                        keypartmodels = set()
                        for keypart in keypart_list:
                            keypartmodels.add(keypart.model_id)

                        # for keypart in keypart_list:
                        # print("Serial no model:",serial_number_obj.model ,"Key part:", keypart.part)

                        # print("Material number:", serial_number_obj.model.model, "bom component:",keypart.part.model)

                        # for item in Bom.objects.filter(material_number=serial_number_obj.model.model, bom_component=keypart.part.model):
                        #     bom.append(item)


                        WorkOrderDetail = apps.get_model('manufacturing', 'WorkOrderDetail')
                        wo_details = WorkOrderDetail.objects.filter(model_id__in=keypartmodels, workorder_id=serial_number_obj.workorder_id)
                        items = []
                        items.append({'status': 200})


                        # filter wo detail for information
                        for entry in wo_details:
                            item = {}
                            item['part_no'] = str(entry.model_id)
                            item['part_name'] = entry.model_desc
                            item['qty'] = entry.bom_usage
                            item['installation_point'] = entry.installation_point
                            items.append(item)

                            # serializers.serialize('json', bom, fields=('name','size'))

                        # serializer = BomSerializer(bom, many=True)
                        # serializer = BomSerializer()
                        # data = serializer.serialize(bom)
                        # print("type of data:", type(data))
                        # print(items)
                        # return JsonResponse(serializer.data, safe=False)

                        return JsonResponse(items, safe=False)

                    else:
                        error = {
                            'status': 404,
                            'message': 'There are no keyparts related to this serial number',
                        }
                else:
                    error = {
                        'status': 405,
                        'message': "Serial Number is not allowed at this station.",
                    }
            else:
                error = {
                    'status': 404,
                    'message': station_ref[0]
                }
        else:
            error = {
                'status': 404,
                'message': station_ref[0]
            }
    else:
        error = {
            'status': 403,
            'message': "serial_number and stationid must be provided.",
        }

    return JsonResponse(error)


# @login_required
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def scankeypart(request):
    return scankeypart_function(request)


def scankeypart_function(request):
    serial_number = None
    station_id = None

    checkkeypart_payload = None

    parts = []
    post_data = None
    json_data = None
    message = "Success"
    status = 200

    def json_config():
        data = {"status": status, "message": message}

        return JsonResponse(data)

    def data_integrity_check():
        nonlocal json_data, status, message, post_data

        if request.method == 'POST':

            if isinstance(request.body, str):

                try:
                    json_data = json.loads(request.body)
                except:

                    status = 505
                    message = "Error loading JSON"
                    return json_config()

            else:

                try:
                    post_data = request.body.decode('utf-8')
                    json_data = json.loads(post_data)
                except:
                    status = 505
                    message = "Error loading JSON"
                    return json_config()
        else:

            message = "Only Post Requests Allowed"
            status = 509

            return json_config()

    def call_checkkeypart():
        nonlocal message, status, checkkeypart_payload

        if json_data:

            # get parts from other endpoint

            try:
                checkkeypart_payload = checkkeypart_function(POST_request_parser(request))
                checkkeypart_payload = checkkeypart_payload.content
                checkkeypart_payload = json.loads(checkkeypart_payload)
            except Exception as e:
                print(e)

                status = 505
                message = "Error loading JSON"

                return json_config()
        else:
            status = 506
            message = "No JSON was received"
            return json_config()

        if 'message' in checkkeypart_payload and 'status' in checkkeypart_payload:

            if checkkeypart_payload['status'] != 200:
                message = checkkeypart_payload['message']
                status = checkkeypart_payload['status']
                return json_config()

    # format parts for kp insertion
    def format_parts():
        nonlocal serial_number, station_id, parts, json_data

        serial_number = json_data['serial_number']
        station_id = json_data['stationid']
        parts = json_data['partsn']

        json_data['user'] = str(request.user)
        if parts and 'PartSN' not in parts[0]:
            # implement later
            status = 511
            message = "CustPartNo Not implemented yet"
            return json_config()

    # iterate through parts and try to create
    def create_keyparts():
        nonlocal status, message
        response = "success"
        counter = 0

        while counter < len(parts):
            response = create_keypart(json_data, parts[counter])

            counter += 1

            if response[1] != "Success":
                status, message = response

                break
        return json_config()

    def station_change():
        serial_number_ref = SerialNumber.objects.filter(pk=serial_number)
        serial_number_ref = serial_number_ref.first()

        if serial_number_ref:
            remaining = serial_number_ref.get_unfinished_keyparts(json_data['stationid'])

            if len(remaining) == 0:
                change_station(json_data, "PASS")

    data_check = data_integrity_check()
    if type(data_check) == JsonResponse:
        return data_check

    api_call = call_checkkeypart()
    if type(api_call) == JsonResponse:
        return api_call

    formatp = format_parts()
    if type(formatp) == JsonResponse:
        return formatp

    insert_parts = create_keyparts()
    if type(insert_parts) == JsonResponse:
        station_change()

        return insert_parts

    return json_config()


# post results of test station
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def testssn(request):
    return testssn_function(request)


'''

station id
serial number
result = state

symptom
failure code

'''


def testssn_function(request):
    if request.method == 'POST':

        post_data = None
        json_data = None
        response = dict()

        if isinstance(request.body, str):

            try:
                json_data = json.loads(request.body)


            except:

                status = 505
                message = "Error loading JSON"

        else:

            try:
                post_data = request.body.decode('utf-8')
                json_data = json.loads(post_data)

            except:

                response = {
                    'status': 505,
                    'message': "Not valid json."
                }

                return JsonResponse(response)

        serial_number = None
        station_id = None
        result = None

        if 'serial_number' in json_data and 'stationid' in json_data and 'result' in json_data:
            serial_number = json_data['serial_number']
            station_id = json_data['stationid']
            result = json_data['result']
            json_data['user'] = request.user

        if serial_number and station_id and result:
            serial_number_obj = serialnumber_scan(json_data)
            station = check_station(json_data)

            if serial_number_obj and station:
                if station[1] == 200:

                    if result != 'PASS' and result != 'FAIL':

                        response = {
                            'status': 400,
                            'message': 'result must be either PASS or FAIL',
                        }
                        return JsonResponse(response)
                    else:
                        insert = False

                        response = {
                            'status': 200,
                            'message': 'Success',
                        }
                        station_ref = Station.objects.filter(pk=station_id).first()
                        if result == 'PASS':

                            # try:
                            test_ref = TestingResult(
                                serial_number=serial_number_obj,
                                station=station_ref.pk,
                                testing_date=make_aware(datetime.now()),
                                creator=str(request.user),
                                result=1
                            )
                            test_ref.save()
                            json_data['log'] = "SN: {}, result: {}".format(json_data['serial_number'], "PASS")
                            create_log(json_data)
                            change_station(json_data, result)

                            insert = True
                            # except:
                            # insert = False

                            if not insert:
                                response = {
                                    'status': 407,
                                    'message': 'unknown error occured'
                                }
                            return JsonResponse(response)
                        else:

                            if 'failure_code' in json_data and 'symptom' in json_data:
                                failure_code = json_data['failure_code']
                                symptom = json_data['symptom']

                                failure_code_ref = FailureCode.objects.filter(failure_code=failure_code)

                                if failure_code_ref:
                                    failure_code_ref = failure_code_ref.first()

                                    insert = True

                                    try:
                                        test_ref = TestingResult(
                                            serial_number=serial_number_obj,
                                            station=station_ref.pk,
                                            testing_date=make_aware(datetime.now()),
                                            creator=str(request.user),
                                            result=0
                                        )

                                        repair_ref = RepairMain(
                                            serial_number=serial_number_obj,
                                            create_date=make_aware(datetime.now()),
                                            station=station_ref.pk,
                                            failure_code=failure_code_ref,
                                            failure_description=symptom,
                                            creator=str(request.user),
                                            result=0
                                        )

                                        test_ref.save()
                                        repair_ref.save()
                                        json_data['log'] = "SN: {}, result: {}, failure_code: {}".format(
                                            json_data['serial_number'], "FAIL", failure_code)
                                        create_log(json_data)

                                        change_station(json_data, result)
                                    except:
                                        insert = False

                                    if not insert:
                                        response = {
                                            'status': 407,
                                            'message': 'unknown error occured'
                                        }
                                        return JsonResponse(response)
                                else:
                                    response = {
                                        'status': 406,
                                        'message': "Failure Code Doesn't Exist"
                                    }
                                    return JsonResponse(response)
                            else:
                                response = {
                                    'status': 408,
                                    'message': 'Missing Data For Failed Test',
                                }

                            return JsonResponse(response)

                    return JsonResponse(response)

                else:
                    error = {
                        'status': 405,
                        'message': station[0],
                    }
            else:
                if not serial_number_obj:
                    error = {
                        'status': 404,
                        'message': 'Serial Number does not exist',
                    }
        else:
            error = {
                'status': 403,
                'message': 'stationid, serial_number, and result are all required.'
            }

        return JsonResponse(error)


# returns if partno/partsn are valid to enter into database
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkkeypart(request):
    return checkkeypart_function(request)


def checkkeypart_function(request):
    serial_number = None
    station_id = None
    parts = None
    part_list = None
    partsn_list = None
    parts = []
    post_data = None
    message = "Success"
    status = 200

    def json_config():
        data = {"status": status, "message": message}

        resp = JsonResponse(data)

        return resp

    if request.method == 'GET':
        post_data = request.GET
    else:
        message = "Only GET Requests Allowed"
        status = 509

    def data_integrity_check():
        nonlocal status, message

        if post_data:
            if 'serial_number' in  post_data and 'stationid' in  post_data and 'partsn' in  post_data or 'partno' in post_data:
                nonlocal serial_number, station_id, part_list, partsn_list, parts
                serial_number = post_data['serial_number']
                station_id = post_data['stationid']
                part_list = post_data.getlist('partno')
                partsn_list = post_data.getlist('partsn')
                parts = []
            else:
                status = 503
                message = "Missing Data"
                return json_config()
        else:
            status = 506
            message = "No JSON was received"
            return json_config()

    def check_sn():
        nonlocal status, message
        serialnumber_ref = None
        if serial_number:
            serialnumber_ref = serialnumber_scan(post_data)

            if not serialnumber_ref:
                status = 505
                message = "No Serial Number Found"
                return json_config()

        else:
            message = "No Serial Number in Request"
            status = 504
            return json_config()
        return serialnumber_ref

    # stored proc in db to validate if an sn can be scanned in on the line
    def is_scannable():
        _req = validator(post_data)
        _resp = None
        if type(_req) == dict:
            _status = _req['status']
            if _status == 200:
                _resp = True
            else:
                _resp = JsonResponse(_req,status=200)
        return _resp



    def check_sn_station():
        nonlocal status, message

        station_check = check_station(post_data)

        if station_check[1] != 200:
            message = station_check[0]
            status = station_check[1]
            return json_config()

        return station_check

    def format_parts():
        nonlocal status, message

        if part_list and partsn_list and len(part_list) == len(partsn_list):

            for element in range(len(part_list)):
                parts.append({
                    'PartNo': part_list[element],
                    'PartSN': partsn_list[element]
                })

        elif 'serial_number' in post_data and 'stationid' in post_data and 'partsn' in post_data:
            serial_number = post_data['serial_number']
            station_id = post_data['stationid']
            for element in range(len(partsn_list)):
                parts.append({
                    'PartSN': partsn_list[element]
                })


        else:
            # implement later
            status = 511
            message = "CustPartNo Not implemented yet"
            pass

        return None

    def check_parts():
        nonlocal status, message
        response = "success"
        counter = 0

        while counter < len(parts):

            response = check_keypart(post_data, parts[counter])

            counter += 1

            if response[1] != "Success":
                status, message = response
                break

        return json_config()

    # call all functions
   
    data_check = data_integrity_check()
    if type(data_check) == JsonResponse:
        
        return data_check

    sn_check = check_sn()
    if type(sn_check) == JsonResponse:
        return sn_check


    _validator = is_scannable()
    if type(_validator) == JsonResponse:
        return validator

    check_station_sn = check_sn_station()
    if type(check_station_sn) == JsonResponse:
        return check_station_sn

    formatp = format_parts()
    if type(formatp) == JsonResponse:
        return formatp

    part_check = check_parts()
    if type(part_check) == JsonResponse:
        return part_check

    return json_config()


# convert post to get request
def POST_request_parser(request):
    json_data = None
    query_string = None
    req = HttpRequest()
    req.method = "GET"
    req.user = request.user

    if isinstance(request.body, str):

        try:
            json_data = json.loads(request.body)
        except:
            status = 505
            message = "Error loading JSON"
    else:
        try:
            post_data = request.body.decode('utf-8')
            json_data = json.loads(post_data)
        except:
            status = 505
            message = "Error loading JSON"

    if 'partsn' in json_data and 'serial_number' in json_data and 'stationid' in json_data:
        serial_number = json_data['serial_number']
        stationid = json_data['stationid']
        parts = json_data['partsn']
        partno = []
        partsn = []

        for part in parts:
            if 'PartNo' in part and 'PartSN' in part:

                partno.append(part['PartNo'])
                partsn.append(part['PartSN'])
            elif 'PartSN' in part:
                partsn.append(part['PartSN'])

        # generate the query string for get request
        if len(parts) == len(partno):
            query_string = "serial_number=" + str(serial_number) + "&"
            query_string += "stationid=" + str(stationid)

            for i in range(len(partno)):
                query_string += "&partno=" + str(partno[i])
                query_string += "&partsn=" + str(partsn[i])
            payload = QueryDict(query_string)

        elif len(partsn) != 0:
            query_string = "serial_number=" + str(serial_number) + "&"
            query_string += "stationid=" + str(stationid)
            for i in range(len(partsn)):
                # query_string += "&partno=" + str(partno[i])
                query_string += "&partsn=" + str(partsn[i])
            payload = QueryDict(query_string)

        req.GET = payload

    return req


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getpart(request):
    return getpart_function(request)


def getpart_function(request):

    error = {
        'status': 500,
        'message': 'Something went wrong.'
    }

    if 'serial_number' in request.GET and 'stationid' in request.GET:

        sn = request.GET['serial_number']
        station_id = request.GET['stationid']

        serial_number = SerialNumber.objects.filter(pk=sn)

        json_data = {
            'serial_number': sn,
            'stationid': station_id
        }

        if serial_number:
            serial_number_ref = serial_number.first()

            station = check_station(json_data)

            status = station[1]

            if status == 200:

                data = serial_number_ref.model_id.model_id

                result = {
                    'status': 200,
                    'message': "Success",
                    "part": data
                }

                return JsonResponse(result, safe=False)
            else:
                error = {
                    'status': 405,
                    'message': "Serial Number not at this station."
                }

        else:
            error = {
                'status': 404,
                'message': "Serial number does not exist."
            }
    else:
        error = {
            'status': 403,
            'message': 'serial_number and stationid are required.'
        }

    return JsonResponse(error)


if __name__ == "__main__":
    SAP = SAPConnection(ASHOST='10.18.222.152', SYSNR='00', CLIENT='902', USER='FIIWSYS', PASSWD='foxcnn1', LANG='EN')
    print(SAP)
