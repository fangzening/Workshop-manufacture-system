# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import IntegrityError
from .models import Station
from django.shortcuts import render, redirect
from django.apps import apps
from .models import Route, StationRoutes, Action, Template, TemplateActions
from .forms import RouteForm, RouteSearchForm, PackForm, PalletForm
from datetime import datetime
from django.http import HttpRequest, QueryDict, HttpResponse, Http404
from django.template.loader import render_to_string

from .wip.process import process

import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.db import transaction
from django.utils.timezone import make_aware
from django.urls import reverse
from .wip.helper.serialnumber_scan import serialnumber_scan
from manufacturing.models import *
from django.db.models import Q

from api.keypart.check_mask import check_mask

@login_required
def route_config(request):
    def post(request):
        data = request.POST
        route_id = str(data.get('route_id'))
        ver = str(data.get('ver'))
        plantcode = str(data.get('plantcode'))
        user = str(request.user)
        first_station = data.get('first_station')

        first_station = Station(pk=first_station)

        Prod_Version = apps.get_model('line', 'Prod_Version')

        prod_version_ref = Prod_Version.objects.filter(pk=ver)

        if prod_version_ref:
            prod_version_ref = prod_version_ref.first()

            route = Route.objects.create(
                                        route_id=route_id,
                                        prod_version=prod_version_ref,
                                        first_station=first_station,
                                        plant_code=plantcode,
                                        creator=user,
                                        create_date=datetime.now(),
                                        updater=user,
                                        update_date=datetime.now()
                                         )
            route.full_clean()
            route.save()

            station_r = StationRoutes.objects.create(
                route=route,
                station=first_station,
                next_station=None,
                state='PASS',
                sequence=0

            )

            station_r.full_clean()
            station_r.save()

            return redirect('line:route')

    def get(request):

        template_name = 'line/route-form.html'
        form = RouteForm()

        stations = Station.objects.all().order_by('station_id')
        Prod_Version = apps.get_model('line','Prod_Version')
        prod_versions = Prod_Version.objects.all()

        context = {
            'form': form,
            'stations': stations,
            'prod_versions' : prod_versions
        }
        return render(request, template_name, context)

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


@login_required
def route_list(request):
    def get(request):

        station = request.GET.get('station')
        route = request.GET.get('route')

        if station == None and route == None:

            route_list = Route.objects.all().order_by('route_id')

            context = {
                'route_list': route_list,

            }

            return render(request, 'line/route-list.html', context)
        else:
            return render(request, 'line/route-list.html')

    if request.method == 'GET':

        return get(request)
    elif request.method == 'POST':
        pass

@login_required
def station_route(request):
    def post(request):

        pass

    def get(request):
        data = request.GET

        route_id = data.get('route_id')

        route_ref = Route.objects.filter(pk=route_id)

        if route_ref:
            route_ref = route_ref.first()

            stations = route_ref.get_stations()

            context = {
                'stations': stations,
                'route_id': route_id,
            }

            return render(request, 'line/station-list.html', context)
        else:

            return render(request, 'line/station-list.html')

        template_name = 'line/station-list.html'
        return render(request, template_name)

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


@login_required
def station_config(request):
    def post(request):

        station_name = request.POST['station-name']
        station_description = request.POST['station-description']
        template = request.POST['template']  # Template.objects.get(pk=request.POST['template'])
        creator = str(request.user)
        create_date = datetime.now()
        updater = creator
        update_date = datetime.now()

        
        station = Station(pk=station_name,
                          desc=station_description,
                          template_id=Template.objects.filter(pk=template).first(),
                          creator=creator,
                          create_date=create_date,
                          updater=updater,
                          update_date=update_date
                          )

        station.save()

        return redirect('line:all-stations')

    def get(request):

        templates = Template.objects.all().order_by('pk')

        template_actions_dict = dict()

        for template in templates:
            template_actions = TemplateActions.objects.filter(template_id=template).order_by('pk')

            actions = list()

            for ta in template_actions:
                actions.append(ta.action_id.name)

            template_actions_dict[template.template_id] = actions

        context = {
            'templates': templates,
            'template_actions': template_actions_dict,
        }

        template_name = 'line/station-create.html'
        return render(request, template_name, context)

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


