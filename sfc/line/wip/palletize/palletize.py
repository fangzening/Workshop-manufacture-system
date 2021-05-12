from django.shortcuts import render, redirect
from django.apps import apps
from ..helper.check_station import check_station
from ..helper.change_station import change_station
from ..helper.check_route import check_route
from ..helper.serialnumber_scan import serialnumber_scan
from ..helper.create_log import create_log


# Station = apps.get_model('line', 'Station')
# Pack = apps.get_model('line', 'Pack')
# PackSerialNumbers = apps.get_model('line','PackSerialNumber')
# PalletPacks = apps.get_model('line', 'PalletPacks')
# Pallet = apps.get_model('line', 'Pallet')
# PackConfiguration = apps.get_model('line', 'PackConfiguration')
# PalletConfiguration = apps.get_model('line', 'PalletConfiguration')

def palletize(request):
    data = request.POST

#     template = data.get('template')
#     route_id = data.get('route')
#     station_id = data.get('station')
#     model = data.get('model')
#     pallet_list = []
#     pallet_id = None
#     current_qty = None
#     target_qty = None
#     result = 'FAIL'
#     message = 'FAIL'

#     # model imports
    

#     # pass station name to template
#     station_ref = Station.objects.filter(pk=station_id)
#     station_ref = station_ref.first()

#     sn_ref = serialnumber_scan(request)

#     if sn_ref:
#         if check_station(request) and check_route(request):

#             # get wo ref
#             workorder = sn_ref.workorder

#             pack_ref = PackSerialNumbers.objects.filter(serialnumber=sn_ref)
#             # create pack if sn doensn't have one
#             if pack_ref:
#                 pack_ref = pack_ref.first()
#             else:
                
#                 pack_config = lookup_pack_config(workorder)
#                 pack = Pack.objects.create(pack_type='single', pack_config=pack_config)

#                 pack_ref = PackSerialNumbers(pack=pack, serialnumber=sn_ref)
#                 pack_ref.clean()
#                 pack_ref.save()


#             #grab pack reference from pack sn model
#             pack_ref = pack_ref.pack

#             on_pallet = PalletPacks.objects.filter(pack=pack_ref)
#             # check if pack is on pallet
#             if on_pallet:
#                 on_pallet = on_pallet.first()
#                 pallet_id = on_pallet.pallet
#                 message = str(sn_ref.serial_number) + ' is on the pallet ' + str(on_pallet.pallet)
#             else:
#                 #check pallet availability
#                 open_pallet = Pallet.objects.filter(status='open')

#                 if open_pallet:
#                     open_pallet = open_pallet.first()
                    
#                 else:
#                    open_pallet = Pallet.objects.create(weight_unit='lbs',status='open')

#                 pallet_config = lookup_pallet_config(workorder)
#                 PalletPacks.objects.create(pallet=open_pallet, pack=pack_ref, pallet_config=pallet_config)
#                 message = str(sn_ref.serial_number) + ' was add to the pallet ' + str(open_pallet)

            

#     context = {

#         'template': template,
#         'route_id': route_id,
#         'station_id': station_id,
#         'model': model,
#         'station_name': station_ref,
#         'result': result,
#         'message' : message,
#         'pallet_id' : pallet_id,
#         'pallet_list' : pallet_list,
#         'current_qty' : current_qty,
#         'target_qty' : target_qty
#     }
#     return render(request, template_name, context)


# def lookup_pack_config(workorder):
#     wo_type = workorder.workorder_type
    

#     # packconfig_ref = PackConfiguration.objects.filter(workorder_type=wo_type)

#     if packconfig_ref:
#         packconfig_ref = packconfig_ref.first() 
#     else:
#         # packconfig_ref = PackConfiguration.objects.filter(workorder_type='default')

#         if packconfig_ref:
#             return packconfig_ref.first()
#         else:
#             # packconfig_ref = PackConfiguration.objects.create(  workorder_type='default',
#                                                                 # country_kit=0,
#                                                                 # print_label=0
#                                                             # )
#             # packconfig_ref.save()
#             # return packconfig_ref
#             return None

# def lookup_pallet_config(workorder):
#     wo_type = workorder.workorder_type

    

#     palletconfig_ref = PalletConfiguration.objects.filter(workorder_type=wo_type)

    

#     if palletconfig_ref:
#         palletconfig_ref = palletconfig_ref.first() 
#         return palletconfig_ref
#     else:
#         palletconfig_ref = PalletConfiguration.objects.filter(workorder_type='default')

#         if palletconfig_ref:
#             return palletconfig_ref.first()
#         else:
#             palletconfig_ref = PalletConfiguration.objects.create(  workorder_type='default',
#                                                                 pallet_mix=0,
#                                                                 pack_limit=8
#                                                             )
#             palletconfig_ref.save()
#             return palletconfig_ref

# def get_view_data(open_pallet, pallet_list, current_qty):
#     packss = PalletPacks.objects.filter(pallet=open_pallet)
    
#     # gather sn's for pallet list
#     for pack in packss:
#         pack = pack.pack
#         serial_numbers = PackSerialNumbers.objects.filter(pack=pack)
#         print(serial_numbers)
#         for serial_number in serial_numbers:
#             pallet_list.append(serial_number.serialnumber)
    
#     pallet_id = open_pallet.pk
    
    
    
