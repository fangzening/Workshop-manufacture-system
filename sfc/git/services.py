# upload
from pandas import pandas as reader
from django.apps import apps
import math
from datetime import datetime

'''
    class: GitService

    desc:
        Advanced services exposed for the Git model.

    ex:
        git_service = GitService()
        response = git_service.upload(excel_file)
'''
class GitService():

    def __init__(self):
        self.Git = apps.get_model("git", "Git")
        self.Config = apps.get_model('git','Config')

    '''
        func: upload excel file to git table

        params:
            _excel_file - file uploaded by user

        return:
            boolean - if uploaded or not uploaded

    '''
    def upload(self,_excel_file):

        def validate(_sorted_data):
            if len(_sorted_data) < 0:
                return False
            else:
                po_list = []
                asset_id_list = []
                for git_obj in _sorted_data:
                    po_list.append(git_obj.po_no)
                    asset_id_list.append(git_obj.asset_no_id)

                # check if duplicates in list
                if len(asset_id_list) != len(set(asset_id_list)):
                    return False


            po_check = self.Git.objects.filter(po_no__in=po_list)
            asset_id_check = self.Git.objects.filter(asset_no_id__in=asset_id_list)




            if po_check and asset_id_check:
                return False
            else:

                return True
             
        # extract data from file
        _excel_data = None
        try:
            _excel_data = reader.read_excel(_excel_file)
        except IOError as e:
            
            return e
        Git = apps.get_model("git", "Git")


        # get excel file headers
        column_headers = list(_excel_data.columns.values)
        
        _sorted_data = []

        for column, row in _excel_data.iterrows():
            
            temp = list(row)
            filtered_data = []

            for element in temp:
            
                
                if isinstance(element,float) and math.isnan(element):
                    
                    element = None
                    
                filtered_data.append(element)    

            temp = filtered_data
            
            
            # create git model per excel row
            _git_instance = self.Git(
                                asset_no_id = temp[column_headers.index('ASSET_NO.')],
                                status = temp[column_headers.index('STATUS')],
                                shipment = temp[column_headers.index('SHIPMENT')],
                                deliver_date = temp[column_headers.index('DELIVER DATE')],
                                dest = temp[column_headers.index('DEST')],
                                tracking_no = temp[column_headers.index('TRACKING_NO.')],
                                tracking_company = temp[column_headers.index('TRACKING_COMPANY')],
                                po_no = temp[column_headers.index('PO_NO.')],
                                etd = temp[column_headers.index('ETD')],
                                eta = temp[column_headers.index('ETA')],
                                vendor = temp[column_headers.index('VENDOR')],
                                model = temp[column_headers.index('MODEL')],
                                v_asset_no = temp[column_headers.index('V_ASSET_NO.')],
                                nsn = temp[column_headers.index('NSN')],
                                serialnumber = temp[column_headers.index('S/N')],
                                config = temp[column_headers.index('CONFIG')],
                                config_description = temp[column_headers.index('CONFIG_DESCRIPTION')],
                                sub_config = temp[column_headers.index('SUB_CONFIG')],
                                cpu = temp[column_headers.index('CPU')],
                                mem = temp[column_headers.index('MEM')],
                                nic = temp[column_headers.index('NIC')],
                                raid = temp[column_headers.index('RAID')],
                                disk = temp[column_headers.index('DISK')],
                                gpu = temp[column_headers.index('GPU')],
                                bmc_mac = temp[column_headers.index('BMC_MAC')],
                                baseboard = temp[column_headers.index('BASEBOARD')],
                                bios = temp[column_headers.index('BIOS')],
                                other = temp[column_headers.index('OTHER')],
                                # updatetime = temp[column_headers.index('UPDATETIME')],
                                # actual_shipping_address = temp[column_headers.index('ACTUAL SHIPPING ADRESS')],
                                # receiver = temp[column_headers.index('RECEIVER')],
                                linkman = temp[column_headers.index('LINKMAN')],
                                telephone = temp[column_headers.index('TELERPHONE')],
                                # rdr_reason = temp[column_headers.index('RDR_REASON')],
            )

            _sorted_data.append(_git_instance)
            
        # validate/insert into DB
        if validate(_sorted_data):
            Git.objects.bulk_create(_sorted_data)
        else:
            
            return False
        

        return True

    def test(self):
        self.create_user(email=1)


    def create_user(self,*, email: str):
        pass

    '''
        func: lookup asset tag in git table for provided SN
        params:
            serialnumber - internal serial number from SerialNumber Model

        return:
            PayLoad Object
    '''
    def get_asset_tag(self, _serialnumber):
        # check if sn has asset tag
        _check_sn = self.Git.objects.filter(serialnumber=_serialnumber)

        _payload = PayLoad(0,"Unknown Error")

        

        if _check_sn:
            _payload.status = 405
            _payload.message = "Serial Number has Asset Tag"
            return _payload
        
        # look up serial number
        SerialNumber = apps.get_model('manufacturing','SerialNumber')

        print(_serialnumber)

        _serial_number_ref = SerialNumber.objects.filter(serial_number=_serialnumber)
        print('_serial_number_ref',_serial_number_ref)

        # RETURN POINT
        if not _serial_number_ref:
            _payload.status = 406
            _payload.message = "Serial Number Doesn't Exist"
            return _payload

        else:
            # get part numbers for git table lookup
            _serial_number_ref = _serial_number_ref.first()
            _customer_pn = ""
            try:
                _customer_pn = _serial_number_ref.model_id.alternative_pn
            
            # RETURN POINT
            except Exception as e:
                _payload.message = e
                return _payload

            # get earliest availabe asset tag
            _git_queryset = self.Git.objects.filter(sub_config=_customer_pn,serialnumber=None) #.order_by("deliver_date")
            
            if len(_git_queryset) > 0:
                _git_obj = _git_queryset.first()
                _git_obj.serialnumber = _serial_number_ref.serial_number
                _git_obj.nsn = _serial_number_ref.serial_number
                _git_obj.save()
                _payload.status = 200
                _payload.message = _git_obj.asset_no_id 
                return _payload
            else:
                _payload.status = 407
                _payload.message = "No Asset Tag Available for {}".format(_serialnumber)
                return _payload

    '''
    update etd/eta/tracking no and company
    
    
    '''

    def update(self, data):
        _payload = PayLoad(200,"Success")
        try:    
            po = data['po']
            eta = data['eta']
            etd = data['etd']
            tracking_no = data['tracking_no']
            tracking_company = data['tracking_company']
        except Exception as e:
            print("error: ",e)
            _payload.status = 405
            _payload.message = 'Missing Data'
            return _payload

        try:

            self.Git.objects.filter(po_no=po).update(eta=eta,
                                                    etd=etd,
                                                    tracking_no=tracking_no,
                                                    tracking_company=tracking_company
                                                    )
        except Exception as e:
            print("error: ",e)
            _payload.status = 405
            _payload.message = 'Missing Data'
            return _payload

        return _payload
    
    def get_git(self, _serialnumber):
        _payload = PayLoad(0,"Unknown Error")

        # look up serial number
        SerialNumber = apps.get_model('manufacturing','SerialNumber')
        _serial_number_ref = SerialNumber.objects.filter(serial_number=_serialnumber)

        # RETURN POINT
        if not _serial_number_ref:
            print("Can't find SN")
            _payload.status = 406
            _payload.message = "Serial Number Doesn't Exist"
            return _payload
        else:

            # get part numbers for git table lookup
            _serial_number_ref = _serial_number_ref.first()
            _customer_pn = ""
            try:
                _customer_pn = _serial_number_ref.model_id.alternative_pn
                

            
            # RETURN POINT
            except Exception as e:
                _payload.message = e
                return _payload

            _git_queryset = self.Git.objects.filter(sub_config=_customer_pn,serialnumber=_serialnumber)
            print('_git_queryset', _git_queryset)

            if _git_queryset:
                _git = _git_queryset.first()
                _payload.status = 200
                _payload.message = _git

        return _payload

