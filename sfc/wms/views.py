from django.db import connection
from django.urls import reverse_lazy
from django.views import View, generic
from django.http import JsonResponse, HttpResponseRedirect
from django.apps import apps
from django.shortcuts import render, redirect, reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from Internal.data import DataLayer
from rest_framework.reverse import reverse
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

def wms_form(request):
    return render(request, 'wms_receiving_form.html', {})


@api_view(['GET'])
def query_click_button(request):
    return render(request, 'query-wms.html', {})


@api_view(['GET'])
def query(request):
    if request.method == 'GET':
        try:
            data = request.data
        except Exception as error:
            print(error)
            response = {
                'status': '400',
                'message': 'Provide proper value for PO'
            }
    if 'po' in data:
        po = data['po']
        wms_detail = receiving_form.objects.filter(po_no=po)

        print('printing wms detail:', wms_detail)


@login_required
def wms_receiving_form(request):
    return render(request, 'wms_receiving_form/wms_receiving_form.html')
