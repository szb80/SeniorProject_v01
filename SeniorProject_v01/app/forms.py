"""
Definition of forms.
"""
import SeniorProject_v01
import datetime
import django.contrib.auth.forms

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _

from app.models import Event, SearchEvent, ListEvent, District
from bootstrap_datepicker_plus import DateTimePickerInput


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
    required_css_class = ' required'

    class Meta:
        model = Event
        fields = ['name',
                  'description',
                  'address',
                  'district',
                  'date_start',
                  'date_end',
                  'event_type',
                  'payment_url',
                  'primary_contact_name',
                  'primary_contact_info',
                  'coord_x',
                  'coord_y',
                  'google_location',
                  'creation_user',
                  'creation_date',
                  ]

        widgets = {
            'date_start': DateTimePickerInput(),
            'date_end': DateTimePickerInput(),
                   }

    def __init__(self, *args, **kwargs):
        district = kwargs.pop('district')
        permissions = kwargs.pop('permissions')

        super(createform, self).__init__(*args, **kwargs)

        self.fields['address'].widget.attrs = {'id': 'locationTextField',}
        self.fields['coord_x'].widget = forms.HiddenInput()
        self.fields['coord_y'].widget = forms.HiddenInput()
        self.fields['google_location'].widget = forms.HiddenInput()
        self.fields['creation_user'].widget = forms.HiddenInput()
        self.fields['creation_date'].widget = forms.HiddenInput()

        # check for district admin level or above
        # if not, only show the user's current distrit
        # set selected district to user's district
        if permissions < 3:
            self.fields['district'] = forms.ModelChoiceField(queryset=District.objects.filter(district_name=district))
        self.initial['district'] = district


class editForm(forms.ModelForm):
    required_css_class = ' required'

    class Meta:
        model = Event
        fields = ['name',
                  'description',
                  'address',
                  'date_start',
                  'date_end',
                  'event_type',
                  'payment_url',
                  'primary_contact_name',
                  'primary_contact_info',
                  ]

        widgets = {
            'date_start': DateTimePickerInput(),
            'date_end': DateTimePickerInput(),
                   }

class listform(forms.ModelForm):
    class Meta:
        model = ListEvent
        fields = ['event_type', 'district', ]



# SIGN UP FORM ################################################################################

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                 widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                 widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=254,  required=True,
                              widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Email address'}))
    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Create password'}))
    password2 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Repeat password'}))
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

        def clean_email(self):
                # Get the email
                email = self.cleaned_data.get('email')

                # Check to see if any users already exist with this email as a username.
                try:
                    match = User.objects.get(email=email)
                except User.DoesNotExist:
                    # Unable to find a user, this is fine
                    return email

                # A user was found with this as a username, raise an error.
                raise forms.ValidationError('This email address is already in use.')