@login_required
def station_edit(request, station_id):
    def post(request):
        station = Station.objects.get(pk=station_id)

        station.pk = request.POST['station-name']
        station.desc = request.POST['station-description']
        station.template = Template.objects.get(pk=request.POST['template'])
        station.updater = str(request.user)
        station.update_date = datetime.now()

        station.save()

        return redirect('line:all-stations')

    def get(request):
        station = Station.objects.get(pk=station_id)

        templates = Template.objects.all().order_by('pk')

        template_actions_dict = dict()

        for template in templates:
            template_actions = TemplateActions.objects.filter(template_id=template).order_by('pk')

            actions = list()

            for ta in template_actions:
                actions.append(ta.action.name)

            template_actions_dict[template.template_id] = actions

        context = {
            'templates': templates,
            'template_actions': template_actions_dict,
            'station': station,
        }

        template_name = 'line/station-edit.html'
        return render(request, template_name, context)

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


# collect stations to display in after production flow
@login_required
def station_list(request):
    def get(request):

        prod_ver = request.GET.get('ver')

        Prod_Version = apps.get_model('line', 'Prod_Version')

        prod_version_ref = Prod_Version.objects.filter(pk=prod_ver)

        if prod_version_ref:
            prod_version_ref = prod_version_ref.first()

            station_list = []
            route = Route.objects.filter(prod_version=prod_version_ref)

            if route:
                route = route.first()

                station_list = route.get_stations()

                context = {
                    'station_list': station_list,
                    'route': route,
                    'ver': str(route.prod_version)
                }
                print(route.prod_version)

            if len(station_list) == 0:
                error = 'Route Has No Stations'
                form = RouteSearchForm()

                context = {
                    'error': error,
                    'form': form,

                }
                return render(request, 'line/production-search.html', context)

            return render(request, 'line/production.html', context)
        else:
            error = 'Version Does Not Exist'
            form = RouteSearchForm()

            context = {
                'error': error,
                'form': form
            }

            return render(request, 'line/production-search.html', context)

    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':
        return render(request, 'line/production-search.html', context)
        # return post(request)


@login_required
def wip_search(request):
    def get(request):
        form = RouteSearchForm()
        context = {
            'form': form
        }
        template_name = 'line/production-search.html'
        return render(request, template_name, context)
        # will return basic page

    return get(request)


@login_required
def wip_flow(request):
    def get(request):

        raise Http404("Can't go to page by searching!")

    def post(request):
        data = request.POST

        template = data.get('template')
        route_id = data.get('route')
        station_id = data.get('station')
        ver = data.get('ver')

        StationRoutes = apps.get_model('line', 'StationRoutes')

        station_route_ref = StationRoutes.objects.filter(route_id=route_id, station=station_id)
        station_route_ref = station_route_ref.first()

        Station = apps.get_model('line', 'Station')
        station_ref = Station.objects.filter(pk=station_id)
        station_ref = station_ref.first()

        context = {
            'template': template,
            'route_id': route_id,
            'station_id': station_id,
            'ver': ver,
            'station_name': station_ref
        }

        template_ref = Template.objects.filter(name=template)
        template_ref = template_ref.first()

        if template_ref:
            temp_name = template_ref.name

            if temp_name == 'Start':
                template_name = 'production/start.html'
                return render(request, template_name, context)

            elif temp_name == 'KeyPart':
                template_name = 'production/key-part.html'
                return render(request, template_name, context)

            elif temp_name == 'Test':
                template_name = 'production/test.html'

                return render(request, template_name, context)

            elif temp_name == 'Complete':
                template_name = 'production/complete.html'
                return render(request, template_name, context)

            elif temp_name == 'Palletize':
                template_name = 'production/palletize.html'
                return render(request, template_name, context)

            elif temp_name == 'Pack':
                template_name = 'production/pack.html'
                return render(request, template_name, context)
            elif temp_name == 'Shipping':
                template_name = 'production/shipping.html'
                return render(request, template_name, context)

            elif temp_name == 'Repair':
                template_name = 'production/repair.html'
                return render(request, template_name, context)

        else:
            form = RouteSearchForm()
            context = {
                'form': form
            }
            template_name = 'line/production-search.html'
            return render(request, template_name, context)

    if request.method == 'POST':

        # if 'assembly' in str(request.body):

        #     template_name = 'line/production-search.html'
        #     return render(request, template_name)

        if request.POST.get('submit'):

            if request.POST.get('submit') != '':
                return process(request)




        else:
            return post(request)


    else:

        return get(request)

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
@login_required
def all_stations(request):
    def get(request):
        # object_list = Station.objects.filter(status=1).order_by('station_id')
        station_list = Station.objects.all().order_by('station_id')
        paginator = Paginator(station_list, 20)  # 3 posts in each page
        page = request.GET.get('page')
        try:
            station_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            station_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            station_list = paginator.page(paginator.num_pages)
        # return render(request,
        #               'index.html',
        #               {'page': page,
        #                'post_list': post_list})

        # station = request.GET.get('station')
        # route = request.GET.get('route')

        # if station == None and route == None:


        context = {
            'station_list': station_list,
            'page': page,

        }

        return render(request, 'line/all-stations.html', context)
        # else:
        #     return render(request,'line/route-list.html')



    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':

        pass
        # return post(request)


