from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Profile, TestingResult, RepairDetail, Label, RepairMain
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    # group = forms.ModelChoiceField(queryset=Group.objects.all(),
    #                                required=True)
    # groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
    # groups = forms.ManyToManyField(Group, through='User')
    # plant_code = forms.ModelChoiceField(queryset=Profile.objects.all(),
    #                                required=True)
    department = forms.CharField(max_length=100)

    # TYPE_CODE = (
    #     ('FIIX', 'FIIX'),
    # )
    # plant_code = forms.ChoiceField(choices=TYPE_CODE)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'department')


class SignUpLogInForm(UserCreationForm):
    department = forms.CharField(max_length=100)

    # TYPE_CODE = (
    #     ('FIIX', 'FIIX'),
    #     ('TEST', 'TEST'),
    # )
    # plant_code = forms.ChoiceField(choices=TYPE_CODE)

    class Meta:
        model = User
        fields = ('department', 'groups')


class UserProfileForm(forms.Form):
    location = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    role = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)


################ group ###################


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'permissions': FilteredSelectMultiple("Permission", False, attrs={'rows': '2'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


############# user and profile form ##########
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('department',)

    # ############## users id update form ########


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user', 'department')  # Note that we didn't mention user field here.

    def save(self, user=None):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ('name', 'zpl')


#################### repair form ########################
# class OutPNForm(forms.Form):
#     out_part_no = forms.CharField(max_length=30)
#     message = forms.CharField(max_length=200, widget=forms.TextInput)
#
#
# class TestResultForm(forms.Form):
#     result = forms.CharField(max_length=1)


class OutPNForm(forms.Form):
    fields = '__all__'

    #     lookup model instances
    def lookup(self):
        self.data['replacement'] = "foobar"
        print(self.data.get('replacement'))

    #     add non appended data
    def entry(self):
        pass


class RepairMainForm(forms.Form):
    fields = ['result']


######## password reset email ###############
