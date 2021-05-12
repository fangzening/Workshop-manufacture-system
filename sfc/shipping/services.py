from django.apps import apps
import xlwt
# from pyrfc import Connection

class ShipLoadService():
    def __init__(self):
        self.ShipLoad = apps.get_model('shipping','ShipLoad')

    '''
    get bol data from SAP
    '''
    # def call_sap(self,bol):

    #     def get_config():
    #         ASHOST='10.18.222.152'
    #         SYSNR='00'
    #         CLIENT='902'
    #         USER='FIIWSYS'
    #         PASSWD='foxcnn1'
    #         conn = Connection(ashost=ASHOST, sysnr=SYSNR, client=CLIENT, user=USER, passwd=PASSWD)
    #         return conn


    #     conn = get_config()
        

    #     if conn:
    #         desc = conn.get_function_description('ZRFC_GET_WO_HEADER_AMZ').parameters
    #         print(desc)

    #     else:
    #         pass



    def validate(self,bol):
        _bol_ref = None
        try:
            _bol_ref = self.ShipLoad.objects.get(billoflading_id=bol)

        except Exception as e:
            print("error: ", e)

        return _bol_ref

    def create_doc(self,response):

        response['Content-Disposition'] = 'attachment; filename="git.xls"'
    
        wb = xlwt.Workbook(encoding='utf-8')
        ws =wb.add_sheet('OutFactoryTable')
        row_num = 0

        font_style = xlwt.XFStyle()
        
        columns = ['Application','Brand']
                        
 

        for col in range(len(columns)):
            ws.write(row_num,col, columns[col],font_style)

        for col in range(len(columns)):
            ws.write(1,col, columns[col],font_style)

        

        wb.save(response)

        return PayLoad(200,"Success")




class PayLoad():
    def __init__(self,_status,_message):
        self.status = _status
        self.message = _message


    def get_data(self):
        return {
                'status':self.status,
                'message' : self.message,
                }
            