from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(WorkOrder)
admin.site.register(WorkOrderDetail)
# admin.site.register(SerialNumber)
admin.site.register(MaterialMaster)
# admin.site.register(KeyPart)
admin.site.register(SerialNumberLog)
admin.site.register(Profile)
admin.site.register(WoStatusCategory)
admin.site.register(Bom)


admin.site.register(FailureCategory)
admin.site.register(FailureGroup)
admin.site.register(FailureCode)
admin.site.register(RepairCode)
admin.site.register(RepairGroup)



@admin.register(SerialNumber)
class AdminSerialNumber(admin.ModelAdmin):
    list_display = ['serial_number','model_id',]
    list_filter = ['serial_number','model_id', ]

@admin.register(TestingResult)
class AdminTestingResult(admin.ModelAdmin):
    list_display = ['serial_number','result','station',]
    list_filter = ['serial_number', ]

@admin.register(RepairMain)
class AdminRepairMain(admin.ModelAdmin):
    list_display = ['serial_number','station']
    list_filter = ['serial_number', 'station']

@admin.register(RepairDetail)
class AdminRepairDetail(admin.ModelAdmin):
    list_display = ['repaired_code',]
    list_filter = ['repaired_code', ]

@admin.register(KeyPart)
class AdminKeyPart(admin.ModelAdmin):
    list_display = ['model_id','serialnumber','cserialnumber']
    list_filter = ['serialnumber', 'model_id','cserialnumber']

@admin.register(SerializationRule)
class AdminSerializationRule(admin.ModelAdmin):
    list_display = ['rule_type','current_sequence']
    list_filter = ['rule_type','current_sequence']

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from manufacturing.models import Profile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(SN_Status_Category)

from django.contrib.auth.models import Permission
admin.site.register(Permission)
