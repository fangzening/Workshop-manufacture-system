from django.apps import apps


def serialnumber_scan(request):
    data = request.POST

    serial_number = data.get('serial_number')

    # response to return false or the sn reference
    response = False

    reference = None

    SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
    reference = SerialNumber.objects.filter(serial_number=serial_number)
    reference = reference.first()

    if reference != None:
        response = reference

    return response