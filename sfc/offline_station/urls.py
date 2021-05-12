from django.urls import path
from . import views

app_name = 'offline_station'

urlpatterns = [
    path('' , views.phantom_data_input, name='offline_station')

]