@login_required
def stationroute_create(request):
    def post(request):

        route_id = request.POST['route-id']

        station_id = request.POST['station']

        next_station_id = request.POST['next_station']

        state = request.POST['state']

        if route_id and station_id and next_station_id:

            # n_station_id = next_station.first().id
            if station_id != next_station_id:
                station = Station.objects.filter(pk=station_id).first()
                next_station = Station.objects.filter(pk=next_station_id).first()

                
                try:
                    StationRoutes.objects.create(
                            route_id=route_id,
                            station=station,
                            next_station=next_station,
                            state=state,
                            sequence=0
                            )
            
                except:
               
                    print("couldn't create stationroute")

                    print("couldn't create stationroute")

        response = redirect('line:stations')
        response['Location'] += '?route_id=' + str(route_id)
        return response

    def get(request):

        route_id = request.GET['route-id']

        station_route_objects = StationRoutes.objects.filter(route=route_id)

        # route_obj = Route.objects.filter(pk=route_id)
        # route_obj = route_obj.first()

        # stations = Station.objects.exclude(pk=route_obj.first_station.id)
        stations = Station.objects.all()
        # states = State.objects.all()

        context = {
            'stations': stations,
            'route_id': route_id,
            # 'states' : states
        }

        template_name = 'line/stationroute-create.html'
        return render(request, template_name, context)

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


@login_required
def check_in(request):
    WorkOrder = apps.get_model('manufacturing', 'WorkOrder')
    template_name = 'line/check-in.html'

    def get(request):

        if 'searchID' in request.GET:

            if 'q' in request.GET:

                query = request.GET['q']

                workorder = WorkOrder.objects.filter(
                    Q(pk=query)
                )

                workorder_name = ""

                context = {
                    'workorder': workorder
                }

                if workorder:
                    workorder_name = workorder.first().pk
                    context['workorder_name'] = workorder_name
                else:
                    context['message'] = "Work Order Doesn't Exist"
                    context['result'] = 'FAIL'

                return render(request, template_name, context)
        else:
            return render(request, template_name)

    def post(request):
        data = request.POST
        workorder = data.get('workorder')
        message = "Work Order " + workorder + " doesn't exist"
        result = "FAIL"

        workorder_list = WorkOrder.objects.filter(
            Q(pk=workorder)
        )

        workorder_ref = WorkOrder.objects.filter(pk=workorder)

        if workorder_ref:
            workorder_ref = workorder_ref.first()
            message = "Work Order " + workorder + " isn't ready to be picked"

            if workorder_ref.pick_status == 'n' and workorder_ref.target_qty == workorder_ref.finished_qty:
                workorder_ref.pick_status = 'y'
                result = "success"
                message = "Work Order " + workorder + " was picked!"
                workorder_ref.save()
            elif workorder_ref.pick_status == 'y':
                message = "Work Order " + workorder + " was already picked!"

        context = {
            'result': result,
            'message': message,
            'workorder_name': workorder,
            'workorder': workorder_list
        }

        return render(request, template_name, context)

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


def pack_config(request):
    template_name = 'line/pack-config.html'

    def get(request):
        PackConfig = apps.get_model('line', 'PackConfiguration')

        packs = PackConfig.objects.all()

        context = {
            'packs': packs
        }

    return get(request)


