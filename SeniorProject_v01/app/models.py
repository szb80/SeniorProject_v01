"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import googlemaps

# Create your models here.

class State(models.Model):
    state_name = models.CharField(max_length = 100, default = '');
    abbreviation = models.CharField(max_length = 2, default = '');

    def __str__(self):
        return self.state_name;


class Troop(models.Model):
    troop_number = models.IntegerField(default = 0);
    """ district_ID = models.ForeignKey(District);
    leader_ID = models.ForeignKey(Person); ------------------------------ """
    admin_ID = models.ForeignKey(User);

    def __str__(self):
        return str(self.troop_number);


class Person(models.Model):
    first_name = models.CharField(max_length = 255, default = 'John');
    last_name = models.TextField(max_length = 255, default = 'Doe');
    email = models.EmailField(default = 'contact@me.co');
    troop_number = models.ForeignKey(Troop);
    """ address = AddressField(); --------------------------------------------------- """
    street_address = models.TextField(default = '')
    postal_code = models.IntegerField(default = 0);
    city = models.CharField(max_length = 255, default = '');
    state_name = models.ForeignKey(State);

    def __str__(self):
        return self.first_name + " " + self.last_name;


class Region(models.Model):
    region_name = models.CharField(max_length=255, default = '');
    abbreviation = models.CharField(max_length=6, default = '')

    def __str__(self):
        return self.region_name;


class District(models.Model):
    district_name = models.CharField(max_length=255, default = '');
    pointman_ID = models.ForeignKey(Person);
    region_ID = models.ForeignKey(Region);

    def __str__(self):
        return self.district_name;


class EventType(models.Model):
    name = models.CharField(max_length = 255, default = '');
    description = models.TextField(default = '');
    icon = models.FileField(null=True, blank=True)
    
    def __str__(self):
        return self.name;


class Event(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(help_text='Enter a description of the event.')
    event_type = models.ForeignKey(EventType)
    date_start = models.DateField(default = datetime.now)
    date_end = models.DateField(default = datetime.now)
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.TimeField(null=True, blank=True)
    address = models.CharField(max_length = 500, default = 'Address not provided')
    coord_x = models.CharField(max_length = 255, default = '', null=True, blank=True)
    coord_y = models.CharField(max_length = 255, default = '', null=True, blank=True)
    google_location = models.CharField(max_length = 300, default = '', null=True, blank=True)
    district = models.ForeignKey(District)
    payment_url = models.URLField(default = 'https://www.')
    primary_contact_ID = models.ForeignKey(Person, default=0)
    creation_date = models.DateTimeField(default = datetime.now)
    creation_user = models.ForeignKey(User, null=True, blank=True)

    def publish(self):
        self.creation_date = datetime.now();
        self.creation_user = request.user.id
        self.save();

    def __str__(self):
        return self.name;

    def get_absolute_url(self):
        url = '/event/' + str(self.id)
        return u'<a href="%s">%s</a>' % (url, str(self.name))


class SearchEvent(models.Model):
    name = models.CharField(max_length = 255, blank=True, null=True);
    description = models.CharField(max_length=255, default = '', blank=True, null=True);
    event_type = models.ForeignKey(EventType, blank=True, null=True);
    date_start = models.DateField(default = '', blank=True, null=True);
    district = models.ForeignKey(District, blank=True, null=True);
    primary_contact_ID = models.ForeignKey(Person, blank=True, null=True);


class ListEvent(models.Model):
    event_type = models.ForeignKey(EventType, blank=True, null=True);
    date_start = models.DateField(default = '', blank=True, null=True);
    district = models.ForeignKey(District, blank=True, null=True);


class autofill(models.Model):
    address = models.CharField(max_length=400)