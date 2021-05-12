from pyrfc import Connection
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import json
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
def getWOConfirmation(request):
    dataBuffer = request._body
    dataBuffer = eval(dataBuffer)
    work_order = dataBuffer['WO']
    SAP = SAPConnection(ASHOST='10.18.222.152', SYSNR='00', CLIENT='902', USER='FIIWSIS', PASSWD='foxcnn1', LANG='EN')
    PLANT = "FIIO"
    ZAMZ = [
        {
            "AUFNR" : work_order,
            "BMENG" : str(1),
            "PALLET" : "",
            "CARTON" : "",
            "SFCUSR" : "",
            "MSGTP" : "",
            "MSGTX" : "",
            "CONF_NO" : "0",
            "CONF_CNT" : "0",
        }
    ]
    res = SAP.connection.call('ZRFC_AMZ_COFWO_002', PLANT = PLANT, ZAMZ01 = ZAMZ)
    returncode = res['ZAMZ01'][0]['MSGTP']
    returnmessage = res['ZAMZ01'][0]['MSGTX']
    result = {"return_code": returncode, "returnmessage": returnmessage}
    result_json = json.dumps(result)
    return HttpResponse(result_json)