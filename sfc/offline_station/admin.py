from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(PhantomAssy)
class AdminPhantomAssy(admin.ModelAdmin):
    list_display = ['phantom_serialnumber', 'phantom_partno',]
    list_filter = ['phantom_serialnumber', 'phantom_partno',]