def create_pack_config(request):
    template_name = 'line/create-pack-config.html'

    def get(request):

        form = PackForm()

        context = {
            'form': form
        }

        return render(request, template_name, context)

    def post(request):

        data = request.POST

        workorder_type = data.get('workorder_type')
        options = data.getlist('options')

        form = PackForm()
        context = {
            'form': form
        }
        PackConfiguration = apps.get_model('line', 'PackConfiguration')

        label = 0
        country_kit = 0

        if '1' in options:
            print_label = 1
        if '2' in options:
            country_kit = 1

        pack = PackConfiguration.objects.create(workorder_type=workorder_type,
                                                print_label=print_label,
                                                country_kit=country_kit
                                                )
        pack.clean()
        pack.save()

        return redirect('line:pack')

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


@login_required
def check_in(request):
    WorkOrder = apps.get_model('manufacturing', 'WorkOrder')
    template_name = 'line/check-in.html'

    def get(request):

        if 'searchID' in request.GET:

            if 'q' in request.GET:

                query = request.GET['q']

                workorder = WorkOrder.objects.filter(
                    Q(pk=query)
                )

                workorder_name = ""

                context = {
                    'workorder': workorder
                }

                if workorder:
                    workorder_name = workorder.first().pk
                    context['workorder_name'] = workorder_name
                else:
                    context['message'] = "Work Order Doesn't Exist"
                    context['result'] = 'FAIL'

                return render(request, template_name, context)
        else:
            return render(request, template_name)

    def post(request):
        data = request.POST
        workorder = data.get('workorder')
        message = "Work Order " + workorder + " doesn't exist"
        result = "FAIL"

        workorder_list = WorkOrder.objects.filter(
                    Q(pk=workorder)
                )

        workorder_ref = WorkOrder.objects.filter(pk=workorder)
        
        if workorder_ref:
            workorder_ref = workorder_ref.first()
            message = "Work Order " + workorder + " isn't ready to be picked"

            if workorder_ref.pick_status == 'n' and workorder_ref.target_qty == workorder_ref.finished_qty:
                workorder_ref.pick_status = 'y'
                result = "success"
                message = "Work Order " + workorder + " was picked!"
                workorder_ref.save()
            elif workorder_ref.pick_status == 'y':
                message = "Work Order " + workorder + " was already picked!"

        context = {
            'result': result,
            'message': message,
            'workorder_name': workorder,
            'workorder': workorder_list
        }

        return render(request, template_name, context)

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


def pack_config(request):
    template_name = 'line/pack-config.html'

    def get(request):
        PackConfig = apps.get_model('line', 'PackConfiguration')

        packs = PackConfig.objects.all()

        context = {
            'packs': packs
        }

        return render(request, template_name, context)

    return get(request)


def create_pack_config(request):
    template_name = 'line/create-pack-config.html'

    def get(request):

        form = PackForm()

        context = {
            'form': form
        }

        return render(request, template_name, context)

    def post(request):

        data = request.POST

        workorder_type = data.get('workorder_type')
        options = data.getlist('options')

        form = PackForm()
        context = {
            'form': form
        }
        PackConfiguration = apps.get_model('line', 'PackConfiguration')

        label = 0
        country_kit = 0

        if '1' in options:
            print_label = 1
        if '2' in options:
            country_kit = 1

        pack = PackConfiguration.objects.create(workorder_type=workorder_type,
                                                print_label=print_label,
                                                country_kit=country_kit
                                                )
        pack.clean()
        pack.save()

        return redirect('line:pack')

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


