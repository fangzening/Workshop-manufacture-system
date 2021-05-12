from django.shortcuts import render, redirect, reverse
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import *
from manufacturing.models import *
import json
from .forms import SegmentForm, MaskForm, SegmentModalForm
from django.urls import reverse_lazy
from datetime import datetime, date
from django.core.exceptions import ValidationError
from django.apps import apps
import random
import string

### temp ###

@login_required
def ooba_list_view(request):
    return render(request, 'ooba/ooba_list.html')
def ooba_create_view(request):
    return render(request, 'ooba/ooba_create_sku.html')
########################

class MaterialMasterListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = MaterialMaster
    context_object_name = 'materialmaster_list'
    template_name = 'maskconfig/createmask.html'

    def get_context_data(self, **kwargs):
        context = super(MaterialMasterListView, self).get_context_data(**kwargs)
        context.update({
            'mask_list': Mask.objects.all().order_by('mask_id'),
            'more_context': Mask.objects.all(),
        })
        return context

    # def Diff(materialmaster_list, mask_list):
    #     li_dif = [i for i in materialmaster_list + mask_list if i not in materialmaster_list or i not in mask_list]
    #     return li_dif

    def createmask(request):
        template_name = 'maskconfig/createmask.html'
        
        def get(request):
            form = MaskForm()

            return render(request, template_name, {'form': form})

        def post(request):

            data = request.POST

            # in order of model

            model = str(data.get('model'))

            MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')

            model_ref = MaterialMaster.objects.filter(pk=model)

            if model_ref:
                model_ref = model_ref.first()
                creator = str(request.user)
                action = 'Mask: ' + model + ' was created by ' + creator

                mask = Mask(model=model_ref,
                            action=action,
                            creator=creator,
                            create_date=datetime.now()

                            )
                mask.full_clean()
                mask.save()
            return redirect('maskconfig:mask-list-reverse')

        # request handler
        if request.method == 'GET':
            return get(request)
        elif request.method == 'POST':
            return post(request)

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return MaterialMaster.objects.filter(
                Q(model_id__icontains=query)
            )
        else:

            return MaterialMaster.objects.all().order_by('model_id')

class CreateMaskView(LoginRequiredMixin, CreateView):
    model = Mask
    template_name = 'maskconfig/createmask.html'
    # fields = ['model']
    fields = '__all__'
    success_url = reverse_lazy('maskconfig:mask-list-reverse')

    def get_context_data(self, **kwargs):
        context = super(CreateMaskView, self).get_context_data(**kwargs)
        context.update({
            'materialmaster_list': MaterialMaster.objects.order_by('model_id'),
            'more_context': MaterialMaster.objects.all(),
        })
        return context


# List of mask shells
class MaskConfigListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Mask

    template_name = 'maskconfig/maskmanager-list.html'
    context_object_name = 'maskmanager_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(MaskConfigListView, self).get_context_data(**kwargs)
        context.update({
            'materialmaster_list': MaterialMaster.objects.order_by('model_id'),
            'more_context': MaterialMaster.objects.all(),
        })
        return context

    def get_queryset(self):

        query = self.request.GET.get('q')
        if query:
            return Mask.objects.filter(
                Q(model=query)
            )
        else:
            return Mask.objects.all().order_by('mask_id')


class MaskConfigListReverseView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Mask

    template_name = 'maskconfig/maskmanager-list.html'
    context_object_name = 'maskmanager_list'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(MaskConfigListReverseView, self).get_context_data(**kwargs)
        context.update({
            'materialmaster_list': MaterialMaster.objects.order_by('model_id'),
            'more_context': MaterialMaster.objects.all(),
        })
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Mask.objects.filter(
                Q(model=query)
            )
        else:
            return Mask.objects.all().order_by('mask_id')


class MaskConfigCreateView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Mask

    template_name = 'maskconfig/createmask.html'
    context_object_name = 'maskmanager_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MaterialMasterListView, self).get_context_data(**kwargs)
        context.update({
            'mask_list': Mask.objects.order_by('mask_id'),
            'more_context': Mask.objects.all(),
        })
        return context


