from django.shortcuts import render, redirect
from django.apps import apps
from ..helper.check_station import check_station
from ..helper.change_station import change_station
from ..helper.check_route import check_route
from ..helper.serialnumber_scan import serialnumber_scan
from ..helper.create_log import create_log

Station = apps.get_model('line', 'Station')
Pack = apps.get_model('line', 'Pack')
PackSerialNumbers = apps.get_model('line','PackSerialNumber')

def pack(request):
    data = request.POST

    template = data.get('template')
    route_id = data.get('route')
    station_id = data.get('station')
    pack_id = int(data.get('pack_id') or -1)
    model = data.get('model')
    result = 'FAIL'
    message = 'FAIL'
    # submit sn and pack

    station_ref = Station.objects.filter(pk=station_id)
    station_ref = station_ref.first()

    # ref to sn
    sn_ref = serialnumber_scan(request)

    template_name = 'production/pack.html'
    # check if sn exists
    if sn_ref:
        # check place of sn
        if check_station(request) and check_route(request):
            # check if ssn has a pack already
            if not PackSerialNumbers.objects.filter(serialnumber=sn_ref):
                # check if pack id was actually passed and check if its full
                workorder = sn_ref.workorder
                if pack_id == -1 or check_capacity(request):
                    pack_id = create_pack(workorder)

                # get pack ref
                pack_ref = Pack.objects.filter(pk=pack_id)
                pack_ref = pack_ref.first()

                sn_type = workorder.workorder_type
                pack_type = pack_ref.pack_config.workorder_type

                # compare wo order types between pack/sn
                if sn_type != pack_type:
                    pack_id = create_pack(workorder)

                add_to_pack = PackSerialNumbers(pack=pack_ref, serialnumber=sn_ref)
                add_to_pack.clean()
                add_to_pack.save()

                create_log(request)
                change_station(request)
                result = "success"
                message = str(sn_ref.serial_number) + ' was added to pack ' + str(pack_id)
            else:
                current_pack = PackSerialNumbers.objects.filter(serialnumber=sn_ref)
                current_pack = current_pack.first()
                message = str(sn_ref.serial_number) + ' has the pack ' + str(current_pack.pk) + ' already'

        else:
            message = 'This Serial Number Is Not At This Station'
    else:
        message = 'Serial Number Was Not Found'

    context = {
        'template': template,
        'route_id': route_id,
        'station_id': station_id,
        'model': model,
        'station_name': station_ref.pk,
        'result': result,
        'message': message,
        'pack_id': pack_id
    }

    return render(request, template_name, context)


# check capacity of pack
def check_capacity(request):
    PackSerialNumbers = apps.get_model('line', 'PackSerialNumbers')
    Pack = apps.get_model('line', 'Pack')

    data = request.POST
    pack_id = int(data.get('pack_id') or -1)

    pack_ref = Pack.objects.filter(id=pack_id)
    pack_ref = pack_ref.first()

    items = PackSerialNumbers.objects.filter(pack=pack_ref)

    current_capacity = len(items)

    sn_ref = serialnumber_scan(request)

    pack_capacity = sn_ref.workorder.pack_count

    if current_capacity == pack_capacity:
        return True
    else:
        return False


def lookup_config(workorder):
    wo_type = workorder.workorder_type


    PackConfiguration = apps.get_model('line', 'PackConfiguration')

    packconfig_ref = PackConfiguration.objects.filter(workorder_type=wo_type)

    if packconfig_ref:
        packconfig_ref = packconfig_ref.first()
    else:
        packconfig_ref = PackConfiguration.objects.filter(workorder_type='default')

        if packconfig_ref:
            return packconfig_ref.first()
        else:
            packconfig_ref = PackConfiguration.objects.create(workorder_type='default',
                                                              country_kit=0,
                                                              print_label=0
                                                              )
            packconfig_ref.save()
            return packconfig_ref


def create_pack(workorder):
    pack_config = lookup_config(workorder=workorder)
    if workorder.pack_count > 1:

        create_pack = Pack.objects.create(pack_type='multi', pack_config=pack_config)
    else:
        create_pack = Pack.objects.create(pack_config=pack_config)

    return create_pack.pk