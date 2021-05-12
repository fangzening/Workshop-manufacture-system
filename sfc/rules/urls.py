from django.urls import path
from . import views

app_name = 'rules'

urlpatterns = [

    path('route/stations/rules/create/', views.create_rule, name='create-rule'),
    path('route/stations/rules/', views.rules, name='rules'),

]