# List of segments per model number
@login_required
def segment(request):
    def get(request):

        model = request.GET.get('model_number')

        mask_ref = Mask.objects.filter(model_id=model)

        if mask_ref:

            mask_ref = mask_ref.first()

            segment_list = Segment.objects.filter(mask_id=mask_ref).order_by('position')

            context = {
                'segment_list': segment_list,
                'model': model
            }

            display_sn = mask_ref.generate_sn()
            if display_sn:
                context['sample_serial_number'], context['pattern'] = display_sn

            return render(request, 'maskconfig/masksegment-list.html', context)
        else:
            return render(request, 'maskconfig/masksegment-list.html')

    def post(request):

        data = str(request.body)

        data = data[2:-1:1]
        segment_array = []
        segment = ''

        for char in data:

            segment = segment + char

            if char == '}':
                if len(segment_array) != 0:
                    segment = segment[1:]

                length = len(segment_array)
                segment = json.loads(segment)
                segment_array.insert(length, segment)
                segment = ''

        return redirect('maskconfig:home')

    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':

        return post(request)


# creating a mask shell to hold segments
def createmask(request):
    template_name = 'maskconfig/createmask.html'

    def get(request):
        form = MaskForm()

        return render(request, template_name, {'form': form})

    def post(request):
        data = request.POST

        # in order of model

        model = str(data.get('model'))

        MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')

        model_ref = MaterialMaster.objects.filter(pk=model)
        Mask = apps.get_model('maskconfig', 'Mask')

        mask_ref = None
        if model_ref:
            mask_ref = Mask.objects.filter(model=model_ref.first())

        if model_ref and not mask_ref:
            model_ref = model_ref.first()
            creator = str(request.user)
            action = 'Mask: ' + model + ' was created by ' + creator

            mask = Mask.objects.create(model=model_ref,
                                       action=action,
                                       creator=creator,
                                       create_date=datetime.now()

                                       )
            mask.full_clean()
            mask.save()
        return redirect('maskconfig:mask-list-reverse')

    # request handler
    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':
        return post(request)


###### 2/25 ############################################


def createmask_row(request):
    template_name = 'maskconfig/maskmanager-list-search.html'

    def get(request):
        form = MaskForm()
        return render(request, template_name, {'form': form})

    def post(request):
        data = request.POST

        models = data.getlist('model')

        '''
        how data is modeled from request

        {model: [model1,model2,model3]}      
        extract the data and seperate it into lists
        test comment
        '''

        MaterialMaster = apps.get_model('manufacturing', 'MaterialMaster')

        filtered_models = []

        for element in range(len(models)):
            mod = str(models[element])

            mod_exist = MaterialMaster.objects.filter(pk=mod)

            if mod_exist:
                filtered_models.append(models[element])

        for index in range(len(filtered_models)):
            model = str(models[index])
            creator = str(request.user)
            action = 'Mask: ' + model + ' was created by ' + creator

            model_ref = MaterialMaster.objects.get(pk=model)

            mask = Mask.objects.create(model=model_ref,
                                       creator=creator,
                                       action=action,
                                       )
            mask.full_clean()
            mask.save()

        return redirect('maskconfig:mask-list-reverse')
        # success_url = reverse_lazy('manufacturing:workorder_list')

    # request handler
    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':
        return post(request)


class MaskDelete(LoginRequiredMixin, DeleteView):
    model = Mask
    success_url = reverse_lazy('maskconfig:mask-list-reverse')


### 2/26

class MaskUpdate(LoginRequiredMixin, UpdateView):
    model = Mask
    template_name = 'maskconfig/maskmanager-list.html'
    fields = ['model']
    success_url = reverse_lazy('maskconfig:mask-list-reverse')

    def get_name(request):
        if request.method == 'POST':
            form = MaskUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('maskconfig/maskmanager-list.html')
            else:
                form = MaskUpdate()
            return render(request, 'maskconfig/maskmanager-list.html', {'form': form})


