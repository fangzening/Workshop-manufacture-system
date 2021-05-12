import json
import urllib

from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from requests import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . import views


# Create your views here.


class InspectionListView(LoginRequiredMixin, View):
    template_name = 'inspection-tool.html'
    model = bs_inspection_tool

    def get(self, request):
        query = self.model.objects.all()
        context = {
            'inspectiontools': query
        }
        return render(request, self.template_name, context)

    def delete(self, request):
        data = request.POST

        if data.get('inspection_id'):
            self.model.objects.filter(pk=data.get('inspection_id')).delete()
        return self.get(request)

    def dispatch(self, request):

        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            data = request.POST
            if data.get('action'):
                if data.get('action') == 'post':
                    return self.post(request)
                if data.get('action') == 'update':
                    return self.update(request)
                if data.get('action') == 'delete':
                    return self.delete(request)
            else:
                return self.get(request)


class CreateInspectionToolView(LoginRequiredMixin, CreateView):
    model = bs_inspection_tool
    template_name = 'create-tool.html'
    fields = ('inspection_tool',)
    success_url = reverse_lazy('qms:inspection-tool')

    def post(self, request):
        try:
            entry = self.model(inspection_tool=request.POST.get('inspection_tool'), creator=str(request.user))
            entry.save()
        except Exception as e:
            print(e)
            return redirect('qms:inspection-tool-create')

        return HttpResponseRedirect(self.success_url)

    # def get_context_data(self, **kwargs):
    #     context = super(CreateMaskView, self).get_context_data(**kwargs)
    #     context.update({
    #         'materialmaster_list': MaterialMaster.objects.order_by('model_id'),
    #         'more_context': MaterialMaster.objects.all(),
    #     })
    #     return context


