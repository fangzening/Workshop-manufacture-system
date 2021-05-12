from django.urls import path, include
from . import views
from django.urls import path
from .views import *

app_name = 'wms'

urlpatterns = [
    # path('', views.QMSHomeView.as_view(), name='home'),
    path('wmsform/', views.wms_form, name='wms-form'),
    path('query/', views.query_click_button, name='query-wms'),
    path('wms_receiving_form/', views.wms_receiving_form, name='wms_receiving_form'),
]