def stationroute_edit(request):
    method = request.method
    template_name = 'line/route/edit-station-route.html'

    StationRoute = apps.get_model('line', 'StationRoutes')

    Station = apps.get_model('line', 'Station')

    def get(request):
        data = request.GET

        route_id = data.get('route_id')
        station_id = data.get('station_id')

        context = {
            'route_id': route_id,
            'station_id': station_id,

        }

        '''
        get unused stations
        and station routes for current station
        '''

        stations = StationRoutes.objects.filter(route=route_id, station=station_id)
        station_ref = Station.objects.filter(pk=station_id)
        route_ref = Route.objects.filter(route_id=route_id)

        if route_ref:
            context['station_list'] = route_ref.first().get_stations()

        if station_ref:
            context['station'] = station_ref.first()

        if stations:
            context['stations'] = stations
            context['repaired_station'] = stations[0].repaired_station


        return render(request, template_name, context)

        '''
        station
        state
        route

        '''

    def post(request):

        data = request.POST

        response = None

        action = data.get('action')
        route_id = data.get('route_id') 
        station_id = data.get('station_id')


        def delete_one():
            stationroute_id = int(data.get('stationroute_id') or -1)

            stationroute_ref = StationRoute.objects.filter(pk=stationroute_id)

            if stationroute_ref:
                stationroute_ref = stationroute_ref.first()
                stationroute_ref.remove_station_route()

        def delete_many():

            stationroute_ref = StationRoute.objects.filter(route=route_id, station=station_id)

            if stationroute_ref:
                stationroute_ref = stationroute_ref.first()
                stationroute_ref.remove_all_station_routes()
            else:

                stationroute_ref = StationRoute.objects.filter(route=route_id, next_station=station_id)

                stationroute_ref = stationroute_ref.first()
                stationroute_ref.remove_station_route() 
            response = redirect('line:stations')
            response['Location'] += '?&route_id=' + str(route_id)
            return response

        def change_states():
            stationroute_id = int(data.get('stationroute_id') or -1)
            state = data.get('state')
            stationroute_ref = StationRoute.objects.filter(pk=stationroute_id)

            if stationroute_ref and state:
                stationroute_ref = stationroute_ref.first()

                stationroute_ref.state = state
                stationroute_ref.save()

        def repair_station():

            repaired_station = data.get('repair_station')
            stationroute_ref = StationRoute.objects.filter(station_id=station_id, route_id=route_id)
            station_ref = Station.objects.filter(station_id=repaired_station)


            if stationroute_ref and station_ref:

                for stationroute in stationroute_ref:

                    stationroute.repaired_station = station_ref.first()
                    stationroute.save()




        if action == 'delete_one':
            delete_one()
        elif action == 'delete_many':
            response = delete_many()
        elif action == 'save':
            change_states()
        elif action == 'repair_station':
            repair_station()

        if not response:
            response = redirect('line:station-route-edit')
            response['Location'] += '?station_id=' + str(station_id) + '&route_id=' + str(route_id)

        return response

    if method == 'POST':
        return post(request)
    else:
        return get(request)


class TestingResultUpdate(LoginRequiredMixin, UpdateView):
    TestingResult = apps.get_model('manufacturing', 'TestingResult')
    model = TestingResult
    template_name = 'manufacturing/wip/repair.html'
    fields = ['result']
    success_url = reverse_lazy('manufacturing:repair_station')

    def get_name(request):
        if request.method == 'POST':
            form = TestingResultUpdate(request.POST)
            if form.is_valid():
                # return HttpResponseRedirect('manufacturing/wip/repair.html')
                return redirect(reverse('manufacturing:repair_station') + '?sn=' + str(testingresult.serial_number))
            else:
                form = TestingResultUpdate()
            # return render(request, 'manufacturing/wip/repair.html', {'form': form})
            # return reverse("manufacturing:repair_station", kwargs={'pk': pk})
            return redirect(reverse('manufacturing:repair_station') + '?sn=' + str(testingresult.serial_number))

    def post(self, request):
        data = request.POST
        # data is a dictionary version of all data taken from POST
        if 'get_wo' in data:
            first_char = 'A'
            model_name = str(data.get('work order model'))
            count = str(SerialNumber.objects.count())
            while len(count) < 10:
                count = '0' + count
            serial_num = first_char + model_name + count

        return redirect('manufacturing:workorder_list')


@transaction.atomic
# @csrf_exempt
# @xframe_options_sameorigin

