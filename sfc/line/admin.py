# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Station)
admin.site.register(StationRoutes)
admin.site.register(Template)
admin.site.register(TemplateActions)

admin.site.register(Route)
# admin.site.register(Pallet)
admin.site.register(Action)
admin.site.register(Pack)
admin.site.register(PackSerialNumber)
admin.site.register(Prod_Version)
# admin.site.register(PalletConfiguration)
# admin.site.register(PalletPacks)