'''
    class: ConfigService

    desc:
        Advanced services exposed for the Git model.

    ex:
        config_service = ConfigService()
        response = config_service.mac_parser(sn)
'''
class ConfigService():

    def __init__(self):
        self.Git = apps.get_model("git", "Git")
        self.Config = apps.get_model('git','Config')

    def mac_parser(self,serial_number):
        _payload = PayLoad(500,"Fail")
        try:
            config_ref = self.Config.objects.get(serialnumber=serial_number)
        except Exception as e:
            _payload.status = 401
            _payload.message = "Serial Number Doesn't Exist"
            print("error: ", e)
            return _payload

        if config_ref:
            mac_string = config_ref.nic
            mac_length = 17
            mac_list = []

            count = mac_string.count("s/")
            index = 0
            offset = 3
            mac_length = 17


            while count > 0:
                start = mac_string.find("/s",index)

                if start > 0:
                    start = start + offset
                    end = start + mac_length
                    temp_mac = mac_string[start:end]

                    _mac = ""
                    for char in temp_mac:
                        if char.isalpha():
                            char = char.upper()
                        
                        _mac += char
                    mac_list.append(_mac)
                    index = start
                
                count -= 1

            ipmi_string = [config_ref.ipmi]

            _ipmi = ""
            if ipmi_string[0] and ipmi_string[0] != None:
                count = 0
                for char in ipmi_string[0]:
                    if char != None and char.isalpha():
                        char = char.upper()

                    if count % 2 == 0 and count != 0:
                        _ipmi += ":" + str(char)
                    else:
                        _ipmi += char

                    count += 1

            ipmi = [_ipmi]

            bmc = [config_ref.bmc]

            if bmc:
                if len(bmc[0]) > 0 and "/" in bmc[0]:
                    bmc_list = bmc[0].split("/")
                    _bmc = bmc_list[1]
                    _bmc = str(_bmc)

                    bmc = [_bmc]



            data = {
                "ipmi" : ipmi,
                "ncsi" : bmc,
                "mac_addresses" : mac_list
            }
            if len(mac_list) > 0:
                _payload.status = 200
                _payload.message = data

        return _payload
            

'''
    class: PayLoad

    desc:
        Object for passing data(status, message)

    ex:
        _payload = PayLoad(200,"Success")
        _payload.message = "Failed"
'''

class PayLoad():
    def __init__(self,_status,_message):
        self.status = _status
        self.message = _message

    def get_data(self):
        return {
                'status':self.status,
                'message' : self.message
                }
            



    
    
    
