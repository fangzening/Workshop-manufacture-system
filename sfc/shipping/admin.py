from django.contrib import admin

# Register your models here.
from .models import Pallet, PalletSerialNumber
from .models import *
admin.site.register(SalesOrder)
# admin.site.register(SalesOrderDetail)
admin.site.register(SalesOrderShipInfo)
admin.site.register(SalesOrderReturnInfo)
admin.site.register(PalletDnLog)
# admin.site.register(PalletDeliveryNumber)
# admin.site.register(DeliveryNumber)
# admin.site.register(DeliveryNumberDetail)

@admin.register(PalletDeliveryNumber)
class AdminPalletDeliveryNumber(admin.ModelAdmin):
    list_display = ['deliverynumber_id','pallet_id']
    list_filter = ['deliverynumber_id','pallet_id']

@admin.register(DeliveryNumber)
class AdminDeliveryNumber(admin.ModelAdmin):
    list_display = ['salesorder_id','deliverynumber_id',]
    list_filter = ['salesorder_id','deliverynumber_id',]

@admin.register(DeliveryNumberDetail)
class AdminDeliveryNumberDetail(admin.ModelAdmin):
    list_display = ['deliverynumber_id','skuno','current_qty','salesorder_id',]
    list_filter = ['deliverynumber_id','skuno','current_qty', 'salesorder_id',]

@admin.register(SalesOrderDetail)
class AdminSalesOrderDetail(admin.ModelAdmin):
    list_display = ['salesorder_id','skuno', 'salesorder_qty']
    list_filter = ['salesorder_id', 'skuno', 'salesorder_qty']

@admin.register(Pallet)
class AdminPallet(admin.ModelAdmin):
    list_display = ['pallet_id','status',]
    list_filter = ['pallet_id', 'status', ]

@admin.register(PalletSerialNumber)
class AdminPalletSerialNumber(admin.ModelAdmin):
    list_display = ['pallet_id','serialnumber',]
    list_filter = ['pallet_id','serialnumber' ]
