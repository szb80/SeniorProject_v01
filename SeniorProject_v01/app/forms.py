"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from app.models import Event, SearchEvent, ListEvent, District
import datetime

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User Name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class searchform(forms.ModelForm):
    class Meta:
        model = SearchEvent
        fields = ['name', 'description', 'event_type', 'date_start', 'district', ]
        widgets = {'date_start': SelectDateWidget(empty_label=("Select Year", "Select Month", "Select Day"))}


class createform(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Event
        fields = ['name',
                  'description',
                  'address',
                  'date_start',
                  'date_end',
                  #'street_address',
                  #'city',
                  #'zipcode',
                  'event_type',
                  'district',
                  'payment_url',
                  'primary_contact_ID',
                  'coord_x',
                  'coord_y',
                  'google_location',
                  ]
        widgets = {
            'date_start': SelectDateWidget(),
            'date_end': SelectDateWidget(),
                   }

    def __init__(self, *args, **kwargs):
        super(createform, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs = {'id': 'locationTextField',}
        self.fields['coord_x'].widget = forms.HiddenInput()
        self.fields['coord_y'].widget = forms.HiddenInput()
        self.fields['google_location'].widget = forms.HiddenInput()

class listform(forms.ModelForm):
    class Meta:
        model = ListEvent
        fields = ['event_type', 'district', ]

