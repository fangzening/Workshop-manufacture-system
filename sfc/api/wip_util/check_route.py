from django.apps import apps
from .serialnumber_scan import serialnumber_scan


def check_route(request):
        # may rewrite the sql query
        data = request.POST

        response = False
        myroute = data.get('route')

        
        Route = apps.get_model('line', 'Route')

        
        serial_number_ref = serialnumber_scan(request)

        if serial_number_ref:
            if myroute:
                route_ref = Route.objects.filter(pk=myroute)
                route_ref = route_ref.first()

            if str(serial_number_ref.workorder_id.production_version) == str(route_ref.prod_version):
                response = True

        return response