from django.urls import path
from . import views

app_name = 'shipping'

urlpatterns = [
    ######################### palletization #############################################
    path('wip/palletize/', views.PalletStationDetailView.as_view(), name='pallet_station'),
    path('wip/palletize/add_sn/', views.add_sn_view, name='pallet_add_sn'),
    path('wip/palletize/delete/<str:pk>/', views.PalletDetail.as_view(), name='pallet_detail_delete'),
    path('wip/palletize/delete/<str:pk>', views.delete_sn_view, name='delete_sn'),
    path('wip/palletize/save_dimension/', views.save_dimension, name='save_dimension'),
    path('wip/palletize/save_dimension/<str:pk>/', views.PalletDetail.as_view(), name='after_save_dimensions'),
    path('wip/palletize/create_new_pallet/', views.create_new_pallet, name='create_new_pallet'),
    path('wip/palletize/create_new_pallet/<str:pk>/', views.PalletDetail.as_view(), name='after_create_new'),

    path('wip/palletize/validate-sn/', views.validate_sn_json, name='validate_sn_json'),
    path('wip/palletize/delete-sn/', views.delete_sn_json, name='delete_sn_json'),
    path('wip/palletize/add-sn/', views.add_sn_json, name='add_sn_json'),

    path('wip/palletize/add/', views.add_sn_test_view, name='add_sn_to_pallet'),
    path('wip/palletize/add/<str:pk>', views.PalletDetail.as_view(), name='pallet_detail'),
    path('wip/palletize/create_new_pallet_id/', views.create_pallet_id, name='create_new_pallet_id'),
   # path('wip/palletize/create_new_pallet_id/<str:pk>/', views.PalletDetail.as_view(), name='after_create_new_id'),

    # #######################  ship out ###########################################
    path('wip/ship_out/', views.SalesOrderEnterView.as_view(), name='ship_out_station'),
    path('wip/ship_out/success/', views.SalesOrderSuccessView.as_view(), name='ship_out_success'),
    path('wip/ship_out/detail/<str:pk>/', views.SalesDetail.as_view(), name='ship_out_detail'),
    path('wip/shipout/process/', views.Process, name='process'),
    path('wip/shipout/validate_sn/', views.ValidateSN, name='validate_sn'),
    path('wip/shipout/validate_sku/', views.ValidateSKU, name='validate_sku'),

    # ####################### truck load #############################################
    path('wip/truckload/', views.TruckLoadView.as_view(), name='truckload_station'),
    path('wip/truckload/getpallet/', views.get_pallets_by_dn, name='get_pallet'),
    path('wip/truckload/savetruckload/', views.SaveTruckLoad, name='save_truck'),

    # ####################### salesorder #############################################
    path('tool_box/salesorder_list/', views.SalesOrderListView.as_view(), name='salesorder_list'),
    path('tool_box/salesorder_list/detail/<int:pk>/', views.SalesOrderDetailView.as_view(), name='salesorder_detail'),

    # ####################### deliverynumber #############################################
    path('tool_box/deliverynumber_list/', views.DeliveryNumberListView.as_view(), name='deliverynumber_list'),
    path('tool_box/deliverynumber_list/detail/<str:pk>/', views.DeliveryNumberDetailView.as_view(), name='deliverynumber_detail'),


    path('wip/unpalletize/', views.UNPalletStationDetailView.as_view(), name='unpallet_station'),
    path('wip/unpalletize/detail/<str:pk>', views.UNPalletDetail.as_view(), name='unpallet_detail'),


    path('pallet-printer', views.PalletTemplateForm.as_view(), name="print_pallet_list"),


    ]
