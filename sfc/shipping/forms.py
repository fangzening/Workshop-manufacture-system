from django import forms
from .models import PalletSerialNumber
from django.apps import apps
from manufacturing.models import *
from .models import *


# creating a form
# class AddSerialNumberForm(forms.ModelForm):
#
#     class Meta:
#
#         model = PalletSerialNumber
#
#
#         # fields = '__all__'
#         fields = ['serial_number', 'pallet_id']


class AddSerialNumberForm(forms.Form):
    serial_number = apps.get_model('manufacturing', 'SerialNumber')
    # serial_number =  forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                       'placeholder': 'Serial Number...'
    #                                                       }))
    # pallet_id =  forms.CharField(max_length=100)
    serial_number = forms.ModelChoiceField(queryset=SerialNumber.objects.all(),
                                    required=True)

    pallet_id = forms.ModelChoiceField(queryset=Pallet.objects.all(),
                                           required=True)


class PalletQty(forms.ModelForm):
    class Meta:
        model = Pallet
        fields = ['current_qty', 'pallet_id']