### 3/16

class SegmentListUpdate(LoginRequiredMixin, UpdateView):
    model = Segment
    template_name = 'maskconfig/maskmanager-list-modal.html'
    fields = ['position', 'name', 'data_type', 'length']
    success_url = reverse_lazy('maskconfig:mask-list-reverse')


class MaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Mask
    template_name = 'maskconfig/maskmanager-list.html'
    success_url = reverse_lazy('maskconfig:home')


###### end 2/25 ############################################


# creating a segment to add to mask
# when using this page it needs to have a model number in
# the get request to be able to process the segment
def createsegment(request):
    # template name that is served during get request
    template_name = 'maskconfig/createsegment.html'

    # request for serving form to user
    def get(request):
        form = SegmentForm()
        return render(request, template_name, {'form': form})

    # request for handling that form
    def post(request):

        # incoming data
        data = request.POST

        # used to get the foregin key to join the segments on
        mask = get_model(request)
        mask_id = mask.pk

        segment_ref = Segment.objects.filter(mask_id=mask_id)

        # gets the number of segments
        count = 0
        for segment in segment_ref:
            count += 1

        # model(Segment) from models.py
        create_date = datetime.now()
        creator = str(request.user)
        name = str(data.get('name'))
        action = 'Segment: ' + name + ' was created by ' + creator
        position = len(segment_ref) + 1
        data_type = data.get('data_type')
        length = int(data.get('length') or -1)
        value = data.get('value')

        if data_type == 'Hard Code':
            length = len(value)
        elif data_type == 'Model':
            value = mask.model.model_id
            if int(length) > len(mask.model.model_id) or int(length) <= 0:
                length = len(mask.model.model_id)
                value = mask.model
            else:
                value = mask.model.model_id[0:length]
        else:
            value = None

        # handling the new segment based on the position inputted
        # position is position of the segment from the form
        # count is the number of segments currently in the table for that model
        if position > 0 and position <= (count + 1):
            # create the segment model

            segment_instance = Segment(mask_id=mask,
                                       create_date=create_date,
                                       creator=creator,
                                       name=name,
                                       action=action,
                                       position=position,
                                       data_type=data_type,
                                       length=length,
                                       value=value
                                       )

            # checks if there is no segments

            if int(length) < 20 and int(length) > 0:
                if position == (count) and count == 0:
                    segment_instance.save()
                if position == (count + 1):

                    segment_instance.save()
                elif position <= count:

                    override_position(segment_instance, count)
                    segment_instance.save()
                else:
                    segment_instance = None

            else:
                segment_instance = None
        else:

            segment_instance = None
            # redirect to original segment list
        return redirect(reverse('maskconfig:segments') + '?model_number=' + str(mask.model))

    '''
    gets the model reference needed
    must supply a get request with the model number
    '''

    def get_model(request):

        model = request.GET.get('model_number')
        mask_ref = Mask.objects.filter(model_id=model)
        return mask_ref.first()

    ''' 
    Algorithm to resolve position conflicts and re-order segments.
    Takes in a segment object as segment and the number of segments
    as the count.
    '''

    def override_position(segment, count):

        '''
        segment A,B,C with position 1,2,3 respectively

        takes in segment D with position 2

        output is A,D,B,C with positions 1,2,3,4 respectively

        '''
        temp_count = int(count)

        while (segment.position <= temp_count):
            old_segment = Segment.objects.filter(mask_id=segment.mask
                                                 ).filter(position=temp_count)

            old_segment = old_segment.first()
            old_segment.position = temp_count + 1

            old_segment.save()
            temp_count -= 1

    # use to handle incoming requests
    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':
        return post(request)


