from django.views import View, generic
from django.http import *
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from maskconfig.models import *
from line.models import *
from django.utils.timezone import make_aware
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.apps import apps
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, UserProfileForm, UserForm, ProfileForm, RepairMainForm, OutPNForm, LabelForm
from .models import *
from django.core.paginator import Paginator
from django.core import serializers
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.urls import reverse_lazy
from datetime import datetime
import string
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.db import connection
from collections import namedtuple


def reset_confirm(request):
    return render(request, 'registration/password_reset_confirmIMS.html')


# #### sidebar button
@login_required
def sub_config(request):
    return render(request, 'manufacturing/menu/sub-config.html')


@login_required
def sub_toolbox(request):
    return render(request, 'manufacturing/menu/sub-toolbox.html')


@login_required
def sub_wip(request):
    return render(request, 'manufacturing/menu/sub-wip.html')

@login_required
def sub_shipping_manager(request):
    return render(request, 'manufacturing/menu/sub-shipping-manager.html')

@login_required
def sub_qms(request):
    return render(request, 'manufacturing/menu/sub-qms.html')

@login_required
def sub_wms(request):
    return render(request, 'manufacturing/menu/sub-wms.html')


# #########################################################
@login_required
def home(request):
    return render(request, 'manufacturing/index.html')


@login_required
def fof(request):
    return render(request, 'bootstrap/404.html')


@login_required
def user_profile(request):
    return render(request, 'manufacturing/user/user-profile.html')


@login_required
def user_add_profile(request):
    return render(request, 'manufacturing/user/user-add-profile.html')


@login_required
def label_center(request):
    if request.method == 'GET':
        search_by = {
            'wo': 'WO',
            'sn': 'SN'
        }

        context = {
            'values': request.GET,
            'search_by': search_by,
        }

        label_types = Label.objects.all()
        if label_types:
            context['label_types'] = label_types

        if 'q' in request.GET:
            paginate_by = 5
            search_option = request.GET['searchID']
            query = request.GET['q']
            context['searchID'] = search_option

            if search_option == 'wo':
                #     model = SerialNumber
                workorder_list = WorkOrder.objects.filter(
                    Q(pk=query)
                )

                context['workorder_list'] = workorder_list

            elif search_option == 'sn':

                serial_number = SerialNumber.objects.filter(
                    Q(serial_number__iexact=query)
                )

                if serial_number:
                    context['serial_number'] = serial_number.first()

            else:
                messages.error(request, "doesn't exist")

        return render(request, 'manufacturing/label-center/label-center.html', context)
    elif request.method == 'POST':
        return render(request, 'manufacturing/label-center/label-center.html')


@login_required
def so_list(request):
    if request.method == 'GET':
        context = {
            'values': request.GET,
        }

        SalesOrder = apps.get_model('shipping', 'SalesOrder')

        sales_orders = SalesOrder.objects.all()

        if 'q' in request.GET:
            paginate_by = 10
            query = request.GET['q']

            sales_orders = sales_orders.filter(pk=query)

        context['sales_orders'] = sales_orders

    return render(request, 'manufacturing/somanager_list.html')


@login_required
def edit_profile(request):
    return render(request, 'manufacturing/user/user-profile-edit.html')

@login_required
def serialnumber_log(request):
    return render(request, 'manufacturing/serialnumber_log.html')


@login_required
def main_permissions(request):
    return render(request, 'manufacturing/user/user-main-permissions.html')


# ################################################################################
from django.contrib import messages


def signup(request):
    form = SignUpForm(request.POST)
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            # form.save()
            user = form.save()
            user.refresh_from_db()

            user.profile.department = form.cleaned_data.get('department')
            # user.profile.plant_code = form.cleaned_data.get('plant_code')
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('manufacturing:home')

    else:
        form = SignUpForm()
    return render(request, 'registration/signup-limited-access.html', {'form': form})


from django.contrib.auth.models import Group


@login_required
@permission_required('manufacturing.can_add_user')
def signup_sidebar(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # profile_form = ProfileForm(request.POST)

        if form.is_valid():
            # form.save()
            user = form.save()
            user.refresh_from_db()

            # groups = Group.objects.get('groups')
            # user.groups.add(groups)
            user.groups.name = form.cleaned_data.get('groups')

            user.profile.department = form.cleaned_data.get('department')
            # user.profile.plant_code = form.cleaned_data.get('plant_code')
            user.save()

            username = form.cleaned_data.get('username')

            # groups = form.cleaned_data.get('groups')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            # login(request, user)
            return redirect('manufacturing:user_list')




    else:
        form = SignUpForm()
        # profile_form = ProfileForm()
    return render(request, 'manufacturing/user/tabs/signup-sidebar.html', {'form': form})


## update user & profile forms at once
from django.db import transaction


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # group = Group.objects.get(name='group_name')
            # user.groups.add(group)

            return redirect('manufacturing:user_profile')
        else:
            messages.error(request, 'username already exists')


    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'manufacturing/user/user-profile-edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


######## password #################

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('manufacturing:user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'manufacturing/user/user-profile-change-password.html', {
        'form': form
    })


