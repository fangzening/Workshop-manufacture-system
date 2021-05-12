from django.http import *
from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from maskconfig.models import *
from line.models import *
from .models import *
from manufacturing.models import *
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View, generic
from django.apps import apps
from django.utils import timezone as tz

from .forms import AddSerialNumberForm, PalletQty
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
import random
import string
from datetime import datetime

from django.http import JsonResponse
from shipping.models import *
from django.db import connection
from collections import namedtuple
import json
import collections

import pdb
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist



######################## end api ###############################################

# Create your views here.

class PalletStationDetailView(LoginRequiredMixin, generic.ListView):
    Pallet = apps.get_model('shipping', 'Pallet')

    # permission_required = 'manufacturing.can_repair'
    model = Pallet
    context_object_name = 'pallet_list'
    template_name = 'production/palletize/palletize.html'
    fields = '__all__'

    # def sn_not_in_pallet(request):
    #     SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
    #     serial_number = self.POST['serialnumber']
    #     context = {(
    #     sn_not_in_list = SerialNumber.objects.filter(serial_number__iexact=serial_number,
    #                                                   palletserialnumber__isnull=True)
    #     )}
    #     return render(request, template_name, context)

    def get_queryset(self):
        query = self.request.GET.get('pallet_id')
        if query:
            return Pallet.objects.filter(
                Q(pallet_id__iexact=query)
            )
        else:
            return Pallet.objects.all().order_by('pallet_id')

    def get_context_data(self, **kwargs):

        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        # serial_number = self.POST['serialnumber']
        # sn_not_in_list = SerialNumber.objects.filter(palletserialnumber__isnull=True)
        context = super(PalletStationDetailView, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'palletsn_list': PalletSerialNumber.objects.order_by('create_date'),
            'more_context': PalletSerialNumber.objects.all(),
            'serialnumber_list': SerialNumber.objects.order_by('generated_date'),
            'sn_context': SerialNumber.objects.all(),
            'snnot_list': SerialNumber.objects.filter(palletserialnumber__isnull=True),
            # 'snnot_context': SerialNumber.objects.filter(palletserialnumber__isnull=True),
            #'sn_not_in_list' : sn_not_in_list,
            #'sn_not_in_list'= SerialNumber.objects.filter(serial_number__iexact=serial_number, palletserialnumber__isnull=True ),
        })


        return context


class PalletDetail(LoginRequiredMixin, generic.DetailView):
    model = Pallet
    template_name = 'production/palletize/palletize_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        context = super(PalletDetail, self).get_context_data(**kwargs)
        # inner_qs = PalletSerialNumber.objects.all()
        # sns = SerialNumber.objects.exclude(serial_number__in=inner_qs)
        # exclude = []
        # for sn in sns:
        #     exclude.append(sn)
        # print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'palletsn_list': PalletSerialNumber.objects.order_by('row_id'),
            'pallet_list': Pallet.objects.order_by('create_date'),
            'serialnumber_list': SerialNumber.objects.order_by('generated_date'),
            'more_context': PalletSerialNumber.objects.all(),
            'pallet_context': Pallet.objects.all(),
            'sn_context': SerialNumber.objects.all(),
             'snnot_list': SerialNumber.objects.filter(palletserialnumber__isnull=True),
            #'snnot_context': SerialNumber.objects.all(),
            #'snnot_list': SerialNumber.objects.exclude(serial_number__in=inner_qs).order_by('generated_date'),
            #'exclude': exclude,
        })
        return context


@login_required
def add_sn_view(request):
    print('h4')
    if request.method == 'POST':
        # template_name = 'production/palletize/palletize_detail.html'
        print('h3')
        form = AddSerialNumberForm(request.POST)
        if form.is_valid():
            print('h2')

            form.save()
            # return redirect(reverse('shipping:pallet_detail')  + str(get_pallet_id(request)))
            pallet_id = request.POST.get('pallet_id')
            serial_number = request.POST.get('serial_number')
            add_sn = authenticate(
                request,
                pallet_id=pallet_id,
                serial_number=serial_number
            )
            login(request, add_sn)
            # return redirect(reverse('shipping:pallet_station'))
            return HttpResponse('hi')



        else:

            return redirect(reverse('shipping:pallet_station'))
        return redirect(reverse('shipping:pallet_station'))

# ############################# test modal #########################
@transaction.atomic
@login_required
def create_new_pallet(request):
    pallet_id = request.POST['pallet_id']

    def post(request):
        pallet_id = request.POST['pallet_id']
        messages.success(request, 'Create ' + pallet_id + ' Pallet ID successfully.')


        # return redirect(reverse('shipping:pallet_station'))
        return HttpResponseRedirect(result + '/')
        # return redirect(reverse('shipping:save_dimension'))

    if request.method == 'POST':
        pallet_id = request.POST['pallet_id']

        updater = request.POST['updater']
        creator = request.POST['creator']
        last_pallet_id = request.POST['last_pallet_id']
        # model= request.POST['model']
        result = ''
        sub_result = ''
        cursor = connection.cursor()
        query = '''CALL serialization_get_next_value (%s, %s, %s)'''
        sp_result = cursor.execute(query, ['PAL', '0', ''])
        rows = cursor.fetchall()
        for row in rows:
            result = row[0]
            print(result)
            sub_result = result[0:3]
            print(sub_result)
        if sub_result == '99-':
            # return JsonResponse({"error": result}, safe=False, status=200)
            return messages.error(request, result)
        # pallet = result
        # letters = string.ascii_lowercase
        # numbers = string.digits
        # randoms = 'pallet'.join(random.choice(letters) for i in range(10)).join(
        #     random.choice(numbers) for i in range(10))
        # randoms = randoms[0:10]
        # print (''.join(random.choice(letters) for i in range(10)).join(random.choice(numbers) for i in range(10)))
        # print (randoms)
        # count_row = PalletSerialNumber.objects.filter(pallet_id=pallet_id).count()

        pallet = Pallet(
            # model=model,
            current_qty=0,
            pallet_id=result,
            status=1,
            creator=creator,
            # full_date=datetime.now(),
            create_date=datetime.now(),
            full=0,
            updater=updater,
        )

        # pallet.save()
        print("Generating BOL")
        if Pallet.objects.filter(pallet_id=result).exists():
            messages.error(request, 'The pallet ID already exists. Please try again')
            return HttpResponseRedirect(result + '/')

        else:
            pallet.save()

        return post(request)

    return HttpResponseRedirect(pallet_id + '/')

