from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.db.utils import IntegrityError
from .services import GitService, ConfigService
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import json
from django.http import JsonResponse, HttpResponse
import csv
import xlwt
from django.apps import apps
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.core.paginator import Paginator
from datetime import datetime

'''
    func:  
        view to upload git excel file

    params:
        None, CBV handles Request object

    return Render object 
'''
class GitDisplay(LoginRequiredMixin, View):
    template_name = './git-upload.html'

    Git = apps.get_model('git','Git')
    def get(self, request): 
        
        data = request.GET
        
        git_list = self.Git.objects.values('po_no').distinct().order_by('po_no')
        context = {}

        if git_list:
            
            if 'po' in data and len(data.get('po')) > 0:
                _po = data.get('po')
                
                po_list = self.Git.objects.filter(po_no=data.get('po'))
                
                _git_list = []

                for git in git_list:
                    
                    if git['po_no'] == _po:
                        
                        git['target_qty'] = len(po_list)
                        git['eta'] = ''
                        git['etd'] = ''
                        git['tracking_no'] = ''
                        git['tracking_company'] = ''

                        current_qty = 0
                        for po in po_list:
                            if po.cpu != None and po.serialnumber != None:
                                current_qty += 1 

                            if git['eta'] == '' and  po.eta != None:
                                git['eta'] = str(po.eta.date())

                            if git['etd'] == '' and  po.etd != None:
                                git['etd'] = str(po.etd.date())

                            if git['tracking_no'] == '' and  po.tracking_no != None:
                                git['tracking_no'] = str(po.tracking_no)

                            if git['tracking_company'] == '' and  po.tracking_company != None:
                                git['tracking_company'] = str(po.tracking_company)


                        git['current_qty'] = current_qty

                        _git_list.append(git)
                
                git_list = _git_list
                
            else:

                for git in git_list:
                    po_list = self.Git.objects.filter(po_no=git['po_no'])
                    
                    
                    git['target_qty'] = len(po_list)
                    git['eta'] = ''
                    git['etd'] = ''
                    git['tracking_no'] = ''
                    git['tracking_company'] = ''
                    current_qty = 0
                    for po in po_list:
                        if po.cpu != None and po.serialnumber != None:
                            current_qty += 1 

                        if git['eta'] == '' and  po.eta != None:
                            git['eta'] = str(po.eta.date())

                        if git['etd'] == '' and  po.etd != None:
                            git['etd'] = str(po.etd.date())

                        if git['tracking_no'] == '' and  po.tracking_no != None:
                            git['tracking_no'] = str(po.tracking_no)
                            
                        if git['tracking_company'] == '' and  po.tracking_company != None:
                            git['tracking_company'] = str(po.tracking_company)


                    git['current_qty'] = current_qty

            paginator = Paginator(git_list,17)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context['page_obj'] = page_obj
            context['git_list'] = git_list

        return render(request,self.template_name,context)

    def dispatch(self,request):
        if request.method == 'GET':
            return self.get(request)
        else:
            if 'json' in request.content_type:
                return self.update(request)
            else:
                return self.post(request)

    def post(self, request):

        context = {}
        git_obj = GitService()
        
        if request.FILES:

            try:
                result = git_obj.upload(request.FILES['file'])
                if result:
                    context['message'] = "Success"
                else:
                    context['message'] = "Fail, File Has Been Uploaded or Has Duplicates"
            except IOError as e:
                print("IO error: ",e)
                context['message'] = "Error Occured When Reading From File"

            except IntegrityError as e:
                print("Integrity Error: ",e)
                context['message'] = "Error Data In Excel File"
            except Exception as e:
                print("Exception: ",e)
                context['message'] = "Error in File"
            if 'message' in context:    
                print(context['message'])  

        git_list = self.Git.objects.values('po_no').distinct().order_by('po_no')

        if git_list:
            
            for git in git_list:
                po_list = self.Git.objects.filter(po_no=git['po_no'])
                
                git['eta'] = ''
                git['etd'] = ''
                git['target_qty'] = len(po_list)
                current_qty = 0
                for po in po_list:
                    if po.cpu != None and po.serialnumber != None:
                        current_qty += 1 

                    if git['eta'] == '' and  po.eta != None:
                        git['eta'] = str(po.eta.date())

                    if git['etd'] == '' and  po.etd != None:
                        git['etd'] = str(po.etd.date())

                git['current_qty'] = current_qty

            paginator = Paginator(git_list,17)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context['page_obj'] = page_obj
            context['git_list'] = git_list   




        return render(request,self.template_name,context)


    def update(self, request):

        
        _data = None
        try:
            _data = json.loads(request.body)
        except Exception as e:
            print(e)

        git_obj = GitService()
        payload = git_obj.update(_data)

        return JsonResponse(payload.get_data())

    


