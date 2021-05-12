from django.shortcuts import render, redirect
from django.apps import apps
from .models import *


def rules(request):
    template_name = 'rules.html'

    def get(request):

        data = request.GET
        route_id = data.get('route_id')
        station_id = data.get('station')

        Route = apps.get_model('line', 'Route')

        Station = apps.get_model('line', 'Station')

        station_ref = Station.objects.filter(pk=station_id)
        route_ref = Route.objects.filter(pk=route_id)
        rules = None

        context = {
            'route': route_id,
            'station': station_id
        }

        if route_ref and station_ref:
            station_ref = station_ref.first()
            route_ref = route_ref.first()

            rules = Rule.objects.filter(route=route_ref, station=station_ref)

        if rules:
            context['rules'] = rules

        return render(request, template_name, context)

    def post(request):
        data = request.POST

        rule_id = int(data.get('rule') or -1)
        route_id = data.get('route')
        station_id = data.get('station')

        Rule.objects.filter(id=rule_id).delete()

        # needs to be changed if urls change
        response = redirect('rules:rules')
        response['Location'] += '?station=' + str(station_id) + '&route_id=' + str(route_id)
        return response

    if request.method == 'GET':
        return get(request)
    else:
        if request.POST.get('action') == 'delete':
            return post(request)


def create_rule(request):
    template_name = 'createrule.html'
    Route = apps.get_model('line', 'Route')
    WorkOrderDetail = apps.get_model("manufacturing", "WorkOrderDetail")

    def get(request):

        # get materials
        MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')

        data = request.GET
        route_id = data.get('route')
        station_id = data.get('station')
        # collect material groups

        context = {

            'route': route_id,
            'station': station_id

        }

        route_ref = Route.objects.filter(pk=route_id)

        material_groups = []

        if route_ref:
            route_ref = route_ref.first()

            materials = MaterialMaster.objects.all()

            for material in materials:
                group = material.keypart_group
                if not group in material_groups and len(group) > 0:
                    material_groups.append(group)

            context['material_groups'] = material_groups

        return render(request, template_name, context)

    def post(request):
        data = request.POST
        route_id = data.get('route')
        station_id = data.get('station')
        material_group = data.get('material_group')
        scan_type = data.get('scan_type')
        # get references
        Route = apps.get_model('line', 'Route')

        Station = apps.get_model('line', 'Station')

        MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')

        # collect material groups to validate input

        route_ref = Route.objects.filter(pk=route_id)

        material_groups = []

        if route_ref:
            route_ref = route_ref.first()

            materials = MaterialMaster.objects.all()

            for material in materials:
                group = material.keypart_group
                if not group in material_groups and len(group) > 0:
                    material_groups.append(group)

        # get refs to station/route
        station_ref = Station.objects.filter(pk=station_id)

        # check if material group exists
        valid_group = False
        if material_group in material_groups:
            valid_group = True

        if station_ref and route_ref and valid_group:
            station_ref = station_ref.first()


            # check if rule exists
            rule_check = Rule.objects.filter(material_group=material_group, station=station_ref, route=route_ref)
            stop = False
            if not rule_check:
                my_rule = Rule(material_group=material_group, station=station_ref, route=route_ref, scan_type=scan_type)
                my_rule.clean()
                my_rule.save()

        response = redirect('rules:rules')
        response['Location'] += '?station=' + str(station_id) + '&route_id=' + str(route_id)
        return response

    if request.method == 'GET':
        return get(request)
    else:
        return post(request)

