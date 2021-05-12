from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(bs_inspection_tool)
admin.site.register(bs_inspection_free_list)
admin.site.register(bs_aql_value)
admin.site.register(iqc_maintenance)

@admin.register(bs_manufacture_data)
class AdminBS_MANUFACTURE_DATA(admin.ModelAdmin):
    list_display = ['manufacture_name','manufacture_part_no']
    list_filter = ['manufacture_name','manufacture_part_no']

@admin.register(mrb)
class AdminMRB(admin.ModelAdmin):
    list_display = ['mrb_form_id','mrb_result']
    list_filter = ['mrb_form_id','mrb_result']

@admin.register(insp_param_catalogue)
class AdminINSP_PARAM_CATALOUGUE(admin.ModelAdmin):
    list_display = ['inspect_parameters_id']
    list_filter = ['inspect_parameters_id']
#
@admin.register(iqc_inspection)
class AdminIQC_INSPECTION(admin.ModelAdmin):
    list_display = ['inspection_form_id']
    list_filter = ['inspection_form_id']

@admin.register(incoming_iqc_list)
class AdminINCOMING_IQC_LIST(admin.ModelAdmin):
    list_display = ['incoming_list_id','model_id']
    list_filter = ['incoming_list_id','model_id']

