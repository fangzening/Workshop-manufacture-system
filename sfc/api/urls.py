from django.urls import path, include
from . import views

app_name = 'api'

urlpatterns = [
    path('checkssn', views.checkssn, name='checkssn'),
    path('scankeypart', views.scankeypart, name='scankeypart'),
    path('testssn', views.testssn, name='testssn'),
    path('checkkeypart', views.checkkeypart, name='checkkeypart'),
    path('getpart', views.getpart, name='getpart'),
    path('get-delivery-number', views.getDeliveryNumber, name = 'getDeliveryNumber'),

]   