class UpdateInspectionToolView(LoginRequiredMixin, UpdateView):
    model = bs_inspection_tool
    template_name = 'create-tool.html'
    fields = ('inspection_tool',)
    success_url = reverse_lazy('qms:inspection-tool')

    def get(self, request, pk):
        return self.post(request, pk)

    def post(self, request, pk):

        if request.POST.get('action') == 'update':

            entry = self.model.objects.filter(pk=pk)

            if entry and request.POST.get('inspection_tool'):

                try:
                    entry = entry.first()
                    entry.inspection_tool = request.POST.get('inspection_tool')
                    entry.creator = str(request.user)
                    entry.save()
                except Exception as e:
                    print(e)
                    success_flag = False

            return HttpResponseRedirect(self.success_url)

        query = self.model.objects.filter(pk=pk)

        if query:
            context = {
                'tool': query.first()
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(self.success_url)


class InspectionLevelListView(LoginRequiredMixin, View):
    template_name = 'inspection-level.html'
    model = bs_inspection_level

    def get(self, request):
        query = self.model.objects.all()
        context = {
            'inspectionlevels': query
        }
        return render(request, self.template_name, context)

    def delete(self, request):
        data = request.POST

        if data.get('inspection_id'):
            self.model.objects.filter(pk=data.get('inspection_id')).delete()
        return self.get(request)

    def dispatch(self, request):

        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            data = request.POST
            if data.get('action'):
                if data.get('action') == 'post':
                    return self.post(request)
                if data.get('action') == 'update':
                    return self.update(request)
                if data.get('action') == 'delete':
                    return self.delete(request)
            else:
                return self.get(request)


class CreateInspectionLevelView(LoginRequiredMixin, CreateView):
    model = bs_inspection_level
    template_name = 'create-level.html'
    fields = ('inspection_level',)
    success_url = reverse_lazy('qms:inspection-level')

    def post(self, request):
        try:
            entry = self.model(inspection_level=request.POST.get('inspection_level'), creator=str(request.user))
            entry.save()
        except Exception as e:
            print(e)
            return redirect('qms:inspection-level-create')

        return HttpResponseRedirect(self.success_url)


class UpdateInspectionLevelView(LoginRequiredMixin, UpdateView):
    model = bs_inspection_level
    template_name = 'create-level.html'
    fields = ('inspection_level',)
    success_url = reverse_lazy('qms:inspection-level')

    def get_context_data(self, **kwargs):
        context = super(UpdateInspectionLevelView, self).get_context_data(**kwargs)
        entry = self.model.objects.filter(pk=self.request.POST['inspection_id'])

        if entry:
            context.update({
                'inspectionlevel': entry.first()

            })
        return context

    def get(self, request, pk):
        return self.post(request, pk)

    def post(self, request, pk):

        if request.POST.get('action') == 'update':

            entry = self.model.objects.filter(pk=pk)

            if entry and request.POST.get('inspection_level'):

                try:
                    entry = entry.first()
                    entry.inspection_level = request.POST.get('inspection_level')
                    entry.creator = str(request.user)
                    entry.save()
                except Exception as e:
                    print(e)

            return HttpResponseRedirect(self.success_url)

        query = self.model.objects.filter(pk=pk)

        if query:
            context = {
                'level': query.first()
            }
            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(self.success_url)


class MaterialInspectionFreeListView(LoginRequiredMixin, View):
    template_name = 'inspection-free.html'
    model = bs_inspection_free_list

    def get(self, request):
        query = self.model.objects.all()
        context = {
            'inspectionfree': query
        }
        return render(request, self.template_name, context)

    def delete(self, request):
        data = request.POST

        if data.get('inspection_free_id'):
            self.model.objects.filter(pk=data.get('inspection_free_id')).delete()
        return self.get(request)

    def dispatch(self, request):

        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            data = request.POST
            if data.get('action'):
                if data.get('action') == 'post':
                    return self.post(request)
                if data.get('action') == 'update':
                    return self.update(request)
                if data.get('action') == 'delete':
                    return self.delete(request)
            else:
                return self.get(request)


class CreateMaterialInspectionFreeView(LoginRequiredMixin, CreateView):
    model = bs_inspection_free_list
    manufacture_model = bs_manufacture_data
    hon_hai_model = apps.get_model('manufacturing', 'MaterialMaster')
    template_name = 'create-inspection-free.html'
    fields = ('manufacture_id', 'model_id')
    success_url = reverse_lazy('qms:inspection-free')

    def get_context_data(self, **kwargs):

        context = super(CreateMaterialInspectionFreeView, self).get_context_data(**kwargs)
        materialmasters = self.hon_hai_model.objects.all()
        manufacturing_materials = self.manufacture_model.objects.all()

        context.update({
            'material_masters': materialmasters,
            'manufacturing_materials': manufacturing_materials
        })
        return context

    def post(self, request):

        try:

            hon_hai = self.hon_hai_model.objects.get(pk=request.POST.get('model'))

            manufacturer = self.manufacture_model.objects.get(
                manufacture_part_no=request.POST.get('material_manufacture_data'))

            entry = self.model(manufacture_id=manufacturer,
                               model_id=hon_hai,
                               creator=str(request.user))
            entry.save()
        except Exception as e:
            print(e)
            return redirect('qms:inspection-free-create')

        return HttpResponseRedirect(self.success_url)


class UpdateMaterialInspectionFreeView(LoginRequiredMixin, UpdateView):
    model = bs_inspection_free_list
    manufacture_model = bs_manufacture_data
    hon_hai_model = apps.get_model('manufacturing', 'MaterialMaster')
    template_name = 'create-inspection-free.html'
    fields = ('manufacture_id', 'model_id')
    success_url = reverse_lazy('qms:inspection-free')

    def get(self, request, pk):
        return self.post(request, pk)

    def post(self, request, pk):

        if request.POST.get('action') == 'update':

            entry = self.model.objects.filter(pk=pk)

            if entry and request.POST.get('material_manufacture_data') and request.POST.get('model'):

                try:
                    hon_hai = self.hon_hai_model.objects.get(pk=request.POST.get('model'))

                    manufacturer = self.manufacture_model.objects.get(
                        manufacture_part_no=request.POST.get('material_manufacture_data'))
                    entry = entry.first()
                    entry.manufacture_id = manufacturer
                    entry.model_id = hon_hai
                    entry.creator = str(request.user)
                    entry.save()
                except Exception as e:
                    print(e)

            return HttpResponseRedirect(self.success_url)

        query = self.model.objects.filter(pk=pk)

        if query:
            materialmasters = self.hon_hai_model.objects.all()
            manufacturing_materials = self.manufacture_model.objects.all()

            context = {
                'material_masters': materialmasters,
                'manufacturing_materials': manufacturing_materials,
                'inspectionfree': query.first()
            }

            return render(request, self.template_name, context)
        else:
            return HttpResponseRedirect(self.success_url)


class ManufactureInfo(LoginRequiredMixin, generic.ListView):
    model = bs_manufacture_data
    context_object_name = 'manufacture_list'
    template_name = 'inspection_manufacture_info/inspection_manufacture_info.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        MaterialMaster = apps.get_model('manufacturing','MaterialMaster')
        context = super(ManufactureInfo, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])
        context.update({
            'materialmaster_list': MaterialMaster.objects.order_by('model_id'),
            'more_context': MaterialMaster.objects.all(),
            'manufactreno_list': bs_manufacture_data.objects.order_by('create_date'),
            'manufactreno_context': bs_manufacture_data.objects.all(),
        })

        return context