# ############### store procedure ###############
@login_required
def create_pallet_id (request):
    pallet = ''
    pallet_id = request.POST['pallet_id']

    def post(request):
        pallet_id = request.POST['pallet_id']
        messages.success(request, 'Create ' + pallet_id + ' Pallet ID successfully.')
        print("Generating PALLET")
        cursor = connection.cursor()
        query = '''CALL serialization_get_next_value (%s, %s, %s)'''
        sp_result = cursor.execute(query, ['PAL', '0', ''])
        rows = cursor.fetchall()
        for row in rows:
            result = row[0]
            print(result)
            sub_result = result[0:3]
            print(sub_result)
        if sub_result == '99-':
            # return JsonResponse({"error": result}, safe=False, status=200)
            return messages.error(request, 'The pallet ID already exists. Please try again')
        pallet = result
        return HttpResponseRedirect(pallet_id + '/')

        print(pallet)

    if request.method == 'POST':
        pallet_id = request.POST['pallet_id']

        updater = request.POST['updater']
        creator = request.POST['creator']


        pallet = Pallet(
            # model=model,
            current_qty=0,
            pallet_id=pallet_id,
            status=1,
            creator=creator,
            # full_date=datetime.now(),
            create_date=datetime.now(),
            full=0,
            updater=updater,
        )

        if Pallet.objects.filter(pallet_id=pallet_id).exists():
            messages.error(request, 'The pallet ID already exists. Please try again')
            return HttpResponseRedirect(pallet_id + '/')

        else:
            pallet.save()

        return post(request)
    return HttpResponseRedirect(pallet_id + '/')
# ############### po validation ###########################################
def pallet_serialnumber_po_validation(prev_sn, cur_sn):
    git_git_object = apps.get_model('git', 'git')
    cur_po_object = git_git_object.objects.filter(serialnumber=cur_sn).values()
    if len(cur_po_object) == 0:
        return (False, cur_sn + ' does not exist in git_git table')
    cur_po = cur_po_object[0]['po_no']
    if cur_po == '':
        return (False, cur_sn + ' does not have a po number')
    prev_po_object = git_git_object.objects.filter(serialnumber=prev_sn).values()
    prev_po = prev_po_object[0]['po_no']
    if prev_po == cur_po:
        return (True, 'PO matched')
    return (False, 'PO does not match')


# ############### for pallet json ##################################
# ###############  validate SN  ####################################
# ############### for pallet json ##################################
# ###############  validate SN  ####################################
@login_required
def validate_sn_json(request):
    data = {}
    if request.method == 'POST':
        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        pallet_id = request.POST['pallet_id']
        serial_number = request.POST['serialnumber']

        cursor = connection.cursor()
        last_sku = request.POST['last_sku']
        first_sku = request.POST['first_sku']
        firs_sku_string = str(first_sku)
        last_sn = request.POST['last_sn']

        cur_sku_object = SerialNumber.objects.filter(serial_number=serial_number).values('model_id')
        cur_status = SerialNumber.objects.filter(serial_number=serial_number).values('sn_status_category')

        print('current sku')
        print(cur_sku_object)
        print(first_sku)
        #scursor.execute("PERFORM * FROM select_data_by_pallet_id( %s); ", (pallet_id,))
        cursor.callproc('palletization_select_data_by_pallet_id', [pallet_id, ])


        sku_qs = cur_sku_object
        for sku in sku_qs:
            if sku['model_id'] == first_sku:
                print('equal')
            else:
                print('different')

            print(sku['model_id'])

        git_git_object = apps.get_model('git', 'git')
        cur_po_object = git_git_object.objects.filter(serialnumber=serial_number)

        sn_completed = SerialNumber.objects.filter(serial_number=serial_number).values('completed','shipped','station_id','model_id')
        completed_list = sn_completed
        for completed in completed_list:
            if completed['completed'] != 1:
                print('not completed')
            elif completed['shipped'] != 0:
                print('its shipped')
            elif completed['station_id'] == 'Repair':
                print('still under repair')
            else:
                print('error')

        sn_shipped = SerialNumber.objects.filter(serial_number=serial_number).values('shipped')
        shipped_list = sn_shipped
        for shipped in shipped_list:
            if shipped['shipped'] != 0:
                print('shipped')
            else:
                print('error')


        last_sku_object = git_git_object.objects.filter(serialnumber=last_sn).values('po_no')
        last_sn_qs = last_sku_object
        for sn in last_sn_qs:
            if sn['po_no']:
                print(sn['po_no'])



        cur_po_no = git_git_object.objects.filter(serialnumber=serial_number).values('po_no')
        po_qs = cur_po_no

        for po in po_qs:
            if po['po_no']:
                print(po['po_no'])
                for sn in last_sn_qs:
                    if sn['po_no'] == po['po_no']:
                        data['stat'] = "po_not_matched";

                        print('equal')
                    else:
                        print('different')
            # else:
            #     print('different')
            #
            # print(sku['model_id'])

        rows = cursor.fetchall()
        pallet_data_list = []
        print(pallet_data_list)
        for row in rows:
            d = collections.OrderedDict()
            d['pallet_id'] = row[0]
            # d['serial_number'] = row[1]

            pallet_data_list.append(d)

        RepairMain = apps.get_model('manufacturing', 'RepairMain')
        repairMainFilter = RepairMain.objects.filter(serial_number=serial_number)

        if not SerialNumber.objects.filter(serial_number=serial_number):
            data['stat'] = "not_exist";
            msg = 'not exist'
            status = "error"
            # messages.error(request, 'SN: "' + serial_number + '" does not exist.')
            json_output = json.dumps({'pallet_table': pallet_data_list})
            return JsonResponse(data, safe=False, status=200)



        elif completed['model_id'] != first_sku:
            data['stat'] = "sku_not_matched";
            return JsonResponse(data, safe=False, status=200)



        elif completed['completed'] != 1:
            data['stat'] = "sn_not_completed";
            return JsonResponse(data, safe=False, status=200)

        elif completed['shipped'] == 1:
            data['stat'] = "is_shipped";
            return JsonResponse(data, safe=False, status=200)



        elif completed['station_id'] == 'Repair':
        # elif len(repairMainFilter) != 0:
            data['stat'] = "in_repair";
            status = "error"
            # messages.error(request, 'SN: "' + serial_number + '" still in Repair station.')
            json_output = json.dumps({'pallet_table': pallet_data_list})
            return JsonResponse(data, safe=False, status=200)


        elif PalletSerialNumber.objects.filter(serialnumber_id=serial_number).exists():
            data['stat'] = "in_use";
            status = "error"
            # messages.error(request, 'SN: "' + serial_number + '" is in Use. Please try again.')
            json_output = json.dumps({'pallet_table': pallet_data_list})
            return JsonResponse(data, safe=False, status=200)

        # elif len(cur_po_object) == 0:
        #     data['stat'] = "po_not_exist";
        #     return JsonResponse(data, safe=False, status=200)

        # elif sn['po_no'] != po['po_no']:
        #     data['stat'] = "po_not_matched";
        #     return JsonResponse(data, safe=False, status=200)

        else:
            data['stat'] = "all_validated";
        json_output = json.dumps({'pallet_table': pallet_data_list})
        return JsonResponse(json_output, safe=False, status=200)


