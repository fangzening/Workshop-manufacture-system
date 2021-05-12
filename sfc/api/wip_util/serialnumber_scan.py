from django.apps import apps

def serialnumber_scan(data):
        
    

    serial_number = data['serial_number']

    
    # response to return false or the sn reference
    response = False

    reference = None

    SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
    reference = SerialNumber.objects.filter(pk=serial_number)
    reference = reference.first()
    
    if reference != None:
        response = reference

    return response