#####################################


@login_required
def add_user_profile(request):
    # if request.method == 'POST':
    user_form = SignUpForm(request.POST)
    profile_form = ProfileForm(request.POST)

    if form.is_valid():
        # form.save()
        user = form.save()
        user.refresh_from_db()

        # group = Group.objects.get('groups')
        # user.groups.add(group)
        user.groups.name = form.cleaned_data.get('groups')

        user.profile.department = form.cleaned_data.get('department')
        # user.profile.department = form.cleaned_data.get('plant_code')
        user.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        # login(request, user)
        return redirect('manufacturing:user_list')
    else:
        form = SignUpForm()
        # profile_form = ProfileForm()
    return render(request, 'manufacturing/user/signup-sidebar.html', {'form': form})


# ### users profile add form
class UsersProfilesAdd(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'manufacturing.can_add_profile'
    model = Profile
    template_name = 'manufacturing/user/users-add-profiles.html'
    fields = '__all__'
    success_url = reverse_lazy('manufacturing:users_profiles_list')


class UsersProfilesListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Profile
    # paginate_by = 5
    context_object_name = 'profile_list'
    template_name = 'manufacturing/user/users-profiles-list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Profile.objects.filter(
                Q(department__icontains=query)
            )
        else:
            return Profile.objects.all().order_by('-id')


