from django.urls import path
from . import views

app_name = 'line'

urlpatterns = [

    path('route/stations/', views.station_route, name='stations'),
    path('route/stations/create', views.stationroute_create, name='create-sationroute'),
    path('route/stations/edit', views.stationroute_edit, name='station-route-edit'),
    path('stations/', views.all_stations, name='all-stations'),
    path('station/create', views.station_config, name='create-station'),
    path('station/edit/<str:station_id>/', views.station_edit, name='edit-station'),
    path('', views.wip_search, name='wip'),
    path('wip/', views.station_list, name='station-list'),
    path('route/', views.route_list, name='route'),
    path('route/create/', views.route_config, name='create-route'),
    path('wip/workflow/', views.wip_flow, name='flow'),
    path('wip/check-in/', views.check_in, name='check-in'),
    path('config/pack/', views.pack_config, name='pack'),
    path('config/pack/create/', views.create_pack_config, name='create-pack'),
    # path('config/pallet/', views.pallet_config, name='pallet'),
    # path('config/pallet/create/', views.create_pallet_config, name='create-pallet'),

    path('wip/repair/', views.RepairStationDetailView.as_view(), name='repair_station'),
    # path('wip/repair/result_update/<str:pk>/', views.TestingResultUpdate.as_view(), name='result_update'),
    # path('wip/repair_code/', views.RepairCodelView.as_view(), name='repair_code'),
    path('wip/workflow/replace-part', views.replace_part, name='replace-part'),
    path('wip/repair_update/', views.update_repair, name='update_repair'),
####### tool box #########
    # path('tool_box/state_list', views.StateListView.as_view(), name='state_list'),
    # path('tool_box/state_list/delete/<int:pk>/', views.StateDelete.as_view(), name='state_delete'),
    # path('tool_box/state_list/add_state/', views.StateAdd.as_view(), name='add_state'),
    # path('tool_box/state_list/edit/<int:pk>/', views.StateUpdate.as_view(), name='update_state_row'),

####### config ###########


]