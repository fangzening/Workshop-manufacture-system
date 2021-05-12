from django.apps import apps

def scan_keypart(request):
        data = request.POST
        serial_number = data.get('serial_number')
        part_number = data.get('part')

        KeyPart = apps.get_model('manufacturing', 'KeyPart')

        SerialNumber = apps.get_model('manufacturing', 'SerialNumber')

        serial_number_ref = SerialNumber.objects.filter(pk=serial_number)
        serial_number_ref = serial_number_ref.first()

        # response to return false or the sn reference
        reference = None
        response = None
        if serial_number_ref:
            MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')

            part_ref = MaterialMaster.objects.filter(pk=part_number)
            part_ref = part_ref.first()

            reference = KeyPart.objects.filter(sn=serial_number_ref,
                                               part=part_ref
                                               )
            reference = reference.first()

        if reference != None:
            response = reference

        
        return response