def edit_segment(request):
    template_name = 'maskconfig/editsegment.html'

    def get_model(request):

        model = request.GET.get('model')
        mask_ref = Mask.objects.filter(model_id=model)
        return mask_ref.first()

    def process_segments(segments, row_id, position):

        row_id = int(row_id)

        edited_segment = []
        segment_list = []
        num_segments = len(segments)

        for segment in segments:
            if segment.row_id == row_id:
                edited_segment.append(segment)
            else:
                segment_list.append(segment)

        for element in range(len(segment_list)):
            segment_list[element].position = element + 1

        if position == num_segments:
            segment_list.append(edited_segment[0])
        elif position == 1:
            segment_list = edited_segment + segment_list

            for element in range(len(segment_list)):
                segment_list[element].position = element + 1
        else:
            segment_list.insert((position - 1), edited_segment[0])

        return segment_list

    def get(request):
        data = request.GET

        segment = data.get('segment')

        segment_ref = Segment.objects.filter(pk=segment)
        segment_ref = segment_ref.first()

        context = {}
        data_types = [
        "Hard Code",
        "Date",
        "Week",
        "Month",
        "Year",
        "Numeric",
        "Alpha Numeric",
        "Text",
        "Model"
        ]

        # TODO fix this garbage code. Just pass the object itself and use dot notation
        if segment_ref:
            context['row_id'] =segment_ref.pk 
            context['name'] = segment_ref.name
            context['position'] = segment_ref.position
            context['data_type'] = segment_ref.data_type
            context['length'] = segment_ref.length
            context['value'] = segment_ref.value
            context['data_types'] = data_types

        return render(request, template_name, context)

    def post(request):

        # incoming data
        data = request.POST
        position = data.get('position')

        # get edited segment
        # segment_ref = Segment.ob

        # used to get the foregin key to join the segments on
        mask = get_model(request)
        mask_id = mask.pk
        segments = Segment.objects.filter(mask_id=mask_id).order_by('position')

        # gets the number of segments
        count = 0
        for segment in segments:
            count += 1

        # model(Segment) from models.py
        create_date = datetime.now()
        creator = str(request.user)

        name = str(data.get('name'))
        action = 'Segment: ' + name + ' was created by ' + creator
        position = int(data.get('position'))
        data_type = data.get('data_type')
        length = data.get('length')
        value = data.get('value')
        row_id = data.get('row_id')

        if position < 1:

            position = 1
        elif position > len(segments):

            position = len(segments)

        segment_list = process_segments(segments,data.get('row_id'),position)

        if data_type == 'Hard Code':
            length = len(value)
        elif data_type == 'Model':
            value = mask.model
            length = len(mask.model)
        else:
            value = None

        # saving segments back to db

        for index in range(len(segment_list)):
            segment_list[index].position = index + 1

            if segment_list[index].pk == int(row_id):
                segment_list[index].name = name
                segment_list[index].action = action
                segment_list[index].data_type = data_type
                segment_list[index].length = length
                segment_list[index].value = value

            segment_list[index].save()

        # for segment in segment_list:

        #     if segment.id == int(id):
        #         segment.name = name
        #         segment.action = action
        #         segment.data_type = data_type
        #         segment.length = length
        #         segment.value = value
        #         segment.position = position
        #     segment.save()

        return redirect(reverse('maskconfig:segments') + '?model_number=' + str(mask.model))

    if request.method == 'GET':
        return get(request)
    elif request.method == 'POST':
        return post(request)

class DeleteSegment(LoginRequiredMixin, DeleteView):
    model = Segment
    # response =  reverse_lazy('maskconfig:home')
    success_url = reverse_lazy('maskconfig:segments')


    def delete(self,request,*args,**kwargs):
        try:
            
            instance = self.model.objects.get(pk=kwargs['pk'])
            instance.delete()

        except:
            pass

        return self.get_success_url(request)

    def get_success_url(self,request):
        # default response
        default_response = redirect(reverse_lazy('maskconfig:home'))
        if request.method == 'POST' and 'model' in request.POST:

            get_param = '?' + 'model_number=' + request.POST['model']
            
            response = redirect(self.success_url + get_param)
        else:
            response = default_response
        return response
        # return redirect(reverse('maskconfig:segments') + '?model_number=' + str(123))


