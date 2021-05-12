from django import forms
from .models import Route, Station
from django.apps import apps

class RouteForm(forms.Form):
    route_id = forms.CharField(max_length=20,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Name...'
                                                          }))
    MaterialMaster = apps.get_model('manufacturing','MaterialMaster')
    

    model = forms.ModelChoiceField(queryset=MaterialMaster.objects.all())


    plantcode = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Plant Code...'
                                                              }))
    first_station = forms.ModelChoiceField(queryset=Station.objects.all())


class RouteSearchForm(forms.Form):
    ver = forms.CharField(max_length=20,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Ver...'
                                                          }))


class PackForm(forms.Form):
    workorder_type = forms.CharField(max_length=20,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'WorkOrder Type...'
                                                                   }))
    options = forms.MultipleChoiceField(choices=[(1, 'Label'), ('2', 'Country Kit')],
                                        widget=forms.CheckboxSelectMultiple(attrs={'class': 'radio-button-forms'
                                                                                   }))


class PalletForm(forms.Form):
    workorder_type = forms.CharField(max_length=20,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'WorkOrder Type...'
                                                                   }))
    pallet_limit = forms.IntegerField()
    options = forms.MultipleChoiceField(choices=[(1, 'pallet mix')],
                                        widget=forms.CheckboxSelectMultiple(attrs={'class': 'radio-button-forms'
                                                                                   }))