# ############### delete SN ###########################################
@login_required
def delete_sn_json(request):
    if request.method == 'POST':
        serial_number = request.POST['serialnumber']
        pallet_id = request.POST['pallet_id']
        updater = request.POST['updater']
        current_qty = PalletSerialNumber.objects.filter(pallet_id=pallet_id).count()
        current_qty = current_qty - 1
        print(current_qty)
        cursor = connection.cursor()
        print('delete0')

        query3 = '''CALL palletization_delete_sn (%s, %s, %s, %s)'''
        cursor.execute(query3, [pallet_id, serial_number,current_qty, updater])

        rows = cursor.fetchall()
        pallet_data_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['pallet_id'] = row[0]
            d['serial_number'] = row[1]

            pallet_data_list.append(d)
        json_output = json.dumps({'pallet_table': pallet_data_list})
        return JsonResponse(json_output, safe=False, status=200)

    cursor = connection.cursor()
    rows = cursor.fetchall()
    pallet_data_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['pallet_id'] = row[0]
        d['serial_number'] = row[1]

        pallet_data_list.append(d)

    json_output = json.dumps({'pallet_table': pallet_data_list})
    return JsonResponse(json_output, safe=False, status=200)



# ############### add SN ###########################################
@login_required
def add_sn_json(request):
    pallet_id = request.POST.get('pallet_id')
    if request.method == "POST":

        serial_number = request.POST['serialnumber']
        # serial_number_option = request.POST['serial_number_id ']

        # model = request.POST['model']
        pallet_id = request.POST['pallet_id']
        create_date = datetime.now()
        update_date = datetime.now()
        status = request.POST['status']
        current_qty = request.POST['current_qty']
        full = request.POST['full']
        full_date = request.POST['full_date']
        wh_id = request.POST['wh_id']
        height = request.POST['height']
        length = request.POST['length']
        width = request.POST['width']
        weight = request.POST['weight']
        gross_weight = request.POST['gross_weight']
        net_weight = request.POST['net_weight']
        volume_weight = request.POST['volume_weight']
        creator = request.POST['creator']
        creator_pallet = request.POST.get('creator_pallet')
        updater = request.POST['updater']




        cursor = connection.cursor()
        print (cursor)
        print ('h1')


        query3 = '''CALL palletization_add_sn (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query3, [serial_number, pallet_id, creator, create_date, updater, update_date])

        query = '''SELECT a.serial_number, a.model_id from manufacturing_serialnumber a inner join shipping_palletserialnumber b on a.serial_number = b.serial_number where b.pallet_id = (%s)'''
        print(query)
        cursor.execute(query, [pallet_id])
        #cursor.callproc('select_data_by_pallet_id', [pallet_id])
        # query3 = '''SELECT row_id from shipping_palletserialnumber where pallet_id = (%s)'''
        # cursor.execute(query3, [pallet_id])

        print ('h2')

        rows = cursor.fetchall()
        pallet_data_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['serial_number'] = row[0]
            d['sku'] = row[1]

            pallet_data_list.append(d)


        json_output = json.dumps({'pallet_table': pallet_data_list})
        print(json_output)
        print('test1')


        return JsonResponse(json_output, safe=False, status=200)



# ############### for pallet json ##################################
# ############### for pallet json ##################################
# ############### for pallet json ##################################


@login_required
def add_sn_test_view(request):
    def post(request):

        pallet_id = request.POST['pallet_id']
       # messages.success(request, 'Added serial number successfully.')
        return HttpResponseRedirect(pallet_id + '#Pallet-Detail')

    if request.method == 'POST':
        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        serial_number = request.POST['serialnumber']
        sn_query = SerialNumber.objects.filter(serial_number=serial_number)

        git_git_object = apps.get_model('git', 'git')
        cur_po_object = git_git_object.objects.filter(serialnumber=serial_number)

        print (sn_query, len(sn_query))
        if len(sn_query)<0:
            messages.success(request, 'The Serial Number is validated.')

            return HttpResponseRedirect(pallet_id + '#Pallet-Detail')


        # serial_number = request.POST['serial_number_id']


        # serial_number_query = request.GET['serialnumber']
        # serial_number_option = request.POST['serial_number_id ']
        current_qty = request.POST['current_qty']
        # model = request.POST['model']
        pallet_id = request.POST['pallet_id']
        create_date = request.POST['create_date']
        status = request.POST['status']
        # current_qty = request.POST['current_qty']
        full = request.POST['full']
        full_date = request.POST['full_date']
        wh_id = request.POST['wh_id']
        height = request.POST['height']
        length = request.POST['length']
        width = request.POST['width']
        weight = request.POST['weight']
        gross_weight = request.POST['gross_weight']
        net_weight = request.POST['net_weight']
        volume_weight = request.POST['volume_weight']
        creator = request.POST['creator']
        creator_pallet = request.POST['creator_pallet']
        updater = request.POST['updater']

        count_row = PalletSerialNumber.objects.filter(pallet_id=pallet_id).count()
        current_qty = Pallet(current_qty=count_row + 1,
                             pallet_id=pallet_id,
                             # model=model,
                             status=status,
                             create_date=create_date,
                             full=full,
                             # full_date=full_date,
                             wh_id=wh_id,
                             height=height,
                             length=length,
                             width=width,
                             weight=weight,
                             gross_weight=gross_weight,
                             net_weight=net_weight,
                             volume_weight=volume_weight,
                             creator=creator_pallet,
                             updater=updater,
                             update_date=datetime.now(),
                             )

        pallet_ref = Pallet.objects.filter(pk=pallet_id)
        pallet_ref = pallet_ref.first()
        pallet_sn = PalletSerialNumber(serialnumber_id=serial_number,
                                    pallet_id=pallet_ref,
                                    creator=creator,
                                    updater=updater,
                                    create_date=datetime.now(),
                                    update_date=datetime.now(),
                                    )
        RepairMain = apps.get_model('manufacturing', 'RepairMain')

        # sn_object = SerialNumber.objects.get(serial_number=serial_number)
        repairMainFilter = RepairMain.objects.filter(serial_number=serial_number)
        # SerialNumberFilter = SerialNumber.objects.get(pk=serial_number)
        if not SerialNumber.objects.filter(serial_number=serial_number):
            messages.error(request, 'SN: "' + serial_number + '" does not exist.')
            return HttpResponseRedirect(pallet_id + '#Pallet-Detail')

        sn_completed = SerialNumber.objects.filter(serial_number=serial_number).values('completed','shipped','station_id')
        completed_list = sn_completed
        for completed in completed_list:
            if completed['completed'] != 1:
                messages.error(request, 'SN: "' + serial_number + '" is not completed.')
                print('first not completed')
            elif completed['shipped'] == 1:
                messages.error(request, 'SN: "' + serial_number + '" is shipped.')
                print('first is shipped')
            elif completed['station_id'] == 'Repair':
                messages.error(request, 'SN: "' + serial_number + '" is still under repair.')
                print('still under repair')


            elif PalletSerialNumber.objects.filter(serialnumber_id=serial_number).exists():
                messages.error(request, 'SN: "' + serial_number + '" is in Use. Please try again.')
                return HttpResponseRedirect(pallet_id + '#Pallet-Detail')

            # elif len(repairMainFilter) != 0:
            #     messages.error(request, 'SN: "' + serial_number + '" still in Repair station.')
            #     return HttpResponseRedirect(pallet_id + '#Pallet-Detail')
            # elif len(cur_po_object) == 0:
            #     messages.error(request, 'SN: "' + serial_number + '" does not have a PO.')
            #     return HttpResponseRedirect(pallet_id + '#Pallet-Detail')
            else:
                pallet_sn.save()
                pallet_sn.full_clean()
                current_qty.save()
            print (count_row + 1)
            return post(request)

    return redirect(reverse('shipping:pallet_station'))
# #####################################################
# #####################################################
def SerialNumberValidation(serialNumber):
    try:
        sn_object = SerialNumber.objects.get(serial_number=serialNumber)
        current_sn_id = sn_object.id
        if sn_object.status == "Complete":
            return 0
        else:
            ## check if current SN is in repair
            repairMainFilter = RepairMain.objects.filter(serial_number=sn_object)
            if len(repairMainFilter) != 0:
                return "Current serial number is in repair"
            return "Current serial number is in progress."
    except Exception as e:
        return "Current serial number does not exist. "


@login_required
def delete_sn_view(request, pk):
    pallet_id = request.POST['pallet_id']
    # model = request.POST['model']

    create_date = request.POST['create_date']
    creator = request.POST['creator']
    status = request.POST['status']
    # current_qty = request.POST['current_qty']
    full = request.POST['full']
    # full_date = request.POST['full_date']
    wh_id = request.POST['wh_id']
    height = request.POST['height']
    length = request.POST['length']
    width = request.POST['width']
    weight = request.POST['weight']
    gross_weight = request.POST['gross_weight']
    net_weight = request.POST['net_weight']
    volume_weight = request.POST['volume_weight']
    updater = request.POST['updater']
    if request.method == "POST":
        obj = get_object_or_404(PalletSerialNumber, pk=pk)
        obj.delete()
        count_row = PalletSerialNumber.objects.filter(pallet_id=pallet_id).count()
        current_qty = Pallet(current_qty=count_row,
                             pallet_id=pallet_id,
                             # model=model,

                             create_date=create_date,
                             creator=creator,
                             status=status,
                             full=full,
                             # full_date=full_date,
                             wh_id=wh_id,
                             height=height,
                             length=length,
                             width=width,
                             weight=weight,
                             gross_weight=gross_weight,
                             net_weight=net_weight,
                             volume_weight=volume_weight,
                             updater=updater,
                             update_date=datetime.now(),

                             )
        current_qty.save()
        messages.success(request, 'Removed serial number successfully.')

        return HttpResponseRedirect(pallet_id + '/#Pallet-Detail')
        # return redirect (reverse('pallet_detail_delete', pallet_id) + '/#Pallet-Detail')

@login_required
def save_dimension(request):
    def post(request):
        pallet_id = request.POST['pallet_id']
        status = request.POST['status']
        create_date = request.POST['create_date']
        creator = request.POST['creator']
        current_qty = request.POST['current_qty']
        current_qty = int(current_qty) +1
        full = request.POST['full']
        wh_id = request.POST['wh_id']
        height = request.POST['height']
        length = request.POST['length']
        width = request.POST['width']
        weight = request.POST['weight']
        gross_weight = request.POST['gross_weight']
        net_weight = request.POST['net_weight']
        volume_weight = request.POST['volume_weight']
        updater = request.POST['updater']
        # pallet_qty = Pallet.objects.filter(pallet_id=pallet_id).values('current_qty')
        # pallet = Pallet(pallet_id=pallet_id,
        #                 status=0,
        #                 create_date=create_date,
        #                 creator=creator,
        #                 current_qty=pallet_qty,
        #                 full=1,
        #                 full_date=datetime.now(),
        #                 wh_id='WH_SHIP',
        #                 height=height,
        #                 length=length,
        #                 width=width,
        #                 weight=weight,
        #                 gross_weight=gross_weight,
        #                 net_weight=net_weight,
        #                 volume_weight=volume_weight,
        #                 updater=updater,
        #                 update_date=datetime.now(),
        #                 )
        # pallet.save()

        cursor = connection.cursor()
        #query2 = '''update shipping_pallet set "full" = 1, status = 0, wh_id = 'WH_SHIP', height = (%s), length = (%s), width = (%s), weight = (%s), updater = (%s), update_date = NOW(), full_date =  NOW() where pallet_id = (%s)'''
        query2 = '''CALL palletization_save_dimension (%s, %s, %s, %s, %s, %s)'''
        print(query2)
        cursor.execute(query2, [ height, length, width, weight, updater, pallet_id])

        messages.success(request, 'Save dimensions & close ' + pallet_id + ' successfully.')
        return redirect(reverse('shipping:pallet_station'))
    if request.method == 'POST':
        return post(request)
    else:
        pallet_id = request.POST['pallet_id']
        messages.failed(request, 'Dimension value must be a decimal number.')
        return HttpResponseRedirect(pallet_id + '/')


######################## ship out #######################################################
class SalesOrderEnterView(LoginRequiredMixin, generic.ListView):
    model = SalesOrder
    context_object_name = 'salseorder_list'
    template_name = 'production/shipout/shipout.html'
    fields = '__all__'

    def get_queryset(self):
        query = self.request.GET.get('salesorder_id')
        if query:
            return SalesOrder.objects.filter(
                Q(salesorder_id__iexact=query)
            )
        else:
            return SalesOrder.objects.all().order_by('salesorder_id')

    def get_context_data(self, **kwargs):
        context = super(SalesOrderEnterView, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'palletdeliverynumber_list': PalletDeliveryNumber.objects.order_by('row_id'),
            'salseorder_list': SalesOrder.objects.order_by('salesorder_id'),
            'pallet_list': Pallet.objects.order_by('create_date'),
            'palletdeliverynumber_context': PalletDeliveryNumber.objects.all(),
            'salseorder_context': SalesOrder.objects.all(),
            'pallet_context': Pallet.objects.all(),
            'palletsn_list': PalletSerialNumber.objects.order_by('row_id'),
            'palletsn_context': PalletSerialNumber.objects.all(),
        })
        return context

class SalesOrderSuccessView(LoginRequiredMixin, generic.ListView):

    model = SalesOrder
    context_object_name = 'salseorder_list'
    template_name = 'production/shipout/shipout-success.html'
    fields = '__all__'

    def get_queryset(self):
        query = self.request.GET.get('salesorder_id')
        if query:
            return SalesOrder.objects.filter(
                Q(salesorder_id__iexact=query)
            )
        else:
            return SalesOrder.objects.all().order_by('salesorder_id')

    def get_context_data(self, **kwargs):
        context = super(SalesOrderSuccessView, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'palletdeliverynumber_list': PalletDeliveryNumber.objects.order_by('row_id'),
            'salseorder_list': SalesOrder.objects.order_by('salesorder_id'),
            'pallet_list': Pallet.objects.order_by('create_date'),
            'palletdeliverynumber_context': PalletDeliveryNumber.objects.all(),
            'salseorder_context': SalesOrder.objects.all(),
            'pallet_context': Pallet.objects.all(),
            'palletsn_list': PalletSerialNumber.objects.order_by('row_id'),
            'palletsn_context': PalletSerialNumber.objects.all(),
        })
        return context

class SalesDetail(LoginRequiredMixin, generic.DetailView):
    model = SalesOrder
    template_name = 'production/shipout/shipout_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        context = super(SalesDetail, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'palletdeliverynumber_list': PalletDeliveryNumber.objects.order_by('row_id'),
            'salseorder_list': SalesOrder.objects.order_by('salesorder_id'),
            'pallet_list': Pallet.objects.order_by('create_date'),
            'palletdeliverynumber_context': PalletDeliveryNumber.objects.all(),
            'salseorder_context': SalesOrder.objects.all(),
            'pallet_context': Pallet.objects.all(),
            'palletsn_list': PalletSerialNumber.objects.order_by('row_id'),
            'palletsn_context': PalletSerialNumber.objects.all(),
            'dndetail_list': DeliveryNumberDetail.objects.order_by('row_id'),
            'dndetail_context': DeliveryNumberDetail.objects.all(),
        })
        return context

@csrf_exempt
def Process(request):
    if request.method == "POST":

        salesorder = request.POST['salesorder']
        sku = request.POST['sku']
        pallet = request.POST['palletlist']
        y = json.loads(pallet)
        palletdata = []
        for song in y:
            for attribute, value in song.items():
                if attribute == "Pallet":
                    if palletdata.count(value) == 0:
                        palletdata.append(value)
        if len(palletdata) == 0:
            pass
            #return JsonResponse({"error": "Please enter the pallet ID"}, status=400)
        qty = request.POST['qty']
        try:
            qty = int(qty)
        except ValueError:
            pass
            #return JsonResponse({"error": "Quantity is wrong"}, status=400)
        username = request.POST['username']
        data_set = {"username": username, "salesorder": salesorder, "palletlist": palletdata, "sku": sku, "qty": qty}

        req = HttpRequest()
        req.user = request.user
        req.method = 'GET'
        data_set_dupm = json.dumps(data_set)
        req._body = data_set_dupm
        from api.views import getDeliveryNumber
        response = getDeliveryNumber(req)
        json_rep = json.loads(response.content)
        if json_rep['ReturnCode'] == '00':
            messages.success(request, (json_rep))
        else:
            messages.error(request, "failed process, please try again")
        return JsonResponse(json_rep, safe=False, status=200)
    return JsonResponse({"error": "Something went wrong"}, status=400)




# ######################### truckload ###############################
class TruckLoadView(LoginRequiredMixin, View):
    template_name = 'production/truckload/truckload.html'

    truckload_Model = apps.get_model('shipping', 'ShipLoad')

    def get(self, *args, **kwargs):
        context = {}
        template_name = 'production/truckload/truckload.html'
        dn_list = DeliveryNumber.objects.all().filter(shipped=0, confirmed=0, cancelled=0)
        return render(self.request, template_name, {'dn_list': dn_list})

    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            dn = self.request.POST['dn']

            cursor = connection.cursor()
            query = '''select * from get_data_by_dn (%s)'''
            cursor.execute(query, [dn])
            rows = cursor.fetchall()

            dn_data_list = []
            for row in rows:
                d = collections.OrderedDict()
                d['cutomer_po'] = row[0]
                d['salesorder'] = row[1]
                d['so_qty'] = row[2]
                d['ship_qty'] = row[3]
                d['pal_qty'] = row[4]
                dn_data_list.append(d)

            json_output = json.dumps({'dn_table': dn_data_list})

            return JsonResponse(json_output, safe=False, status=200)

        return JsonResponse({"error": ""}, status=400)



# ######################### truckload ###############################
class TruckLoadView(LoginRequiredMixin, View):
    template_name = 'production/truckload/truckload.html'

    truckload_Model = apps.get_model('shipping', 'ShipLoad')

    def get(self, *args, **kwargs):
        context = {}
        template_name = 'production/truckload/truckload.html'
        dn_list = DeliveryNumber.objects.all().filter(shipped=0, confirmed=0, cancelled=0)
        return render(self.request, template_name, {'dn_list': dn_list})

    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            dn = self.request.POST['dn']
            cursor = connection.cursor()
            query = '''select * from get_data_by_dn (%s)'''
            cursor.execute(query, [dn])
            rows = cursor.fetchall()

            dn_data_list = []
            for row in rows:
                d = collections.OrderedDict()
                d['cutomer_po'] = row[0]
                d['salesorder'] = row[1]
                d['so_qty'] = row[2]
                d['ship_qty'] = row[3]
                d['pal_qty'] = row[4]
                dn_data_list.append(d)

            json_output = json.dumps({'dn_table': dn_data_list})

            return JsonResponse(json_output, safe=False, status=200)

        return JsonResponse({"error": ""}, status=400)


@csrf_exempt
def get_pallets_by_dn(request):
    print(request)
    if request.method == "POST":
        dn = request.POST['dn']
        cursor = connection.cursor()
        query = '''select * from get_pallet_by_dn (%s)'''
        cursor.execute(query, [dn])
        rows = cursor.fetchall()
        pallet_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['po'] = row[0]
            d['dn_id'] = row[1]
            d['pallet_id'] = row[2]
            pallet_list.append(d)

        json_output = json.dumps({'pallet_table': pallet_list})

        return JsonResponse(json_output, safe=False, status=200)

    return JsonResponse({"error": ""}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bol_downloader(request):
    _jsondata = request.GET

    if _jsondata and "bol" in _jsondata:

        response = HttpResponse(content_type='application/ms-excel')
        bol = _jsondata['bol']

        if bol:
            ship_obj = ShipLoadService()

            # validate BOL ins shipload
            valid = ship_obj.validate(bol)

            if valid:
                # create excel document payload
                _payload = ship_obj.create_doc(response)
                response.write(_payload.get_data())
            else:
                status = 203
                message = "'bol' {} Was Not Found".format(bol)
                resp = JsonResponse({"status": status, "message": message})
                resp.status_code = status
                return resp

            return response
        else:
            status = 203
            message = "'bol' Does Not Exist"
            resp = JsonResponse({"status": status, "message": message})
            resp.status_code = status
            return resp
    else:
        status = 203
        message = "Missing 'bol' in request"
        resp = JsonResponse({"status": status, "message": message})
        resp.status_code = status
        return resp


class BOLTemplateView(View):
    template_name = './test.html'

    def get(self, request):
        return render(request, self.template_name)


class TruckLoadView(LoginRequiredMixin, View):
    template_name = 'production/truckload/truckload.html'

    truckload_Model = apps.get_model('shipping', 'ShipLoad')

    def get(self, *args, **kwargs):
        context = {}
        template_name = 'production/truckload/truckload.html'
        dn_list = DeliveryNumber.objects.all().filter(shipped=0, confirmed=0, cancelled=0)
        return render(self.request, template_name, {'dn_list': dn_list})

    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            dn = self.request.POST['dn']

            cursor = connection.cursor()
            query = '''select * from get_data_by_dn (%s)'''
            cursor.execute(query, [dn])
            rows = cursor.fetchall()

            dn_data_list = []
            for row in rows:
                d = collections.OrderedDict()
                d['cutomer_po'] = row[0]
                d['salesorder'] = row[1]
                d['so_qty'] = row[2]
                d['ship_qty'] = row[3]
                d['pal_qty'] = row[4]
                dn_data_list.append(d)

            json_output = json.dumps({'dn_table': dn_data_list})

            return JsonResponse(json_output, safe=False, status=200)

        return JsonResponse({"error": ""}, status=400)


@csrf_exempt
def get_pallets_by_dn(request):
    print(request)
    if request.method == "POST":
        dn = request.POST['dn']
        cursor = connection.cursor()
        query = '''select * from get_pallet_by_dn (%s)'''
        cursor.execute(query, [dn])
        rows = cursor.fetchall()
        pallet_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['po'] = row[0]
            d['dn_id'] = row[1]
            d['pallet_id'] = row[2]
            pallet_list.append(d)

        json_output = json.dumps({'pallet_table': pallet_list})

        return JsonResponse(json_output, safe=False, status=200)

    return JsonResponse({"error": ""}, status=400)


@csrf_exempt
def SaveTruckLoad(request):
    result = ''
    sub_result = ''
    bol = ''
    if request.method == "POST":
        container = request.POST['container']
        seal = request.POST['seal']
        dn = request.POST['dn']
        y = json.loads(dn)
        data = []
        for song in y:
            for attribute, value in song.items():
                if attribute == "Delivery No":
                    if data.count(value) == 0:
                        data.append(value)
        print(data)
        print(seal)
        print(container)

        for dn in data:
            print("Validating DN: " + dn)
            cursor = connection.cursor()
            query = '''CALL shipping_validate_dn (%s)'''
            sp_result = cursor.execute(query, [dn])
            rows = cursor.fetchall()
            for row in rows:
                result = row[0]
                print(result)
            if len(result) != 0:
                return JsonResponse({"error": result}, safe=False, status=200)

        print("Generating BOL")
        cursor = connection.cursor()
        query = '''CALL serialization_get_next_value (%s, %s, %s)'''
        sp_result = cursor.execute(query, ['BOL', '0', ''])
        rows = cursor.fetchall()
        for row in rows:
            result = row[0]
            print(result)
            sub_result = result[0:3]
            print(sub_result)
        if sub_result == '99-':
            return JsonResponse({"error": result}, safe=False, status=200)
        bol = result

        print("Performing Truck Load")
        for dn in data:
            cursor = connection.cursor()
            query = '''CALL shipping_truckload_save_sp (%s, %s, %s, %s, %s, %s)'''
            sp_result = cursor.execute(query, ['NEW', dn, bol, container, seal, ''])
            rows = cursor.fetchall()
            for row in rows:
                result = row[0]
                print(result)
                if sub_result == '99-':
                    return JsonResponse({"error": result}, safe=False, status=200)

        return JsonResponse({"error": ""}, safe=False, status=200)

    return JsonResponse({"error": "Bad Request Call"}, safe=False, status=400)


@csrf_exempt
def ValidateSN(request):
    result = ''

    if request.method == "POST":
        serialnumber = request.POST['serialnumber']

        print(serialnumber)
        cursor = connection.cursor()

        query = '''CALL shipping_validate_sn (%s)'''
        sp_result = cursor.execute(query, [serialnumber])
        rows = cursor.fetchall()
        for row in rows:
            result = row[0]
            print(result)
        if len(result) != 0:
            return JsonResponse({"error": result}, safe=False, status=200)

    return JsonResponse({"error": "Bad Request Call"}, safe=False, status=400)

@csrf_exempt
def ValidateSKU(request):
    result = ''

    if request.method == "POST":
        sku= request.POST['sku']

        print(serialnumber)
        cursor = connection.cursor()

        query = '''CALL shipping_validate_sku (%s)'''
        sp_result = cursor.execute(query, [sku])
        rows = cursor.fetchall()
        for row in rows:
            result = row[0]
            print(result)
        if len(result) != 0:
            return JsonResponse({"error": result}, safe=False, status=200)

    return JsonResponse({"error": "Bad Request Call"}, safe=False, status=400)


##### sales order ####################
class SalesOrderListView(LoginRequiredMixin, generic.ListView):
    model = SalesOrder
    context_object_name = 'salseorder_list'
    template_name = 'manufacturing/salesorder/somanager_list.html'
    fields = '__all__'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('salesorder_id')
        if query:
            return SalesOrder.objects.filter(
                Q(salesorder_id__icontains=query)
            )
        else:
            return SalesOrder.objects.all().order_by('salesorder_id')

        return context

class SalesOrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = SalesOrder
    template_name = 'manufacturing/salesorder/somanager_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        context = super(SalesOrderDetailView, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'palletdeliverynumber_list': PalletDeliveryNumber.objects.order_by('row_id'),
            'salseorder_list': SalesOrder.objects.order_by('salesorder_id'),
            'pallet_list': Pallet.objects.order_by('create_date'),
            'palletdeliverynumber_context': PalletDeliveryNumber.objects.all(),
            'salseorder_context': SalesOrder.objects.all(),
            'pallet_context': Pallet.objects.all(),
            'palletsn_list': PalletSerialNumber.objects.order_by('row_id'),
            'palletsn_context': PalletSerialNumber.objects.all(),
            'dndetail_list': DeliveryNumberDetail.objects.order_by('row_id'),
            'dndetail_context': DeliveryNumberDetail.objects.all(),
        })
        return context

class SalesOrderUpdate(LoginRequiredMixin, UpdateView):
    model = SalesOrder
    template_name = 'manufacturing/salesorder/somanager_detail.html'
    fields = '__all__'
    success_url = reverse_lazy('manufacturing:salesorder_list')

    def get_name(request):
        if request.method == 'POST':
            form = SalesOrderUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('manufacturing/salesorder/somanager_list.html')
            else:
                form = SalesOrderUpdate()
            return render(request, 'manufacturing/salesorder/somanager_list.html', {'form': form})

##### deliver number ####################
class DeliveryNumberListView(LoginRequiredMixin, generic.ListView):
    model = DeliveryNumber
    context_object_name = 'deliverynumber_list'
    template_name = 'manufacturing/deliverynumber/deliverynumber_list.html'
    fields = '__all__'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('deliverynumber')
        if query:
            return DeliveryNumber.objects.filter(
                Q(deliverynumber_id__iexact=query)
            )
        else:
            return DeliveryNumber.objects.all().order_by('deliverynumber_id')

    def get_context_data(self, **kwargs):
        context = super(DeliveryNumberListView, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'deliverynumberdetail_list': DeliveryNumberDetail.objects.order_by('salesorder_id'),
            'deliverynumberdetail_context': DeliveryNumberDetail.objects.all(),
        })
        return context

class DeliveryNumberDetailView(LoginRequiredMixin, generic.DetailView):
    model = DeliveryNumber
    template_name = 'manufacturing/deliverynumber/deliverynumber_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        context = super(DeliveryNumberDetailView, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'palletdeliverynumber_list': PalletDeliveryNumber.objects.order_by('row_id'),
            'salseorder_list': SalesOrder.objects.order_by('salesorder_id'),
            'pallet_list': Pallet.objects.order_by('create_date'),
            'palletdeliverynumber_context': PalletDeliveryNumber.objects.all(),
            'salseorder_context': SalesOrder.objects.all(),
            'pallet_context': Pallet.objects.all(),
            'palletsn_list': PalletSerialNumber.objects.order_by('row_id'),
            'palletsn_context': PalletSerialNumber.objects.all(),
            'dndetail_list': DeliveryNumberDetail.objects.order_by('row_id'),
            'dndetail_context': DeliveryNumberDetail.objects.all(),
        })
        return context



# ########## un pallet ##########
class UNPalletStationDetailView(LoginRequiredMixin, generic.ListView):
    Pallet = apps.get_model('shipping', 'Pallet')


    # permission_required = 'manufacturing.can_repair'
    model = Pallet
    context_object_name = 'pallet_list'
    template_name = 'unpallet/unpallet.html'
    fields = '__all__'

    def get_queryset(self):
        query = self.request.GET.get('pallet_id')
        if query:
            return Pallet.objects.filter(
                Q(pallet_id__iexact=query)
            )
        else:
            return Pallet.objects.all().order_by('pallet_id')

    def get_context_data(self, **kwargs):
        Git = apps.get_model('git', 'git')
        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        context = super(UNPalletStationDetailView, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'palletsn_list': PalletSerialNumber.objects.order_by('create_date'),
            'more_context': PalletSerialNumber.objects.all(),
            'serialnumber_list': SerialNumber.objects.order_by('generated_date'),
            'sn_context': SerialNumber.objects.all(),
            'git_list': Git.objects.order_by('asset_no_id'),
            'git_context': Git.objects.all(),
        })
        return context


class UNPalletDetail(LoginRequiredMixin, generic.DetailView):
    model = Pallet
    template_name = 'unpallet/unpallet_detail.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        Git = apps.get_model('git', 'git')
        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        context = super(UNPalletDetail, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])

        context.update({
            'palletsn_list': PalletSerialNumber.objects.order_by('row_id'),
            'pallet_list': Pallet.objects.order_by('create_date'),
            'serialnumber_list': SerialNumber.objects.order_by('generated_date'),
            'more_context': PalletSerialNumber.objects.all(),
            'pallet_context': Pallet.objects.all(),
            'sn_context': SerialNumber.objects.all(),
            'git_list': Git.objects.order_by('asset_no_id'),
            'git_context': Git.objects.all(),
        })
        return context

# def PalletMerge(request):
#     # http://127.0.0.1:8000/shipping/wip/pallet/merge/
#     pallet_serialnumber_object = apps.get_model('shipping', 'PalletSerialNumber')
#     git_git_object = apps.get_model('git', 'git')
#     serialnumber_object = apps.get_model('manufacturing', 'SerialNumber')
#     materialmaster_object = apps.get_model('manufacturing', 'MaterialMaster')
#
#     if request.method == 'POST':
#         pallet_id_1 = request.POST['pallet_id_1']
#         pallet_id_2 = request.POST['pallet_id_2']
#
#         pallet_serialnumber_1 = pallet_serialnumber_object.objects.filter(pallet_id=pallet_id_1).values()
#         pallet_serialnumber_2 = pallet_serialnumber_object.objects.filter(pallet_id=pallet_id_2).values()
#
#         pallet1_qty = len(pallet_serialnumber_1)
#         pallet2_qty = len(pallet_serialnumber_2)
#
#         # check if two pallets' PO match
#         serial_number_1 = pallet_serialnumber_1[0]['serialnumber_id']
#         serial_number_2 = pallet_serialnumber_2[0]['serialnumber_id']
#         PO_serialnumber_1 = git_git_object.objects.filter(serialnumber=serial_number_1).values()[0]['po_no']
#         PO_serialnumber_2 = git_git_object.objects.filter(serialnumber=serial_number_2).values()[0]['po_no']
#         if PO_serialnumber_1 != PO_serialnumber_2:
#             errorMessage = 'PO does not match'
#             return HttpResponse(None)
#
#         # get first pallet limit
#         serialnumber_modelid = serialnumber_object.objects.filter(serial_number=serial_number_1).values()[0][
#             'model_id_id']
#         first_pallet_limit = materialmaster_object.objects.filter(model_id=serialnumber_modelid).values()[0][
#             'pallet_limit']
#         if (pallet1_qty + pallet2_qty) > first_pallet_limit:
#             errorMessage = 'total quantity exceed the pallet limit, can not merge'
#             return HttpResponse(None)
#
#         cursor = connection.cursor()
#         sql = '''select public.pallet_id_merge(%s, %s, %s)'''
#         cursor.execute(sql, [pallet_id_1, pallet_id_2, ''])
#         return HttpResponse(None)
#     return HttpResponse(None)

# def PalletDelete(request):
#     #####################################################################################
#     # 1. need to delete the pallet_id record from shipping_palletdeliverynumber
#     # 2. need to delete all pallet_id with serial number from shipping_palletserialnumber
#     # 3. updating table manufacturing_serialnumberlog
#     #####################################################################################
#     request.method = 'POST'
#     if request.method == 'POST':
#         pallet_id = request.POST['pallet_id']
#         user = request.POST['user']
#         cursor = connection.cursor()
#         sql_query = '''SELECT * FROM public.pallet_id_delete(%s, %s)'''
#         cursor.execute(sql_query, [pallet_id, user])
#         res_message = cursor.fetchall()[0][0]
#         if res_message == 'No records found for current pallet id':
#             return HttpResponse(res_message)
#         return HttpResponse('Success')
#     pass


class PalletTemplateForm(View):
    template_name = "pallet_list_print.html"

    def get(self, request):
        first_start = 1
        second_start = 10
        amount_of_barcodes = 18

        data = request.GET

        pallet_id = data.get('pallet-id')
        context = None
        if pallet_id:

            # SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
            # sns = SerialNumber.objects.all()[:amount_of_barcodes]
            # sn_list = [sn.serial_number for sn in sns]
            now = tz.now()


            cursor = connection.cursor()
            query = '''SELECT get_sn_by_pallet (%s)'''
            fn_result = cursor.execute(query, [pallet_id])
            sn_list = cursor.fetchall()
            part_number = SerialNumber.objects.filter(pk=sn_list[0][0]).first().model_id
            sn_list = [sn[0] for sn in sn_list]
            
            context = { 
                # 'serial_numbers' : sn_list,
                'serial_numbers' : sn_list,
                'first_range' : range(first_start,second_start),
                'second_range' : range(second_start,amount_of_barcodes+1),
                'user' : str(request.user),
                'date' : datetime.now().date(),
                'pallet_id' : pallet_id,
                'part_number': part_number
                }


        return render(request,self.template_name,context)