class UsersProfilesDelete(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'manufacturing/user/users-profiles-list.html'
    success_url = reverse_lazy('manufacturing:users_profiles_list')


class UsersProfilesUpdate(LoginRequiredMixin, UpdateView):
    model = Profile

    template_name = 'manufacturing/user/users-update-profiles.html'
    # fields = '__all__'
    fields = ['department', ]
    success_url = reverse_lazy('manufacturing:user_list')


class UsersSidebarProfilesUpdate(LoginRequiredMixin, UpdateView):
    model = Profile

    template_name = 'manufacturing/user/user-sidebar-profile-update.html'
    # fields = '__all__'
    fields = ['department', ]
    # success_url = reverse_lazy('manufacturing:users_profiles_list')
    success_url = reverse_lazy('manufacturing:user_list')


# ####################  user permission ########################################
class UserListPermissionsView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    permission_required = 'manufacturing.can_add_permission'
    model = User
    # paginate_by = 5

    context_object_name = 'user_list'
    template_name = 'manufacturing/user/user-main-permissions.html'


class UserAddPermissionUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'manufacturing/user/user-add-permissions.html'
    # fields = '__all__'
    fields = ['user_permissions', 'groups', 'is_active', 'is_staff', 'is_superuser']
    success_url = reverse_lazy('manufacturing:user_list')

    def get_name(request):
        if request.method == 'POST':
            form = UserUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('manufacturing/user/user-list.html')
            else:
                form = UserUpdate()
            return render(request, 'manufacturing/user/user-list.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super(UserAddPermissionUpdate, self).get_context_data(**kwargs)
        context.update({
            'user_list': User.objects.order_by('-id'),
            'more_context': User.objects.all(),
        })
        return context


########### group ##############
class CreateUserGroup(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'manufacturing.can_add_user_group'
    model = Group
    template_name = 'manufacturing/user/group/create-user-group.html'
    fields = '__all__'
    success_url = reverse_lazy('manufacturing:user_group_list')

    def get_context_data(self, **kwargs):
        context = super(CreateUserGroup, self).get_context_data(**kwargs)
        context.update({
            'group_list': Group.objects.order_by('-id'),
            'more_context': Group.objects.all(),
        })
        return context


class UserGroupListView(PermissionRequiredMixin, LoginRequiredMixin, generic.ListView):
    permission_required = 'manufacturing.can_view_user_group_list'
    """Generic class-based list view for a list of authors."""
    model = Group
    # paginate_by = 5
    context_object_name = 'group_list'
    template_name = 'manufacturing/user/group/user-group-list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Group.objects.filter(Q(name__icontains=query))
        else:
            return Group.objects.all().order_by('id')


class UserGroupUpdate(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'manufacturing/user/group/update-user-group.html'
    fields = '__all__'
    success_url = reverse_lazy('manufacturing:user_group_list')

    def get_name(request):
        if request.method == 'POST':
            form = UserGroupUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('manufacturing/user/group/user-group-list.html')
            else:
                form = UserGroupUpdate()
            return render(request, 'manufacturing/user/group/user-group-list.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super(UserGroupUpdate, self).get_context_data(**kwargs)
        context.update({
            'group_list': Group.objects.order_by('id'),
            'more_context': Group.objects.all(),
        })
        return context


class UserGroupDelete(LoginRequiredMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('manufacturing:user_group_list')


################################################


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # group = Group.objects.get(name='group_name')
            # user.groups.add(group)

            return redirect('manufacturing:user_profile')
        else:
            messages.error(request, 'username already exists')


    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'manufacturing/user/user-profile-edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


######## password #################

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('manufacturing:user_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'manufacturing/user/user-profile-change-password.html', {
        'form': form
    })


#####################################


@login_required
def add_user_profile(request):
    # if request.method == 'POST':
    user_form = SignUpForm(request.POST)
    profile_form = ProfileForm(request.POST)

    if form.is_valid():
        # form.save()
        user = form.save()
        user.refresh_from_db()

        # group = Group.objects.get('groups')
        # user.groups.add(group)
        user.groups.name = form.cleaned_data.get('groups')

        user.profile.department = form.cleaned_data.get('department')
        # user.profile.department = form.cleaned_data.get('plant_code')
        user.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        # login(request, user)
        return redirect('manufacturing:user_list')
    else:
        form = SignUpForm()
        # profile_form = ProfileForm()
    return render(request, 'manufacturing/user/tab/signup-sidebar.html', {'form': form})


# ### users profile add form
class UsersProfilesAdd(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'manufacturing.can_add_profile'
    model = Profile
    template_name = 'manufacturing/user/users-add-profiles.html'
    fields = '__all__'
    success_url = reverse_lazy('manufacturing:users_profiles_list')


class UsersProfilesListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Profile
    # paginate_by = 5
    context_object_name = 'profile_list'
    template_name = 'manufacturing/user/users-profiles-list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Profile.objects.filter(
                Q(department__icontains=query)
            )
        else:
            return Profile.objects.all().order_by('-id')


class UsersProfilesDelete(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'manufacturing/user/users-profiles-list.html'
    success_url = reverse_lazy('manufacturing:users_profiles_list')


class UsersProfilesUpdate(LoginRequiredMixin, UpdateView):
    model = Profile

    template_name = 'manufacturing/user/users-update-profiles.html'
    # fields = '__all__'
    fields = ['department', ]
    success_url = reverse_lazy('manufacturing:user_list')


class UsersSidebarProfilesUpdate(LoginRequiredMixin, UpdateView):
    model = Profile

    template_name = 'manufacturing/user/user-sidebar-profile-update.html'
    # fields = '__all__'
    fields = ['department', ]
    # success_url = reverse_lazy('manufacturing:users_profiles_list')
    success_url = reverse_lazy('manufacturing:user_list')


# ####################  user permission ########################################
class UserListPermissionsView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    permission_required = 'manufacturing.can_add_permission'
    model = User
    # paginate_by = 5

    context_object_name = 'user_list'
    template_name = 'manufacturing/user/user-main-permissions.html'
    # def get_context_data(self, **kwargs):
    #     context = super(UserAddPermissionUpdate, self).get_context_data(**kwargs)
    #     context.update({
    #         'permissions_list': Permission.objects.order_by('-id'),
    #         'more_context': Permission.objects.all(),
    #     })
    #     return context


class UserAddPermissionUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'manufacturing/user/user-add-permissions.html'
    # fields = '__all__'
    fields = ['user_permissions', 'groups', 'is_active', 'is_staff', 'is_superuser']
    success_url = reverse_lazy('manufacturing:user_list')

    def get_name(request):
        if request.method == 'POST':
            form = UserUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('manufacturing/user/user-list.html')
            else:
                form = UserUpdate()
            return render(request, 'manufacturing/user/user-list.html', {'form': form})

    def get_context_data(self, **kwargs):
        context = super(UserAddPermissionUpdate, self).get_context_data(**kwargs)
        context.update({
            'user_list': User.objects.order_by('-id'),
            'more_context': User.objects.all(),
        })
        return context


################################################

class UserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = User
    # paginate_by = 5

    context_object_name = 'user_list'
    template_name = 'manufacturing/user/user-list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(
                Q(last_name__icontains=query) | Q(first_name__icontains=query) | Q(username__icontains=query) | Q(
                    email__icontains=query)
            )
        else:
            return User.objects.all().order_by('-id')


class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('manufacturing:user_list')


class UserProfilePageUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'manufacturing/user/user-profile-edit.html'
    fields = '__all__'
    success_url = reverse_lazy('manufacturing:user_profile')

    def get_name(request):
        if request.method == 'POST':
            form = UserProfilePageUpdate(request.POST)

            if form.is_valid():
                return HttpResponseRedirect('manufacturing/user/user-profile-edit.html')
            else:
                form = UserProfilePageUpdate()
            return render(request, 'manufacturing/user/user-profile-edit.html', {'form': form})


class UserProfileDetail(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'manufacturing/user/user-profile.html'
    fields = '__all__'


from django.contrib import messages


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'manufacturing/user/tabs/signup-sidebar-update.html'
    # fields = '__all__'
    fields = ['username', 'first_name', 'last_name', 'email', 'groups']
    success_url = reverse_lazy('manufacturing:user_list')

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context.update({
            'profile_list': Profile.objects.order_by('-id'),
            'more_context': Profile.objects.all(),
        })
        return context

    def get_name(self):
        if request.method == 'POST':
            form = UserUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('manufacturing/user/user-list.html')
            else:
                messages.error(request, 'username already exists')
        else:
            form = UserUpdate()
            return render(request, 'manufacturing/user/user-list.html', {'form': form})

    def validate_user(self):
        if request.method == 'POST':
            form = UserUpdate(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manufacturing:user_list')
            else:
                messages.error(request, "username already exists")


# ###### user id update form #####
from django.views.generic.edit import FormView


class NewUserProfileView(FormView):
    template_name = 'manufacturing/user/tabs/signup-sidebar-update.html'
    form_class = UserProfileForm

    def form_valid(self, form):
        form.save(self.request.user)
        return super(NewUserProfileView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('manufacturing:user_list')


class EditUserProfileView(UpdateView):
    form_class = UserProfileForm
    template_name = 'manufacturing/user/tabs/signup-sidebar-update.html'

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user.profile

    def get_success_url(self, *args, **kwargs):
        return reverse('manufacturing:user_list')


########################
def profiles_detail_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["user"] = User.objects.get(id=id)

    return render(request, 'manufacturing/user/tabs/signup-sidebar-update.html', context)


# update view for details
def users_update_profiles_view(request, id):
    # dictionary for initial datFa with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(User, id=id)
    objprofile = get_object_or_404(Profile, id=id)

    user_form = UserForm(request.POST or None, instance=obj)
    profile_form = ProfileForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return HttpResponseRedirect("/" + id)

        # add form dictionary to context
    context['user_form', 'profile_form'] = user_form

    return render(request, 'manufacturing/user/tabs/signup-sidebar-update.html', context)


##########################

class UserProfileListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = User
    context_object_name = 'user_list'
    template_name = 'manufacturing/user/user-profile.html'


###   all users profile add form


########################################################################


class SearchUserView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'manufacturing/user/tabs/signup-sidebar-update.html'
    fields = '__all__'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            query = 'default value'
        object_list = OrderForm.objects.filter(
            Q(last_name__icontains=query) | Q(first_name__icontains=query) | Q(username__icontains=query) | Q(
                email__icontains=query)
        )
        return object_list


############$##########################################################
class WorkOrderListView(LoginRequiredMixin, generic.ListView):
    model = WorkOrder
    # context_object_name = 'workorder_list'
    template_name = 'manufacturing/workorder_list.html'
    paginate_by = 17
    success_url = reverse_lazy('manufacturing:workorder_list_reverse')

    def get_queryset(self):

        queryset_list = WorkOrder.objects.order_by('pk')

        if 'searchID' in self.request.GET:
            searchID = self.request.GET['searchID']

            if searchID == 'sn':

                if 'query' in self.request.GET and self.request.GET['query'] != '':
                    serial_number = self.request.GET['query']
                    if serial_number:
                        sn = SerialNumber.objects.filter(serial_number=serial_number)
                        if sn:
                            sn = sn.first()
                            queryset_list = queryset_list.filter(workorder_id=sn.workorder_id)
            elif searchID == 'wo':
                if 'query' in self.request.GET and self.request.GET['query'] != '':
                    work_order = self.request.GET['query']
                    queryset_list = queryset_list.filter(pk=work_order)

            if 'status' in self.request.GET:
                status = self.request.GET['status']

                if status:
                    queryset_list = queryset_list.filter(status_id__name=status)

            # paginator = Paginator(queryset_list, 10)
            # page = self.request.GET.get('page')
            # paged_workorders = paginator.get_page(page)

            # context = WorkOrder.objects.all().order_by('-id')
            # return paged_workorders
        return queryset_list

    def get_context_data(self, **kwargs):
        context = super(WorkOrderListView, self).get_context_data(**kwargs)

        search_by = {
            'wo': 'WO',
            'sn': 'SN'
        }
        status = ['Accepted', 'Import', 'Released', 'Generated SN', 'Completed', 'Cancelled', 'Error']

        context['values'] = self.request.GET
        context['search_by'] = search_by
        context['status'] = status

        return context


class WorkOrderReverseListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""

    template_name = 'manufacturing/workorder_list.html'
    paginate_by = 17

    def get_queryset(self):
        # model = WorkOrder
        context_object_name = 'workorder_list'

        query = self.request.GET.get('q')

        # search_option = self.request.GET['searchID']

        if query:
            return WorkOrder.objects.filter(
                Q(pk=query)
            )
        else:
            return WorkOrder.objects.all().order_by('-pk')
        return redirect('manufacturing:workorder_list_reverse')

    def get_context_data(self, **kwargs):
        context = super(WorkOrderReverseListView, self).get_context_data(**kwargs)

        search_by = {
            'wo': 'WO',
            'sn': 'SN'
        }

        status = ['Accepted', 'Import', 'Released', 'Generated SN', 'Completed', 'Cancelled', 'Error']

        context['search_by'] = search_by
        context['status'] = status

        return context


##### 3/9 search #####################################################
class SearchResultsBySNView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = SerialNumber
    context_object_name = 'serialnumber_list'
    template_name = 'manufacturing/serialnumber_list.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            query = 'default value'

        object_list = SerialNumber.objects.filter(
            Q(serial_number__icontains=query)
        )

        return object_list


class SearchResultsByWOView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = WorkOrder
    # context_object_name = 'workorder_list'
    template_name = 'manufacturing/label-center-search-wo.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if not query:
            query = 'default value'

        object_list = WorkOrder.objects.filter(
            Q(pk=query)
        )
        return object_list


########################################################################
class WorkOrderEditUpdate(LoginRequiredMixin, UpdateView):
    model = WorkOrder
    template_name = 'manufacturing/workorder_status.html'
    fields = ['status_id']
    success_url = reverse_lazy('manufacturing:workorder_list_reverse')

    def get_name(self, request):
        if request.method == 'POST':
            form = WorkOrderEditUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('manufacturing/WorkOrder_list.html')
            else:
                form = WorkOrderEditUpdate()
            return render(request, 'manufacturing/WorkOrder_list.html', {'form': form})


#########################################################################################################################
class WorkOrderDetailListView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return WorkOrderDetail.objects.filter(title__icontains=query)
        else:
            return WorkOrderDetail.objects.all().order_by('-row_id')

    paginate_by = 6


class WorkOrderDetailDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = WorkOrderDetail


def workorder_detail(request, pk):
    if request.method == 'GET':

        search_by = {
            'wo': 'WO',
            'sn': 'SN'
        }

        context = {
            'values': request.GET,
            'search_by': search_by,
        }
        # TODO catch errors for calling .first()

        work_order = WorkOrder.objects.filter(pk=pk)
        

        if work_order:
            work_order = work_order.first()
            context['workorder'] = work_order
          

            model = MaterialMaster.objects.filter(pk=work_order.skuno).first()

            if model:

                route = Route.objects.filter(prod_version=work_order.production_version).first()
                context['route'] = route
                serial_numbers = SerialNumber.objects.filter(workorder_id=work_order.pk).order_by('serial_number')

                if serial_numbers:
                    context['serial_numbers'] = serial_numbers
                    context['total_sn'] = serial_numbers.count()
                   
                if route:
                    stations = route.get_stations()

                    context['stations'] = stations

            wo_detail = WorkOrderDetail.objects.filter(workorder_id=work_order.pk)

            if wo_detail:
                context['wo_detail'] = wo_detail
        return render(request, 'manufacturing/workordermanager-wo-detail.html', context)


def serialnumber_detail(request, pk):
    serial_number = SerialNumber.objects.filter(pk=pk).first()

    if serial_number:
        context = {
            'serialnumber': serial_number
        }

        # TODO sn has an fk in memory to mm. No need to lookup
        model = MaterialMaster.objects.filter(pk=serial_number.model_id).first()

        if model:
            context['model'] = model
            wo_ref = WorkOrder.objects.filter(pk=serial_number.workorder_id)
            route = None

            if wo_ref:
                wo_ref = wo_ref.first()
                route = Route.objects.filter(prod_version=wo_ref.production_version).first()

            if route:
                context['route'] = route
                stations = route.get_stations()

            # keyparts = set()

            # for keypart in KeyPart.objects.filter(sn=serial_number.pk).select_related('part'):
            #     # by using select_related you only hit the database once, so then later keypart.part does not hit the database again
            #     keyparts.add(keypart.part)

            keyparts = serial_number.get_keyparts()
            if keyparts:
                context['keyparts'] = keyparts
                models = keyparts.values('model_id')
                materials = MaterialMaster.objects.filter(model_id__in=models)

                for part in keyparts:

                    desc = materials.filter(model_id=part.model_id)
                    if desc:
                        part.desc = desc.first().model_desc


        serial_number_log = SerialNumberLog.objects.distinct('station').filter(
            serial_number__iexact=serial_number.serial_number).order_by('station', '-in_station_time')

        completed_stations = list(serial_number_log.values_list('station', flat=True))

        for station in stations:

            station.completed = False
            station.time = None

            if station.pk in completed_stations:
                temp_log = serial_number_log.filter(station=station).first()
                station.completed = True
                station.in_station_time = str(temp_log.in_station_time)
                station.operator = temp_log.user
        context['stations'] = stations

        if serial_number_log:
            context['serialnumber_log'] = serial_number_log
            context['last_sn_log'] = serial_number_log.last()

    return render(request, 'manufacturing/workordermanager-sn-detail.html', context)


from line.models import Station


class SerialNumberListView(LoginRequiredMixin, generic.ListView):
    # model = SerialNumber
    # context_object_name = 'serialnumber_list'
    template_name = 'manufacturing/snmanager/snmanager_list.html'
    paginate_by = 16
    model = SerialNumber
    context_object_name = 'serialnumber_list'

    # success_url = reverse_lazy('manufacturing:workorder_list_reverse')

    def get_context_data(self, **kwargs):

        context = super(SerialNumberListView, self).get_context_data(**kwargs)

        serialnumbers = SerialNumber.objects.all().order_by('serial_number')

        query = self.request.GET.get('q')

        serialnumber_list = []
        if query:
            serialnumber_list = serialnumbers.filter(serial_number=query)
            context['object_list'] = serialnumber_list
        else:
            serialnumber_list = serialnumbers

        stations = Station.objects.all()
        context.update({
            'serialnumber_list': serialnumber_list,
            'values': self.request.GET,
            'stations': stations
        })



        return context

        


def serialnumber_update(request):
    Station = apps.get_model('line', 'Station')
    SerialNumber = apps.get_model('manufacturing', 'SerialNumber')
    if request.method == "POST":
        data = request.POST
        

        station_id = data.get('station')
        serialnumber_id = data.get('serialnumber')

        serialnumber_ref = SerialNumber.objects.filter(pk=serialnumber_id)
        station_ref = Station.objects.filter(pk=station_id)
        

        if serialnumber_ref and station_ref:
            serialnumber_ref = serialnumber_ref.first()

            serialnumber_ref.station_id = station_ref.first()

            serialnumber_ref.save()

    return redirect('manufacturing:serialnumber_list')


class SerialNumberUpdate(LoginRequiredMixin, UpdateView):
    model = SerialNumber
    template_name = 'manufacturing/snmanager/snmanager_update.html'
    fields = ['station']
    success_url = reverse_lazy('manufacturing:serialnumber_list')

    def get_name(request):
        if request.method == 'POST':
            form = SerialNumberUpdate(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('manufacturing/snmanager/snmanager_list.html')
            else:
                form = SerialNumberUpdate()
            return render(request, 'manufacturing/snmanager/snmanager_list.html', {'form': form})


class SNManagereDetail(LoginRequiredMixin, generic.DetailView):
    model = SerialNumber
    template_name = 'manufacturing/snmanager/snmanager_detail.html'
    fields = '__all__'


class SerialNumberForm(LoginRequiredMixin, CreateView):
    model = SerialNumber
    template_name = 'manufacturing/station_form.html'
    fields = ['work_station', 'serial_number']
    success_url = reverse_lazy('manufacturing:workorder_list')


def wo_detail_view(request, primary_key):
    WorkOrderDetail = get_object_or_404(WorkOrderDetail, pk=primary_key)
    return render(request, 'manufacturing/workorder-detail.html', context={'WorkOrderDetail': WorkOrderDetail})


########################################################################
class SerialNumberTestForm(LoginRequiredMixin, CreateView):
    model = SerialNumber
    template_name = 'manufacturing/station_form.html'
    fields = ['serial_number']


from django.shortcuts import get_object_or_404

def wo_detail_view(request, primary_key):
    WorkOrderDetail = get_object_or_404(WorkOrderDetail, pk=primary_key)
    return render(request, 'manufacturing/workorder-detail.html', context={'WorkOrderDetail': WorkOrderDetail})


##################################################################

class SerialNumberDetail(LoginRequiredMixin, generic.DetailView):
    model = SerialNumber
    template_name = 'manufacturing/letternumber_detail.html'
    fields = '__all__'


##################################################################################################
def post(self, request):
    data = request.POST
    # data is a dictionary version of all data taken from POST
    if 'get_wo' in data:
        first_char = 'A'
        model_name = str(data.get('work order model'))
        count = str(SerialNumber.objects.count())
        while len(count) < 10:
            count = '0' + count
        serial_num = first_char + model_name + count

    return redirect('manufacturing:workorder_list')


################### 211 ############################


class WorkOrderIndex(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = WorkOrder
    context_object_name = 'WorkOrder_list'
    template_name = 'manufacturing/WorkOrder_list.html'


##################### 2/19 ####################################


def post_generate_sn(request):
    template_name = 'manufacturing/WorkOrder_list.html'

    def post_gen(request):

        id = request.POST.get('workorder_id')
        # get work order reference
        workorder_ref = WorkOrder.objects.filter(pk=id)

        if workorder_ref:
            workorder_ref = workorder_ref.first()

            workorder_ref.generate_serial_numbers(request.user)

        return redirect(reverse('manufacturing:workorder_list_reverse'))

    if request.method == 'POST':
        if request.POST.get('serial_number'):
            return post_gen(request)
    return redirect(reverse('manufacturing:workorder_list_reverse'))


######## 3/23 ################

class MaterialMasterListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = MaterialMaster
    context_object_name = 'materialmaster_list'
    template_name = 'maskconfig/maskmanager-list-search.html'
    paginate_by = 5


def label_create(request):
    if request.method == 'GET':
        return render(request, "manufacturing/label-center/label_create.html")

    if request.method == 'POST':
        form = LabelForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('manufacturing:label-center')

        return redirect('manufacturing:label-create')


# Get serial numbers for a workorder
def get_serial_numbers(request):
    if request.method == 'GET':
        wo = request.GET.get('workorder')
        workorder = WorkOrder.objects.filter(pk=wo)

        if workorder:
            workorder = workorder.first()

            serial_numbers = workorder.get_serial_numbers()

            data = []

            for sn in serial_numbers:
                data.append(sn.serial_number)

            return JsonResponse(data, safe=False)
        else:
            return HttpResponse("Workorder does not exist.")

        return redirect('manufacturing:label-create')


# ############# 621 repair update view #####################################
# in process of moving to line/wip/repair. should be removed from here
@login_required
@transaction.atomic
def update_repair(request):
    def get_serialnumber(request):

        serial_number = request.POST.get('serial_number')
        serial_number_ref = SerialNumber.objects.filter(serial_number=serial_number)
        return serial_number_ref.first()

    if request.method == 'POST':

        repairmain = get_serial_numbers(request)

        data = request.POST
        failure_sequence = data.get('failure_sequence')
        repaired_code = data.get('repaired_code')
        repaired_description = data.get('repaired_description')
        replacement = data.get('replacement')
        in_part_no = data.get('in_part_no')
        out_part_no = data.get('out_part_no')
        creator = str(request.user)
        repaired_date = data.get('repaired_date')

        repairmain_ref = RepairMain.objects.filter(failure_sequence=failure_sequence)
        repairmain_ref = RepairMain.objects.filter(failure_sequence=failure_sequence)

        repair_code_ref = RepairCode.objects.filter(pk=repaired_code)
        repairmain = get_serial_numbers(request)

        # if form.is_valid():
        #     messages.success(request, 'The form is valid.')
        # elif in_part_no != out_part_no:
        #     messages.error(request, 'part number does not match.')

        if repair_code_ref and repairmain_ref and in_part_no == out_part_no:
            repairmain_ref = repairmain_ref.first()
            repair_code_ref = repair_code_ref.first()

            repairdetail_ref = RepairDetail(failure_sequence=repairmain_ref,
                                            repaired_code=repair_code_ref,
                                            repaired_description=repaired_description,
                                            replacement=replacement,
                                            in_part_no=in_part_no,
                                            out_part_no=out_part_no,
                                            creator=creator,
                                            repaired_date=make_aware(datetime.now()),

                                            )

            try:
                repairdetail_ref.save()
                repairmain_ref.result = 1
                repairmain_ref.repaired_date = datetime.now()
                repairmain_ref.save()
            except:
                pass

            error = 'Repair code Does Not Exist'
            context = {
                'error': error,

            }

            # return redirect(reverse('manufacturing:repair_station') + '?sn=' + str(get_serialnumber(request)) + '?error' + error)
            return redirect(reverse('manufacturing:repair_station') + '?sn=' + str(get_serialnumber(request)))

            # return render(request, 'manufacturing/wip/repair.html', context)

            # return redirect(request.get_full_path())
            # return HttpResponseRedirect(request.path_info)

        # elif in_part_no != out_part_no:
        # messages.error(request, 'part number does not match.')
        # messages = 'part number does not match.'
        # return redirect(reverse('manufacturing:repair_station') + '?sn=' + str(get_serialnumber(request)) + '&error=' + messages)
        else:
            error = 'Repair code Does Not Exist'

            if in_part_no != out_part_no:
                error = 'part number does not match'
            else:
                error = 'Repair code Does Not Exist'

            return redirect(
                reverse('manufacturing:repair_station') + '?sn=' + str(get_serialnumber(request)) + '&error=' + error)
            # return HttpResponseRedirect(request.path_info)

    # return render(request, 'manufacturing/wip/repair.html')

    return redirect(reverse('manufacturing:repair_station') + '?sn=' + '?sn=' + str(get_serialnumber(request)))
    # return render(request, 'manufacturing/wip/repair.html', {
    #
    # })


#####################################################################################################


@login_required
def hold_station(request):
    hold_list = Hold.objects.all().filter(hold_status=1).order_by('-hold_date')
    return render(request, 'manufacturing/hold/hold_station.html', {'hold_list': hold_list})


@login_required
def UnHold(request, hold_id):
    def get(request):
        hold_obj = get_object_or_404(Hold, hold_id=hold_id)
        template_name = 'manufacturing/hold/hold-unhold.html'
        context = {'hold': hold_obj, }
        return render(request, template_name, context)

    def post(request):
        hold_id = request.POST['hold_id']
        hold_value = request.POST['hold_value']
        unhold_reason = request.POST['unhold_reason']
        unhold_by = request.POST['username']

        cursor = connection.cursor()
        query = '''CALL mfg_hold_station_save (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, ['UNHOLD', hold_id,
                               hold_value, '', '', '', '', unhold_by, unhold_reason])
        cursor_result = namedtuplefetchall(cursor)
        result = cursor_result[0].sp_result

        if len(result) > 0:
            messages.error(request, result)
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect('manufacturing:hold_station')

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


@login_required
def HoldEdit(request, hold_id):
    def get(request):
        hold_obj = get_object_or_404(Hold, hold_id=hold_id)
        hold_types = HoldTypes.objects.all()
        template_name = 'manufacturing/hold/hold-edit.html'
        context = {'hold': hold_obj,
                   'hold_types': hold_types}
        return render(request, template_name, context)

    def post(request):
        p_id = request.POST['hold_id']
        p_value = request.POST['hold_value']
        p_by = request.POST['username']
        p_reason = request.POST['hold_reason']
        p_station = request.POST['hold_station']
        p_typeid = request.POST['hold_type']
        p_ureason = request.POST.get('unhold_reason', '')

        cursor = connection.cursor()
        query = '''CALL mfg_hold_station_save (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(
            query, ['EDIT', p_id, p_value, p_by, p_reason, p_station, p_typeid, p_by, p_ureason])
        cursor_result = namedtuplefetchall(cursor)
        result = cursor_result[0].sp_result

        if len(result) > 0:
            messages.error(request, result)
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect('manufacturing:hold_station')
        # return HttpResponse(p_typeid)

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


@login_required
def HoldAdd(request):
    def get(request):
        hold_types = HoldTypes.objects.all()
        template_name = 'manufacturing/hold/hold-add.html'
        context = {'hold_types': hold_types, }
        return render(request, template_name, context)

    def post(request):
        p_value = request.POST['hold_value']
        p_by = request.POST['username']
        p_reason = request.POST['hold_reason']
        p_station = request.POST['hold_station']
        p_typeid = request.POST['hold_type']

        cursor = connection.cursor()
        query = '''CALL mfg_hold_station_save (%s, %s, %s, %s, %s, %s, %s)'''
        sp_result = cursor.execute(
            query, ['HOLD', '', p_value, p_by, p_reason, p_station, p_typeid])

        cursor_result = namedtuplefetchall(cursor)
        result = cursor_result[0].sp_result

        if len(result) > 0:
            messages.error(request, result)
            return redirect(request.META['HTTP_REFERER'])
        else:
            return redirect('manufacturing:hold_station')

    if request.method == 'POST':
        return post(request)
    else:
        return get(request)