'''
    func:  
        view to fetch asset tag

    params:
        post request containing 'serial_number'

    return JSON payload
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def asset_tag_fetcher(request):

    _jsondata = None
    try:
        # _postdata = request.body.decode("utf-8")
        # _postdata = request.data
        # _jsondata = json.loads(_postdata)
        # _jsondata = _postdata
        _jsondata = request.data
    except Exception as e:
        status = 505
        message = "Error loading JSON"
        print(e)
        return JsonResponse({"status":status,"message":message})
        

    if _jsondata and "serial_number" in _jsondata:
        serial_number = _jsondata['serial_number']        
        git_obj = GitService()
        _payload = git_obj.get_asset_tag(serial_number)
        
        return JsonResponse({"status":_payload.status,"message":_payload.message})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mac_fetcher(request):
    _jsondata = request.GET

    if _jsondata and "serial_number" in _jsondata:
        serial_number = _jsondata['serial_number']

        config_obj = ConfigService()
        _payload = config_obj.mac_parser(serial_number)

        
        return JsonResponse({"status":_payload.status,"message":_payload.message})
    else:
        status = 402
        message = "Missing 'serial_number' in request"
        return JsonResponse({"status":status,"message":message})

'''
    func:  
        view to get git data for a serial number

    params:
        get request containing 'serial_number'

    return JSON payload
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_git(request):
    _jsondata = None
    try:
        _jsondata = request.GET
    except Exception as e:
        status = 505
        message = "Error loading JSON"
        print(e)
        return JsonResponse({"status":status,"message":message})
        

    if _jsondata and "serial_number" in _jsondata:
        serial_number = _jsondata['serial_number']        
        git_obj = GitService()
        _git_data = git_obj.get_git(serial_number).message

        if type(_git_data) == str:
            return JsonResponse({"status":404,"message":_git_data})

        SerialNumber = apps.get_model('manufacturing','SerialNumber')

        serial_number = SerialNumber.objects.filter(serial_number=serial_number).first()

        data = {
            'serial_number': _git_data.serialnumber,
            'po_no': _git_data.po_no,
            'asset_tag_number': _git_data.v_asset_no,
            'nsn': _git_data.nsn,
            'suite': _git_data.config,
            'mac_address': _git_data.bmc_mac,
            'part_no': serial_number.model_id.model_id
        }

        print(data)

        return JsonResponse({"status":200,"message":data})        


