from django.contrib import admin
from .models import *
# # Register your models here.


@admin.register(Git)
class AdminGit(admin.ModelAdmin):
    list_display = ['serialnumber','po_no','asset_no_id']
    list_filter = ['serialnumber','po_no', 'asset_no_id']


admin.site.register(Config)
