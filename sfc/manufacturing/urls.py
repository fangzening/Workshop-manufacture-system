from django.urls import path
from . import views

app_name = 'manufacturing'
urlpatterns = [
    path('', views.home, name='home'),
    path('reset_confirm/', views.reset_confirm, name='reset_confirm'),

    path('label_center/', views.label_center, name='label_center'),
    path('label_center/get-serial-numbers', views.get_serial_numbers, name='get-sns-by-wo'),
    path('so_list/', views.so_list, name='so_list'),
    path('serialnumber_log/', views.serialnumber_log, name='serialnumber_log'),

# sidebar tabs ###########
    path('sidebar/sub_config/', views.sub_config, name='sub_config'),
    path('sidebar/sub_toolbox/', views.sub_toolbox, name='sub_toolbox'),
    path('sidebar/sub_wip/', views.sub_wip, name='sub_wip'),
    path('sidebar/sub_shipping_manager/', views.sub_shipping_manager, name='sub_shipping_manager'),
    path('sidebar/sub_qms/', views.sub_qms, name='sub_qms'),
    path('sidebar/sub_wms/', views.sub_wms, name='sub_wms'),

#### user profile ###############
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('add_profile/', views.user_add_profile, name='add_profile'),
    path('users/add_profiles/', views.UsersProfilesAdd.as_view(), name='users_add_profiles'),
    path('users/profiles_list/', views.UsersProfilesListView.as_view(), name='users_profiles_list'),
    path('users/profiles_delete/<int:pk>/', views.UsersProfilesDelete.as_view(), name='users_profile_delete'),
    path('users/profiles_update/<int:pk>/', views.UsersProfilesUpdate.as_view(), name='users_profiles_update'),
]

urlpatterns += [
    path('accounts/signup/', views.signup, name='signup'),
    path('signup/', views.signup_sidebar, name='signup_sidebar'),
    path('user/myprofile_detail/<int:pk>/', views.UserProfileListView.as_view(), name='profile_detail'),
    path('user/myprofile_edit/', views.update_profile, name='user_top_update'),
    path('password/', views.change_password, name='change_password'),
]

urlpatterns += [
    path('management/user/', views.UserListView.as_view(), name='user_list'),
    path('management/user-delete/<int:pk>/', views.UserDelete.as_view(), name='user-delete'),
    path('search/user/', views.SearchUserView.as_view(), name='search_user'),
    path('management/user-update/<int:pk>/', views.UserUpdate.as_view(), name='user-update'),
    path('management/user-update/profile/<int:pk>/', views.UsersSidebarProfilesUpdate.as_view(), name='users_profiles_update_sidebar'),
    path('users_update_profiles_view/<id>/', views.users_update_profiles_view, name='update_profiles_view'),
    path('profiles_detail_view/<id>/', views.profiles_detail_view, name='profiles_detail_view'),
    ##  permission #####
    path('management/user-add-permissions/<int:pk>/', views.UserAddPermissionUpdate.as_view(), name='add-permissions'),
    path('management/user-permissions/', views.UserListPermissionsView.as_view(), name='permissions'),
    ## group ##
     path('management/user-group/', views.CreateUserGroup.as_view(), name='user-group'),
     path('management/user-group-list/', views.UserGroupListView.as_view(), name='user_group_list'),
     path('management/user-group/update/<int:pk>/', views.UserGroupUpdate.as_view(), name='user_group_update'),
     path('management/user-group-delete/<int:pk>/', views.UserGroupDelete.as_view(), name='user-group-delete'),
]

urlpatterns += [
    path('wip/production-flow/test-station', views.SerialNumberTestForm.as_view(), name='production_flow_station'),
    path('tool_box/workorder_list', views.WorkOrderListView.as_view(), name='workorder_list'),
    path('tool_box/workorder_list_reverse', views.WorkOrderReverseListView.as_view(), name='workorder_list_reverse'),
    path('tool_box/workorder-detail/<int:pk>',views.WorkOrderDetailDetailView.as_view(), name='workorder-detail'),
    path('tool_box/workordermanager-wo-detail/<pk>', views.workorder_detail, name='workordermanager-wo-detail'),
    path('tool_box/workordermanager-sn-detail/<pk>', views.serialnumber_detail, name='workordermanager-sn-detail'),
    path('tool_box/workorder_list/status/<pk>/', views. WorkOrderEditUpdate.as_view(), name='workorder-status'),
    path('tool_box/label-center', views.label_center, name='label-center'),
    path('tool_box/search_by_sn', views.SearchResultsBySNView.as_view(), name='search_by_sn'),
    path('tool_box/search_by_wo', views.SearchResultsByWOView.as_view(), name='search_by_wo'),
    path('tool_box/label_create', views.label_create, name='label-create'),
    path('tool_box/serialnumber_list', views.SerialNumberListView.as_view(), name='serialnumber_list'),
    path('tool_box/serialnumber_list/edit/', views.serialnumber_update, name='serialnumber_update'),
    path('tool_box/serialnumber_detail/<str:pk>/', views.SNManagereDetail.as_view(), name='serialnumber_detail'),

    path('wip/serialnumber/detail/', views.SerialNumberDetail.as_view(), name='serialnumber-detail'),
    path('modalform/workorder/', views.WorkOrderIndex.as_view(), name='index-workorder'),
    path('wip/forms/last_button/', views.post_generate_sn, name='last_button'),
    path('master-list/', views.MaterialMasterListView.as_view(), name='master_list'),

]

urlpatterns += [
    path('tool_box/hold_station', views.hold_station, name='hold_station'),
    path('tool_box/UnHold/<str:hold_id>/', views.UnHold, name='UnHold'),
    path('tool_box/HoldEdit/<str:hold_id>/', views.HoldEdit, name='HoldEdit'),
    path('tool_box/HoldAdd', views.HoldAdd, name='HoldAdd'),
]