'''
move to a service.
right doc later TODO


'''
def download(request):
    if request.method == 'POST':
        data = request.POST
        if 'git' in data:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="git.xls"'

            

            wb = xlwt.Workbook(encoding='utf-8')
            ws =wb.add_sheet('Data')
            row_num = 0

            font_style = xlwt.XFStyle()

           
            columns = ['STATUS','SHIPMENT',
                            'DELIVER DATE','DEST','TRACKING_NO.',
                            'TRACKING_COMPANY','PO_NO.','ETD','ETA',
                            'VENDOR','MODEL','ASSET_NO.','V_ASSET_NO.','NSN','S/N',
                            'CONFIG','CONFIG_DESCRIPTION','SUB_CONFIG',
                            'CPU','MEM','NIC','RAID','DISK','GPU',
                            'BMC_MAC','BASEBOARD','BIOS','OTHER',
                            'UPDATETIME','ACTUAL SHIPPING ADRESS','RECEIVER',
                            'LINKMAN','TELERPHONE','RDR_REASON']

            for col in range(len(columns)):
                ws.write(row_num,col, columns[col],font_style)


                            
            Git = apps.get_model('git', 'Git')
            if 'po_no' in data:
                po_list = Git.objects.filter(po_no=data.get('po_no')).values_list('status',
                                                                                    'shipment',
                                                                                    'deliver_date',
                                                                                    'dest',
                                                                                    'tracking_no',
                                                                                    'tracking_company',
                                                                                    'po_no',
                                                                                    'etd',
                                                                                    'eta',
                                                                                    'vendor',
                                                                                    'model',
                                                                                    'asset_no_id',
                                                                                    'v_asset_no',
                                                                                    'nsn',
                                                                                    'serialnumber',
                                                                                    'config',
                                                                                    'config_description',
                                                                                    'sub_config',
                                                                                    'cpu',
                                                                                    'mem',
                                                                                    'nic',
                                                                                    'raid',
                                                                                    'disk',
                                                                                    'gpu',
                                                                                    'bmc_mac',
                                                                                    'baseboard',
                                                                                    'bios',
                                                                                    'other',
                                                                                    'updatetime',
                                                                                    'actual_shipping_address',
                                                                                    'receiver',
                                                                                    'linkman',
                                                                                    'telephone',
                                                                                    'rdr_reason'
                                                                                ).order_by('asset_no_id')

                if po_list:
                    for po in po_list:
                        row_num += 1
                        
                        po = list(po)
                       
                        for col in range(len(po)):
                            if po[col]:
                                po[col] = str(po[col])
                            
                            ws.write(row_num, col, po[col], font_style)




                    table = "GIT"
   
                    eta = po_list[0][8]
                    po = po_list[0][6]

                    file_name_data = [table, eta, po]

                    if file_name_data[1]:
                        file_name_data[1] = file_name_data[1].date() 

                    for e in file_name_data:
                        if e == None or e == '':
                            e = 'NO'



                    file_name = str(file_name_data[0]) + " " + str(file_name_data[1]) + " " + str(file_name_data[2])

                    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(file_name)
                    wb.save(response)
                else:
                    return redirect('git:git-upload')
        elif 'config' in data:

            response = HttpResponse(content_type='application/ms-excel')
            

            

            wb = xlwt.Workbook(encoding='utf-8')
            ws =wb.add_sheet('OutFactoryTable')
            row_num = 0

            font_style = xlwt.XFStyle()
            
            columns = ['Application','Brand','ProductName',
                            'Assettag','sn','CPU',
                            'mem','nic','raid','disk',
                            'gpu','bmc','baseboard','bios','casesn',
                            'others']
                            
            Config = apps.get_model('git', 'Config')
            Git = apps.get_model('git', 'Git')

            for col in range(len(columns)):
                ws.write(row_num,col, columns[col],font_style)


            if 'po_no' in data:
                po_list = Git.objects.filter(po_no=data.get('po_no'))
                sn_list = []


                # git sn to query config table
                for po in po_list:
                    if po.serialnumber not in sn_list and po.serialnumber:

                        sn_list.append(po.serialnumber)



                config_list = Config.objects.filter(serialnumber__in=sn_list).values_list('application',
                                                                                    'brand',
                                                                                    'product_name',
                                                                                    'assettag_id',
                                                                                    'serialnumber',
                                                                                    'cpu',
                                                                                    'mem',
                                                                                    'nic',
                                                                                    'raid',
                                                                                    'disk',
                                                                                    'gpu',
                                                                                    'bmc',
                                                                                    'baseboard',
                                                                                    'bios',
                                                                                    'casesn',
                                                                                    'others',
                                                                                ).order_by('assettag_id')

                # write to csv
                if config_list:
                    for config in config_list:
                        row_num += 1
                        
                        config = list(config)
                       
                        for col in range(len(config)):
                            if config[col]:
                                config[col] = str(config[col])

                            ws.write(row_num, col, config[col], font_style)

                    company = "Foxconn"
                    eta = po_list.first().eta
                    data_center = po_list.first().dest
                    quantity = str(len(po_list)) + "PCS"
                    configuration = config_list[0][0]

                    if eta == None:
                        eta = ""

                    if data_center == None:
                        data_center = ""

                    if configuration == None:
                        configuration = ""

                    file_name = company + " " + eta + " " + data_center + " " + quantity + " " + configuration

                    response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(file_name)
                    wb.save(response)
                else:
                    return redirect('git:git-upload')
    else:
        return redirect('git:git-upload')
    return response

def fix_git(request):
    Git = apps.get_model('git','Git')

    git_list = Git.objects.all()
    init_chars = 'USW0'

    

    for git_obj in git_list:
        
        if git_obj.serialnumber == '' or git_obj.serialnumber == None:

            asset_tag = git_obj.asset_no_id
            asset_tag_list = asset_tag.split("-")
            unformated_date = asset_tag_list[0]


            
            date_obj = date(int(unformated_date[0:4]), int(unformated_date[4:6]),int(unformated_date[6:]))

            date_obj = date_obj.isocalendar()

            week = date_obj[1]
            if week < 10:
                week = '0' + str(week)

            unformated_sn = asset_tag_list[3]
            unformated_sn = unformated_sn[1:]

            formatted_sn = init_chars + str(week) + str(unformated_sn)

            git_obj.serialnumber = formatted_sn
            git_obj.nsn = formatted_sn
            git_obj.save()
        else:
            print("sn: ",git_obj.serialnumber )

    return redirect('git:git-upload')