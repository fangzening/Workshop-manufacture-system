from django import forms


class OfflineStationForm(forms.Form):
    p_sn = forms.CharField(max_length = 50, required = True)
    p_pn = forms.CharField(max_length = 30, required = True)
    p_gsn = forms.CharField(max_length = 50, required = True)
    pn = forms.CharField(max_length = 30, required = True)

