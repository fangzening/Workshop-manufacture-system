from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
from django.urls import reverse
import random
import string
from datetime import datetime, date
from django.apps import apps


class Segment(models.Model):
    row_id = models.AutoField(auto_created=True, primary_key=True)
    mask_id = models.ForeignKey('Mask', on_delete=models.CASCADE, null=True, db_column='mask_id')
    create_date = models.DateTimeField(auto_now=True)

    ######## editable ###########
    name = models.CharField(max_length=30)
    action = models.CharField(max_length=200)
    position = models.IntegerField(validators=[
        MinValueValidator(0),

    ]
    )
    ####### editable ###########

    TYPE_OF = (
        ('Hard Code', 'Hard Code'),
        ('Day', 'Day'),
        ('Week', 'Week'),
        ('Month', 'Month'),
        ('Year', 'Year'),
        ('Numeric', 'Numeric'),
        ('Alpha Numeric', 'Alpha Numeric'),
        ('Text', 'Text'),
        ('Model', 'Model')
    )

    data_type = models.CharField(
        max_length=20,
        choices=TYPE_OF,
        help_text='Type of data segment'
    )
    length = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(20)], null=True)
    value = models.CharField(max_length=15, null=True, blank=True)
    creator = models.CharField('Creator', max_length=20)
    create_date = models.DateTimeField('Create Date', auto_now=True)
    updater = models.CharField('Updater', max_length=20, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    # def __str__(self):
    #     return 'Model: ' + self.model.model + ' position ' + str(self.position)
    def get_absolute_url(self):
        """Returns the url to access a detail record """
        # return reverse('maskconfig:update-mask-row', args=[str(self.id)])
        return reverse('maskconfig:home')

    def __str__(self):
        return self.mask_id.model.model_id + ' Segment ' + str(self.position)

class Mask(models.Model):
    mask_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    model = models.ForeignKey('manufacturing.MaterialMaster',on_delete=models.SET_NULL, null=True)
    
    action = models.CharField(max_length=200)

    creator = models.CharField('Creator', max_length=20)
    create_date = models.DateTimeField('Create Date', auto_now=True)
    updater = models.CharField('Updater', max_length=20, null=True, blank=True)
    update_date = models.DateTimeField('Update Date', null=True, blank=True)

    def __str__(self):
        return self.model.model_id + ' Config'

    # ###### 2/25 ####
    def get_absolute_url(self):
        """Returns the url to access a detail record """
        # return reverse('maskconfig:update-mask-row', args=[str(self.id)])

        return reverse('maskconfig:home')

    def get_sequence(self, segments, serial_number):
        
        reset = False
        new_segment = ''
        # check week
        date_ref = date(datetime.now().year,
                        datetime.now().month,
                        datetime.now().day).isocalendar()

        week = date_ref[1]        
        
        if serial_number:
            serial_number = serial_number.serial_number

        if segments:
            index = 0
            segment = None

            for seg in segments:
                
                if seg.data_type == 'Week':
                    segment = seg
                    break
                else:
                    index += seg.length

            if segment:
                right_bound = index + segment.length

                if serial_number:

                    chunk = serial_number[index:right_bound]
                    # check if
                    if chunk.isnumeric():

                        chunk = int(chunk)
                        
                        if chunk == week:
                            pass
                        else:

                            segment = None
                            for seg in segments:
                                if seg.data_type == 'Numeric':
                                    segment = seg


                            for x in range(0, segment.length):
                                if x == segment.length-1:
                                    new_segment = new_segment + "1"
                                else:
                                    new_segment = new_segment + "0"

                            reset = True



        if segments and not reset:

            index = 0
            segment = None

            found = False

            for seg in segments:

                if seg.data_type == 'Numeric':

                    segment = seg
                    found = True


                elif found == False:

                    index += seg.length

            right_bound = 0

            if segment:
                right_bound = index + segment.length


                if serial_number:

                    chunk = serial_number[index:right_bound]

                    # check if
                    if chunk.isnumeric():

                        chunk = int(chunk)
                        chunk += 1

                        chunk = str(chunk)
                        if (len(chunk) > segment.length):
                            return ''
                        valid = False

                        # pad 0's until valid length
                        # will change later when rules are applied
                        while not valid:

                            if len(chunk) == segment.length:

                                valid = True
                            else:
                                chunk = '0' + chunk

                    new_segment = chunk
                else:

                    for i in range(segment.length):
                        new_segment += '0'

                
        return new_segment



    def generate_sn(self):
        
        
        segment_list = Segment.objects.filter(mask_id=self).order_by('position')
        if segment_list:
            segments = segment_list.values('row_id','position', 'length', 'value', 'data_type')
            segment_list = [entry for entry in segments] 

            serial_number = ''
            pattern = ''
            for segment in segment_list:

                if segment['data_type'] == 'Hard Code':
                    serial_number = str(serial_number + str(segment['value']))

                    # pattern

                    pattern = str(pattern + str(segment['value']))
                elif segment['data_type'] == 'Day':

                    pattern_symbol = 'D'

                    day = datetime.now().day

                    if day > 10:
                        day = '0' + str(day)
                    else:
                        day = str(day)

                    day = day[0:segment['length']]
                    serial_number = str(serial_number + day)

                    for i in range(len(day)):
                        pattern = str(pattern + pattern_symbol)

                elif segment['data_type'] == 'Week':

                    pattern_symbol = 'W'

                    date_ref = date(datetime.now().year,
                                    datetime.now().month,
                                    datetime.now().day).isocalendar()

                    week = date_ref[1]

                    if week < 10:
                        week = '0' + str(week)
                    else:
                        week = str(week)

                    week = week[0:segment['length']]
                    serial_number = str(serial_number + week)

                    for i in range(len(week)):
                        pattern = str(pattern + pattern_symbol)

                elif segment['data_type'] == 'Month':

                    pattern_symbol = 'M'

                    month = datetime.now().month

                    if month > 10:
                        month = '0' + str(month)
                    else:
                        month = str(month)

                    month = month[0:segment['length']]
                    serial_number = str(serial_number + month)

                    for i in range(len(month)):
                        pattern = str(pattern + pattern_symbol)

                elif segment['data_type'] == 'Year':

                    pattern_symbol = 'Y'

                    year = datetime.now().year

                    year = str(year)

                    if segment['length'] == len(year):
                        year = year
                    else:

                        year = year[-1:((len(year) - 1) - segment['length']):-1]

                        year = year[-1::-1]

                    serial_number = str(serial_number + year)

                    for i in range(len(year)):
                        pattern = str(pattern + pattern_symbol)

                elif segment['data_type'] == 'Numeric':
                    

                    SerialNumber = apps.get_model('manufacturing', 'SerialNumber')

                    seg_list = Segment.objects.filter(mask_id=self.mask_id).order_by('position')

                    MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')

                    material_ref = MaterialMaster.objects.filter(pk=self.model)
                    # get latest created
                    if (material_ref):
                        material_ref = material_ref.first()

                        sn_list = SerialNumber.objects.filter(model_id=material_ref)

                        latest_sn = None
                        # find lates
                        for sn in sn_list:

                            if latest_sn == None:
                                latest_sn = sn
                            else:
                                if latest_sn.generated_date < sn.generated_date:
                                    latest_sn = sn
                        print("preseq")
                        sequence = self.get_sequence(seg_list, latest_sn)
                        print(sequence)
                        if sequence == '':
                            return '', ''
                        else:
                            serial_number += str(sequence)
                           

                    pattern_symbol = '#'
                    
                    for index in range(segment['length']):
                        pattern = str(pattern + pattern_symbol)

                elif segment['data_type'] == 'Alpha Numeric':

                    pattern = str(pattern + 'A-9' + '(' + str(segment['length']) + ')')

                    for index in range(segment['length']):
                        random_number = random.randint(0, 1)
                        if random_number == 1:
                            serial_number = str(serial_number + random.choice(string.ascii_uppercase))
                        else:
                            serial_number = str(serial_number + str(random.randint(0, 9)))

                elif segment['data_type'] == 'Text':
                    pattern_symbol = 'A'

                    for index in range(segment['length']):
                        pattern = str(pattern + pattern_symbol)
                        serial_number = str(serial_number + random.choice(string.ascii_uppercase))

                elif segment['data_type'] == 'Model':
                    # into mask creation hard set model instead of 5000000 lookups
                    # iterate current qty ALSO MAKE SURE NUMBER ENTERED DOESN'T EXCEED MAX CURR/MAXQTY
                    pattern = str(pattern + str(segment['value']))
                    serial_number = str(serial_number + str(segment['value']))

            return (serial_number, pattern)
        else:
            return ''


