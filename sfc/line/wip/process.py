from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# import your template handlers here
from .start.start import start
from .assembly.assembly import assembly
from .test.test import test
from .complete.complete import complete
from .repair.repair import repair
# from .pack.pack import pack
from .palletize.palletize import palletize
from .pack.pack import pack
from .helper.check_route import check_route
from .helper.check_station import check_station


@login_required
def process(request):
    data = request.POST
    template = data.get('template')

    if template == 'Start':
        return start(request)

    elif template == 'KeyPart':
        return assembly(request)

    elif template == 'Test':
        return test(request)

    elif template == 'Complete':
        return complete(request)

    elif template == 'Palletize':
        return palletize(request)

    elif template == 'Pack':
        return pack(request)

    elif template == 'Repair':
        return repair(request)

    else:
        return redirect('line:wip')


'''
check station
check route
change status
'''


# permanent checks
def run_checks(request):
    response = True
    message = ''
    if not check_route(request):
        message = message + 'Incorrect route '
        response = False
    if not check_station(request):
        message = message + 'Incorrect station '

    return (response, message)