from django.apps import apps
from django.shortcuts import render, redirect 
from ..helper.serialnumber_scan import serialnumber_scan
from ..helper.check_station import check_station
from ..helper.change_station import change_station
from ..helper.check_route import check_route

def check_mask(request):
        # serialnumber = data.get('serial_number')

        data = request.POST

        part_number = data.get('part')
        kp_serialnumber = data.get('kp_serialnumber')

        Mask = apps.get_model('maskconfig', 'Mask')
        Segment = apps.get_model('maskconfig', 'Segment')

        mask_ref = Mask.objects.filter(model_id=part_number)
        mask_ref = mask_ref.first()

        segments = False

        if mask_ref:
            segments = Segment.objects.filter(mask_id=mask_ref).order_by('position')

        segment_check = []
        
        message_relay = "Success"



        
        if segments:
            
            whole_length = 0
            for segment in segments:
                segment_check.append((segment.data_type, segment.length, segment.value))
                whole_length = whole_length + segment.length

            left_bound = 0
            right_bound = 0
            data = ""

            if whole_length != len(kp_serialnumber):
                message_relay = "Key Part Serial Number Doesn't Meet Mask Requirements.(length)"
                return message_relay

            for segment in segment_check:
                right_bound = right_bound + segment[1]

                chunk = kp_serialnumber[left_bound:right_bound]

                if len(chunk) == segment[1]:

                    if segment[0] == 'Hard Code':
                        if chunk != segment[2]:
                            message_relay = "Segment Of KeyPart Doesn't Match Mask Requirement.(Invalid Segment)"
                            return message_relay

                    elif segment[0] == 'Date':

                        if not chunk.isnumeric():
                            message_relay = "Segment Of KeyPart Doesn't Match Mask Requirement.(Invalid Segment)"
                            return message_relay

                    elif segment[0] == 'Numeric':

                        if not chunk.isnumeric():
                            message_relay = "Segment Of KeyPart Doesn't Match Mask Requirement.(Invalid Segment)"
                            return message_relay

                    elif segment[0] == 'Alpha Numeric':

                        if not chunk.isalnum():
                            message_relay = "Segment Of KeyPart Doesn't Match Mask Requirement.(Invalid Segment)"
                            return message_relay

                    elif segment[0] == 'Text':
                        if not chunk.isalpha():
                            message_relay = "Segment Of KeyPart Doesn't Match Mask Requirement.(Invalid Segment)"
                            return message_relay


                    elif segment[0] == 'Model':

                        if chunk != segment[2]:
                            message_relay = "Segment Of KeyPart Doesn't Match Mask Requirement.(Invalid Segment)"

                            return message_relay
                else:
                    message_relay = "Segment Of KeyPart Doesn't Match Mask Requirement.(Invalid Segment)"
                    return message_relay

                left_bound = right_bound
        else:
            message_relay = "Part Has No Mask."
            

        if not mask_ref:
            message_relay = 'Success'

        return message_relay
