from django.urls import path
from .views import *

app_name = 'qms'

urlpatterns = [
    # path('', views.QMSHomeView.as_view(), name='home'),
    path('inspection-tool/', InspectionListView.as_view(), name='inspection-tool'),
    path('inspection-tool/create', CreateInspectionToolView.as_view(), name='inspection-tool-create'),
    path('inspection-tool/update/<str:pk>/', UpdateInspectionToolView.as_view(), name='inspection-tool-update'),
    path('inspection-level/', InspectionLevelListView.as_view(), name='inspection-level'),
    path('inspection-level/create', CreateInspectionLevelView.as_view(), name='inspection-level-create'),
    path('inspection-level/update/<str:pk>/', UpdateInspectionLevelView.as_view(), name='inspection-level-update'),
    path('inspection-free/', MaterialInspectionFreeListView.as_view(), name='inspection-free'),
    path('inspection-free/create', CreateMaterialInspectionFreeView.as_view(), name='inspection-free-create'),
    path('inspection-free/update/<str:pk>/', UpdateMaterialInspectionFreeView.as_view(), name='inspection-free-update'),

    ############################
    path('inspection_manufacture_info/', views.ManufactureInfo.as_view(), name='inspection_manufacture_info'),
    path('inspection_mrb/', views.MRBauditInfo.as_view(), name='inspection_mrb'),
    path('inspection_waiting/', views.WaitingList.as_view(), name='inspection_waiting'),
    path('inspection_waiting/delete/<str:pk>/', views.WaitingListDelete.as_view(), name='waiting-list-delete'),



    # #### template only #######
    path('inspection/', views.inspection, name='inspection'),
    path('wms_receiving_form/', views.wms_receiving_form, name='wms_receiving_form'),

]