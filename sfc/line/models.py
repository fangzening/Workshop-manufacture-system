# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MinValueValidator

from django.db import models
from django.apps import apps
import uuid


# Create your models here.
class Route(models.Model):
    route_id = models.CharField(max_length=255,primary_key=True )
    # model = models.ForeignKey('manufacturing.MaterialMaster', on_delete=models.CASCADE, null=True, unique=True)
    prod_version = models.ForeignKey('Prod_Version', on_delete=models.SET_NULL, null=True, blank=True, unique=True)
    first_station = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, blank=True)
    plant_code = models.CharField(max_length=50)
    creator = models.CharField('Creator', max_length=20)
    create_date = models.DateTimeField('Create Date', auto_now=True)
    updater = models.CharField('Updater', max_length=20, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        return str(self.route_id)

    '''
    collect stations for WIP
    @return :list of stations 
            or 
            empty array
    '''

    def get_stations(self):
        station_list = []
        if self.first_station:
            station_list.append(self.first_station)

            stations = StationRoutes.objects.prefetch_related('station').filter(route=self).order_by('id')

            for station in stations:

                if station.next_station not in station_list and station.next_station != None:
                    station_list.append(station.next_station)

        return station_list


class StationRoutes(models.Model):
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE, related_name='station')
    next_station = models.ForeignKey('Station', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='next_station')
    repaired_station = models.ForeignKey('Station', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='repaired_station')


    STATE_CHOICES = (
        ('FAIL', 'FAIL'),
        ('PASS', 'PASS'),
    )
    state = models.CharField('State', choices=STATE_CHOICES,default='PASS',max_length=255)
    

    sequence = models.IntegerField()

    action_station = models.IntegerField(default=0)
    audit_station = models.IntegerField(default=0)

    def __str__(self):
        return 'From ' + str(self.station) + ' To ' + str(self.next_station) + ' For Route ' + str(self.route)

    # delete all station routes for a particular station in a route
    def remove_all_station_routes(self):
        station_routes = StationRoutes.objects.filter(route=self.route, station=self.station)
        for station_route in station_routes:
            station_route.remove_station_route()

    def remove_station_route(self):
        # delete current stationroute
        self.delete()

        # collect stationroutes to and from it
        stationroutes_to = StationRoutes.objects.filter(route=self.route, next_station=self.next_station)
        stationroutes_from = StationRoutes.objects.filter(route=self.route, station=self.next_station)

        # check if station is severed from route
        if not stationroutes_to and stationroutes_from:

            for stationroute in stationroutes_from:
                # remove stationroute to that next station
                stationroute.remove_station_route()


# class State(models.Model):
#     state = models.CharField(max_length=50)

#     def __str__(self):
#         return self.state


class Station(models.Model):
    station_id = models.CharField(max_length=255, primary_key=True)
    desc = models.TextField(max_length=1000)
    template_id = models.ForeignKey(
        'Template', db_column='template_id', on_delete=models.SET_NULL, null=True)
    model_partition = models.CharField(max_length=1, default='n')
    creator = models.CharField('Creator', max_length=20)
    create_date = models.DateTimeField('Create Date', auto_now=True)
    updater = models.CharField('Updater', max_length=20, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)
    station_type = models.IntegerField(null=True)
    

    def __str__(self):
        return self.station_id


    # might cause issue if station is used in multiple routes
    def get_rules(self):
        Rule = apps.get_model("rules", "Rule")
        rules = Rule.objects.filter(station=self)
        rule_set = []

        for r in rules:
            rule_set.append(r.material_group)

        return rule_set

    def get_scantypes(self):
        Rule = apps.get_model("rules", "Rule")
        rules = Rule.objects.filter(station=self)
        scan_types = []

        for r in rules:
            scan_types.append(r.scan_type)

        return scan_types


class Action(models.Model):
    action_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Template(models.Model):
    template_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=50)
    desc = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class TemplateActions(models.Model):
    row_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    template_id = models.ForeignKey(
        'Template', db_column='template_id', on_delete=models.CASCADE)
    action_id = models.ForeignKey(
        'Action', db_column='action_id', on_delete=models.CASCADE)


# class Pallet(models.Model):
#     TYPE_MEASURE = (
#         ('In', 'In'),
#         ('cm', 'cm'),

#     )
#     TYPE_WEIGHT = (
#         ('lbs', 'lbs'),
#         ('kg', 'kg'),

#     )
#     TYPE_STATUS = (
#         ('open', 'open'),
#         ('closed', 'closed')
#     )

#     height = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
#     length = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
#     width = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
#     dimensions_net = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)

#     unit = models.CharField(
#         max_length=15,
#         choices=TYPE_MEASURE,
#         default='In',
#         help_text='Height',
#     )

#     weight = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
#     weight_unit = models.CharField(
#         max_length=15,
#         choices=TYPE_WEIGHT,
#         default='lbs',
#         help_text='Weight',
#     )
#     status = models.CharField(
#         max_length=6,
#         choices=TYPE_STATUS,
#         default='open',
#         help_text='status',
#     )
#     pallet_config = models.ForeignKey('PalletConfiguration', null=True, on_delete=models.SET_NULL)
#     delivery_number = models.ForeignKey('DeliveryNumberHeader', blank=True, null=True, on_delete=models.SET_NULL)

#     def __str__(self):
#         return str(self.id)


# class PalletConfiguration(models.Model):
#     pack_limit = models.IntegerField(default=8, blank=True)
#     workorder_type = models.CharField(max_length=50)
#     pallet_mix = models.IntegerField(default=0)

#     def __str__(self):
#         return 'Pallet Config for ' + self.workorder_type

class Pack(models.Model):
    pack_id = models.CharField(max_length=100, primary_key=True)
    TYPE_PACK = (
        ('single', 'single'),
        ('multi', 'multi'),

    )
    pack_type = models.CharField(
        max_length=15,
        choices=TYPE_PACK,
        default='single',
        help_text='Pack Type',
    )
    status = models.CharField(max_length=50)
    print_label = models.CharField(max_length=50)
    country_kit = models.CharField(max_length=50)


class PackSerialNumber(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    serialnumber = models.ForeignKey('manufacturing.SerialNumber', on_delete=models.CASCADE)
    pack_id = models.ForeignKey('Pack', on_delete=models.CASCADE)
    updater = models.CharField('Updater', max_length=20, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

# class PalletPacks(models.Model):
#     pack = models.ForeignKey('Pack', on_delete=models.CASCADE)
#     pallet = models.ForeignKey('Pallet', on_delete=models.CASCADE)

# class DeliveryNumberHeader(models.Model):
#     sales_order = models.ForeignKey('shipping.SalesOrder', on_delete=models.SET_NULL, null=True)
#     delivery_number = models.CharField(max_length=255)
#     shipper_sequence = models.CharField(max_length=255)
#     date_shipped = models.DateField()
#     time_shipped = models.TimeField()
#     carrier = models.CharField(max_length=255)


# class DeliveryNumberDetail(models.Model):
#     delivery_number = models.ForeignKey('DeliveryNumberHeader', null=True, on_delete=models.SET_NULL)
#     cgn = models.CharField(max_length=255)
#     cgn_sequence = models.CharField(max_length=255)
#     part = models.CharField(max_length=255)
#     quantity = models.IntegerField()

class Prod_Version(models.Model):
    prod_version_id = models.CharField(max_length=255, primary_key=True)
    prod_version_description = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    create_date = models.DateField(null=False)

    def __str__(self):
        return str(self.prod_version_id)