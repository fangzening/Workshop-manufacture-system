import os
import sys

from django.db import connection
from django.shortcuts import render

from .forms import OfflineStationForm
from api.keypart.check_mask import *

from maskconfig.models import Mask
from django.apps import apps


def __errorMessageHandling(message):
    if message == "IntegrityError":
        res = "Values already exist in databse!"
    else:
        res = "Unable to handle this error!"
    return res


def phantom_data_input(request):
    if request.method == "POST":
        errorMessage = ""

        cpuMaskCheckFlag = False
        cpuSNDataCheck = {}
        cpu_serial_number = request.POST["Cpu_SN"] #cpu serial number
        cpu_part_number = request.POST["Cpu_PN"] #cpu part number
        cpuSNDataCheck["PartSN"] = cpu_serial_number
        cpuMaskCheck = ""

        # if a part number is given, then need to check if a mask exist, and check if input pass the mask. If a mask does not 
        # exist, then take what ever user input. 
        if cpu_part_number != "": 
            cpuSNDataCheck["PartNo"] = cpu_part_number
            cpuSNDataCheck["mask"] = None

            MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')
            material_ref = MaterialMaster.objects.filter(model_id=cpuSNDataCheck["PartNo"])
            

            cpuMaskFound = Mask.objects.filter(model=cpuSNDataCheck["PartNo"])
            if len(cpuMaskFound) != 0: # mask exist
                cpuSNDataCheck["mask"] = cpuMaskFound[0]
                cpuMaskCheck = check_mask(cpuSNDataCheck)
                if cpuMaskCheck == "Success":
                    cpuMaskCheckFlag = True
                else:
                 
                    cpuMaskCheckFlag = False
            elif material_ref:
                cpuMaskCheck = "Success"
                cpuMaskCheckFlag = True
            else: # mask does not exist
                cpuMaskCheck = "Fail"
                cpuMaskCheckFlag = False
        # if a part number was not given by user, then program need to check every mask vs. serial number. if none of them match, then need 
        # to maintain a mask.
        else:
            mask_refs = Mask.objects.all()
            for mask_ref in mask_refs:
                cpuSNDataCheck["mask"] = mask_ref
                cpuMaskCheck = check_mask(cpuSNDataCheck)
                if cpuMaskCheck == "Success" and mask_ref.model_id == '110113G00-187-G':
                    CpuPN = mask_ref.model_id
                    cpu_part_number = mask_ref.model_id
                    cpuMaskCheckFlag = True
                    break
                else:
                    
                    cpuMaskCheckFlag = False

        if cpuMaskCheck != "Success":
            errorMessage += "CPU Serial Number: " + cpuMaskCheck + "<br \>"

        hsnDataCheck = {}
        heatsink_serial_number = request.POST["H_SN"]  #heatsink serial number
        heatsink_part_number = request.POST["H_PN"]  #heatsink part number

        hMaskCheckFlag = False
        hsnMaskCheck = ""
        hsnDataCheck["PartSN"] = heatsink_serial_number
        if heatsink_part_number != "":
            hsnDataCheck["PartNO"] = heatsink_part_number
            hsnDataCheck["mask"] = None

            material_ref = MaterialMaster.objects.filter(model_id=hsnDataCheck["PartNO"])


            hsnMaskFound = Mask.objects.filter(model = heatsink_part_number)
            if hsnMaskFound:
                hsnDataCheck["mask"] = hsnMaskFound[0]
                hsnMaskCheck = check_mask(hsnDataCheck)
                if hsnMaskCheck == "Success":
                    hMaskCheckFlag = True
                else:
                    hMaskCheckFlag = False

                
                
            elif material_ref:
                hsnMaskCheck = "Success"
                hMaskCheckFlag = True
                
            else:
                hsnMaskCheck = "Fail"
                hMaskCheckFlag = False
                
        else:
            h_mask_refs = Mask.objects.all()
            for h_mask_ref in h_mask_refs:
                hsnDataCheck["mask"] = h_mask_ref
                hsnMaskCheck = check_mask(hsnDataCheck)
                if hsnMaskCheck == "Success" and (h_mask_ref.model_id == '110113G00-000' or h_mask_ref.model_id == '480126F00-553-G'):
                    HPN = h_mask_ref.model_id
                    heatsink_part_number = h_mask_ref.model_id
                    hMaskCheckFlag = True
                    break
                else:
                    
                    hMaskCheckFlag = False

        if hsnMaskCheck != "Success":
            errorMessage += "Heat Sink serial number: " + hsnMaskCheck

        if cpuMaskCheckFlag == True and hMaskCheckFlag == True:
            errorMessage += "Success"
            user = request.user
            cursor = connection.cursor()
            query = "call Insert_Test(" + "'" + str(cpu_serial_number) + "'" + ", " + "'" + str(cpu_part_number) + "'" + ", " + "'" + str(
                heatsink_serial_number) + "'" + ", " + "'" + str(heatsink_part_number) + "'" + "," + "'" + str(user) + "'" + ")"
            try:
                cursor.execute(query, [cpu_serial_number, cpu_part_number, heatsink_serial_number, heatsink_part_number])
            except Exception as e:
                errorMessage = __errorMessageHandling(e.__class__.__name__)
        else:
            if errorMessage == '':
                errorMessage += "Fail"
        context = {
            'error': errorMessage,
            'form': OfflineStationForm()
        }

        return render(request, 'offline_station/p_part_input.html', context)
    else:
        return render(request, 'offline_station/p_part_input.html')

