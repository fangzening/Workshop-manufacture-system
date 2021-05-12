from django.urls import path
from . import views

app_name = 'maskconfig'

urlpatterns = [
    path('', views.MaskConfigListView.as_view(), name='home'),
    path('segments/', views.segment, name='segments'),
    path('segments/create', views.createsegment, name='create-segment'),
    path('segments/delete/<int:pk>/', views.DeleteSegment.as_view(), name='delete-segment'),
    path('segments/edit', views.edit_segment, name='edit-segment'),
    # path('create/', views.CreateMask.as_view(), name='create-mask'),
    path('create/', views.createmask, name='create-mask'),

]


urlpatterns += [
    path('row/create/', views.createmask_row, name='create-mask-row'),
    path('segments/row/create', views.createsegment_row, name='create-segment-row'),
    path('row/delete/<int:pk>/', views.MaskDelete.as_view(), name='delete-mask-row'),
    path('row/edit/<int:pk>/', views.MaskUpdate.as_view(), name='update-mask-row'),
    path('row/detail/<int:pk>/', views.MaskDetailView.as_view(), name='detail-mask-row'),
    path('row/segment/create', views.CreateSegment.as_view(), name='create-segment-row'),
    path('list', views.MaskConfigListView.as_view(), name='mask-list'),
    path('segments/list/', views.segment_template, name='segment-list'),
    path('reverse', views.MaskConfigListReverseView.as_view(), name='mask-list-reverse'),
    path('row/segment/edit/<int:pk>/', views.MaskSegmentUpdate.as_view(), name='update-masksegment-row'),
    path('list/segment/update/', views.SegmentListUpdate.as_view(), name='update-masksegment-list'),
    path('row/segment/update/<int:pk>/', views.MaskSegmentModalUpdate.as_view(), name='update-masksegment-modal'),
    path('row/segment/modal/update/', views.mask_modal_row, name='update-masksegment-modal-row'),
    path('mask/create/', views.MaterialMasterListView.as_view(), name='mask-create'),
    path('maskmanager/create/', views.MaskConfigCreateView.as_view(), name='maskmanager-create'),

    # ##### ooba ######
    path('ooba/list/', views.ooba_list_view, name='ooba_list'),
    path('ooba/create/', views.ooba_create_view, name='ooba_create'),


]
