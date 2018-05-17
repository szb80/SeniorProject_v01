"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
""" import GoogleMaps address object from package: """
from address.models import AddressField
from app.models import Event, SearchEvent

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
        fields = ['name', 'description', 'event_type', 'date_start', 'district']
        widgets = {'date_start': SelectDateWidget()}