class MRBauditInfo(LoginRequiredMixin, generic.ListView):
    model = mrb
    context_object_name = 'mrb_list'
    template_name = 'inspection_mrb/inspection_mrb.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        MaterialMaster = apps.get_model('manufacturing','MaterialMaster')
        context = super(MRBauditInfo, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])
        context.update({
            'materialmaster_list': MaterialMaster.objects.order_by('model_id'),
            'more_context': MaterialMaster.objects.all(),
            'inspection_list': iqc_inspection.objects.order_by('inspection_date'),
            'inspection_context': iqc_inspection.objects.all(),
            'parameter_list': insp_param_catalogue.objects.order_by('create_date'),
            'parameter_context': insp_param_catalogue.objects.all(),
        })

        return context


class WaitingList(LoginRequiredMixin, generic.ListView):
    model = incoming_iqc_list
    context_object_name = 'waiting_list'
    template_name = 'inspection_waiting/inspection_waiting.html'
    fields = '__all__'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return incoming_iqc_list.objects.filter(
                Q(incoming_list_id__icontains=query)
            )
        else:
            return incoming_iqc_list.objects.all().order_by('create_date')


    def get_context_data(self, **kwargs):
        MaterialMaster = apps.get_model('manufacturing','MaterialMaster')
        context = super(WaitingList, self).get_context_data(**kwargs)
        print(self.request.GET)
        if 'error' in self.request.GET:
            context.update({
                'error': self.request.GET.get('error')
            })
            print(context['error'])
        context.update({
            'materialmaster_list': MaterialMaster.objects.order_by('model_id'),
            'more_context': MaterialMaster.objects.all(),
            'inspection_list': iqc_inspection.objects.order_by('inspection_date'),
            'inspection_context': iqc_inspection.objects.all(),
        })

        return context

class WaitingListDelete(LoginRequiredMixin, DeleteView):
    model = incoming_iqc_list
    success_url = reverse_lazy('qms:inspection_waiting')

### temp ###

@login_required
def inspection(request):
    return render(request, 'inspection/inspection.html')

@login_required
def inspection_waiting(request):
    return render(request, 'inspection_waiting/inspection_waiting.html')

@login_required
def inspection_mrb(request):
    return render(request, 'inspection_mrb/inspection_mrb.html')

@login_required
def inspection_manufacture_info(request):
    return render(request, 'inspection_manufacture_info/inspection_manufacture_info.html')

@login_required
def wms_receiving_form(request):
    return render(request, 'wms_receiving_form/wms_receiving_form.html')


