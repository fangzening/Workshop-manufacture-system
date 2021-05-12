from django import forms
from django.core.validators import MinValueValidator
from .models import Mask, Segment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SegmentForm(forms.Form):
    position = forms.IntegerField(validators=[MinValueValidator(0)])
    TYPE_OF = (
        ('Hard Code', 'Hard Code'),
        ('Date', 'Date'),
        ('Numeric', 'Numeric'),
        ('Alpha Numeric', 'Alpha Numeric'),
        ('Text', 'Text'),
        ('Model', 'Model')
    )

    data_type = forms.ChoiceField(choices=TYPE_OF, widget=forms.Select(attrs={"onChange": 'validate()'}))
    name = forms.CharField(max_length=30)
    length = forms.IntegerField(validators=[MinValueValidator(0)], disabled=True)
    value = forms.CharField(max_length=30)

    def clean_position(self, *args, **kwargs):
        position = self.cleaned_data.get('position')
        if position > 0:
            return position
        else:
            raise forms.ValidationError('This is not a valid number(1,2,3,...')


class MaskForm(forms.Form):
    model = forms.CharField(max_length=20)


##### 3/13
class SegmentModalForm(forms.Form):
    mask = forms.CharField(max_length=30)
    position = forms.IntegerField(validators=[MinValueValidator(0)])
    name = forms.CharField(max_length=30)
    length = forms.IntegerField(validators=[MinValueValidator(0)], disabled=True)
    data_type = forms.CharField(max_length=30)


######### 2/26 create segment row
class SegmentRowForm(forms.Form):
    position = forms.IntegerField(validators=[MinValueValidator(0)])
    name = forms.CharField(max_length=30)
    length = forms.IntegerField(validators=[MinValueValidator(0)], disabled=True)

    def clean_position(self, *args, **kwargs):
        position = self.cleaned_data.get('position')
        if position > 0:
            return position
        else:
            raise forms.ValidationError('This is not a valid number(1,2,3,...')