# ###### 2/25 #####
class CreateSegment(LoginRequiredMixin, CreateView):
    model = Segment
    template_name = 'maskconfig/masksegment-list.html'
    # fields = ['name', 'action', 'position']
    fields = '__all__'
    success_url = reverse_lazy('maskconfig:home')


######### 2/26 ########## create segment data row
@login_required
def segment_template(request):
    return render(request, 'maskconfig/masksegment-list.html')


def createsegment_row(request):
    # template name that is served during get request
    template_name = 'maskconfig/Segment-list.html'

    def post_gen(request):

        name = request.POST.get('name')
        id = int(request.POST.get('model_id'))

        mask_ref = Mask.objects.filter(pk=id)

        mask_ref = mask_ref.first()

        if mask_ref and name:
            created_date = datetime.now()
            mask = mask_ref
            name_instance = Mask.objects.create(created_date=created_date,
                                                mask_id=mask,
                                                name=name,
                                                )
            name_instance.clean()
            name_instance.save()

            mask_ref.clean()
            mask_ref.save()
        return redirect(reverse('maskconfig:segment-list'))

    if request.method == 'POST':
        if request.POST.get('name'):
            return post_gen(request)
    return redirect(reverse('maskconfig:segment-list'))


##### 2/28 #######
class MaskSegmentUpdate(LoginRequiredMixin, UpdateView):
    model = Segment
    template_name = 'maskconfig/masksegment-list.html'
    fields = ['name', 'length']

    # success_url = reverse_lazy('maskconfig:update-masksegment-row')

    def get(request):
        model = request.GET.get('model_number')
        mask_ref = Mask.objects.filter(model_id=model)
        if mask_ref:
            mask_ref = mask_ref.first()
            segment_list = Segment.objects.filter(mask_id=mask_ref).order_by('position')
            context = {
                'segment_list': segment_list,
                'model': model
            }
            return render(request, 'maskconfig/masksegment-list.html', context)
        else:
            return render(request, 'maskconfig/masksegment-list.html')

    def get_name(request):
        if request.method == 'POST':
            form = MaskSegmentUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('maskconfig/masksegment-list.html')
            else:
                form = MaskSegmentUpdate()
            return render(request, 'maskconfig/masksegment-list.html', {'form': form})




##### 3/13 #######
class MaskSegmentModalUpdate(LoginRequiredMixin, UpdateView):
    model = Segment
    template_name = 'maskconfig/masksegment-list-modal.html'
    fields = ['name', 'length']
    success_url = reverse_lazy('maskconfig:mask-list-reverse')

    def get_name(request):
        if request.method == 'POST':
            form = MaskSegmentModalUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('maskconfig/masksegment-list.html')
            else:
                form = MaskSegmentUpdate()
            return render(request, 'maskconfig/masksegment-list.html', {'form': form})


def mask_modal_row(request):
    template_name = 'maskconfig/masksegment-list-modal.html'

    def get(request):
        form = SegmentModalForm()
        return render(request, template_name, {'form': form})

    def post(request):

        data = request.POST
        masks = data.getlist('mask')
        name = data.getlist('name')
        length = data.getlist('length')
        position = data.getlist('length')
        data_type = data.getlist('data_type')

        for index in range(len(masks)):
            mask = str(masks[index])
            name = str(name[index])
            length = str(length[index])
            position = str(position[index])
            creator = str(request.user)
            datatype = str(data_type[index])

            segment = Segment.objects.update(mask_id=mask,
                                             name=name,
                                             length=length,
                                             position=position,
                                             creator=creator,
                                             datatype=datatype)

            segment.full_clean()
            segment.save()

        return redirect('maskconfig:mask-list-reverse')

        # success_url = reverse_lazy('manufacturing:workorder_list')

    # request handler
    if request.method == 'GET':

        return get(request)
    elif request.method == 'POST':
        return post(request)