def replace_part(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        template = data.get('template')
        route_id = data.get('route_id')
        station_id = data.get('station_id')
        model = data.get('model')
        serial_number = data.get('serial_number')

        failure_sequence = data.get('failure_sequence')
        repaired_code = data.get('repaired_code')
        repaired_description = data.get('repaired_description')
        out_part_no = data.get('out_part_no')
        out_part_sn = data.get('out_part_sn')
        in_part_no = data.get('part')
        in_part_sn = data.get('kp_serialnumber')
        creator = str(request.user)

        RepairMain = apps.get_model('manufacturing', 'RepairMain')
        repairmain_ref = RepairMain.objects.filter(failure_sequence=failure_sequence)

        RepairDetail = apps.get_model('manufacturing', 'RepairDetail')

        RepairCode = apps.get_model('manufacturing', 'RepairCode')
        repair_code_ref = RepairCode.objects.filter(pk=repaired_code)

        serialnumber_ref = serialnumber_scan(request)

        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        sn = data.get('serial_number')

        sn_list = SerialNumber.objects.filter(serial_number=sn)

        Station = apps.get_model('line', 'Station')
        station_ref = Station.objects.filter(pk=station_id)
        station_ref = station_ref.first()

        if not repair_code_ref:
            error = 'Repair code does not exist.'
            return HttpResponse(error)

        elif in_part_no != out_part_no:
            error = 'Part numbers do not match.'
            return HttpResponse(error)

        elif repair_code_ref and repairmain_ref and in_part_no == out_part_no:

            KeyPart = apps.get_model('manufacturing', 'KeyPart')

            key_parts = KeyPart.objects.filter(serialnumber=serial_number).values_list('model_id', flat=True)

            if out_part_no not in key_parts:
                error = 'OUT part no is not a keypart for this serial number.'
                return HttpResponse(error)

            if in_part_no not in key_parts:
                error = 'IN part no is not a keypart for this serial number.'
                return HttpResponse(error)

            filtered_key_parts = key_parts.filter(model_id=out_part_no, cserialnumber=out_part_sn)

            if not filtered_key_parts:
                if out_part_sn == '':
                    error = 'All parts ' + str(out_part_no) + ' have PartSN installed. Please provide an OUT serial number to replace.'
                    return HttpResponse(error)                

            if out_part_sn:
                key_parts = KeyPart.objects.filter(cserialnumber=out_part_sn)
                if not key_parts:
                    error = 'OUT Part Serial Number does not exist.'
                    return HttpResponse(error)

            if out_part_sn != '' and in_part_sn == '':
                error = 'Please provide a value for IN Part Serial Number'
                return HttpResponse(error)        
            
            if in_part_sn != '':
                keypart = KeyPart.objects.filter(cserialnumber=in_part_sn)

                if keypart:
                    error = 'IN Part Serial Number already in use.'
                    return HttpResponse(error)

                Mask = apps.get_model('maskconfig', 'Mask')

                mask_ref = Mask.objects.filter(model=in_part_no)

                data_for_mask = {
                        'PartSN': in_part_sn,
                        'mask': None
                }

                if mask_ref:
                    mask_ref = mask_ref.first()
                    data_for_mask['mask'] = mask_ref

                mask_result = check_mask(data_for_mask)

                if mask_result != 'Success':
                    return HttpResponse(mask_result)
                      
            repairmain_ref = repairmain_ref.first()
            repair_code_ref = repair_code_ref.first()

            try:
                repairdetail_ref = RepairDetail(failure_sequence = repairmain_ref,
                                                repaired_code = repair_code_ref,
                                                repaired_description = 'Replaced a part',
                                                replacement = 1,
                                                in_part_no = in_part_no,
                                                out_part_no = out_part_no,
                                                in_cserialno = in_part_sn,
                                                out_cserialno = out_part_sn,
                                                repaired_date = make_aware(datetime.now())                                                                                        
                                                )
                repairdetail_ref.save()
        
                key_part = KeyPart.objects.filter(serialnumber=serial_number, model_id = out_part_no, cserialnumber=out_part_sn)

                if key_part:
                    key_part = key_part.first()
                    key_part.model_id = in_part_no                
                    key_part.cserialnumber = in_part_sn
                    key_part.update_date = make_aware(datetime.now())
                    key_part.updater = str(request.user)                                
                    key_part.save()
            except Exception as e:
                print(e.message)

            return HttpResponse("Part was replaced successfully.")
        else:
            return HttpResponse("Something went wrong.")    


def update_repair(request):
    def get_serialnumber(request):
        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        serial_number = request.POST.get('serial_number')
        serial_number_ref = SerialNumber.objects.filter(serial_number=serial_number)
        return serial_number_ref.first()

    if request.method == 'POST':
        data = request.POST

        failure_sequence = data.get('failure_sequence')
        repaired_code = data.get('repaired_code')
        repaired_description = data.get('repaired_description')
        replacement = data.get('replacement')
        in_part_no = data.get('in_part_no')
        out_part_no = data.get('out_part_no')
        creator = str(request.user)
        repaired_date = data.get('repaired_date')
        template_name = 'production/repair.html'

        RepairMain = apps.get_model('manufacturing', 'RepairMain')
        repairmain_ref = RepairMain.objects.filter(failure_sequence=failure_sequence)

        RepairDetail = apps.get_model('manufacturing', 'RepairDetail')

        RepairCode = apps.get_model('manufacturing', 'RepairCode')
        repair_code_ref = RepairCode.objects.filter(pk=repaired_code)
        repairmain = get_serial_numbers(request)

        serialnumber_ref = serialnumber_scan(request)

        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
        sn = request.POST['serial_number']

        sn_list = SerialNumber.objects.filter(serial_number=sn)

        Station = apps.get_model('line', 'Station')
        station_ref = Station.objects.filter(pk=station_id)
        station_ref = station_ref.first()    

        context = {
            'serialnumber_list': sn_list,
            'serial_number': serialnumber_ref,
            'repairdetail_list': RepairDetail.objects.order_by('-id'),
            'more_context': RepairDetail.objects.all(),
            'repairmain': RepairMain.objects.order_by('failure_sequence')[0],
            'testingresult': serialnumber_ref.testingresult_set.all(),
            'template': 'Repair',
            'route_id': route_id,
            'station_id': station_id,
            'model': model,
            'station_name': station_ref.pk,            
        }

        if repair_code_ref and repairmain_ref and in_part_no == out_part_no:
            repairmain_ref = repairmain_ref.first()
            repair_code_ref = repair_code_ref.first()
            repairdetail_ref = RepairDetail(failure_sequence=repairmain_ref,
                                            repaired_code=repair_code_ref,
                                            repaired_description=repaired_description,
                                            replacement=replacement,
                                            in_part_no=in_part_no,
                                            out_part_no=out_part_no,
                                            creator=creator,
                                            repaired_date=make_aware(datetime.now()),

                                            )

            try:
                repairdetail_ref.save()
                repairmain_ref.result = 1
                repairmain_ref.repaired_date = datetime.now()
                repairmain_ref.save()
                context.update({'success': 'success'})
            except:
                pass

            error = 'Repair code Does Not Exist'
            context = {
                'error': error,

            }

            context.update({'error': error})
            return render(request, template_name, context)
        else:
            error = 'Repair code Does Not Exist'

            if in_part_no != out_part_no:
                error = 'part number does not match'
            else:
                error = 'Repair code Does Not Exist'
            context.update({'error': error})
            return render(request, template_name, context)
    return render(request, template_name, context)

    # Get serial numbers for a workorder

def get_serial_numbers(request):
    if request.method == 'GET':
        wo = request.GET.get('workorder')
        workorder = WorkOrder.objects.filter(pk=wo)

        if workorder:
            workorder = workorder.first()

            serial_numbers = workorder.get_serial_numbers()

            data = []

            for sn in serial_numbers:
                data.append(sn.serial_number)

            return JsonResponse(data, safe=False)
        else:
            return HttpResponse("Workorder does not exist.")

        return redirect('manufacturing:label-create')


# class RepairStationDetail(LoginRequiredMixin, generic.DetailView):
class RepairStationDetailView(LoginRequiredMixin, generic.ListView):
    # permission_required = 'manufacturing.can_repair'
    SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
    model = SerialNumber
    context_object_name = 'serialnumber_list'
    template_name = 'production/repair/repair.html'
    fields = '__all__'

    def get_queryset(self):
        query = self.request.GET.get('sn')
        if not query:
            query = 'default value'

        object_list = SerialNumber.objects.filter(
            Q(serial_number__icontains=query)
        )

        return object_list

    def get_context_data(self, **kwargs):
        context = super(RepairStationDetailView, self).get_context_data(**kwargs)
        
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            

        context.update({
            'repairdetail_list': RepairDetail.objects.order_by('-id'),
            'repaircodeonly_list': RepairCode.objects.order_by('create_date'),
            'more_context': RepairDetail.objects.all(),
            'repaircode_context': RepairCode.objects.all(),

        })


        return context