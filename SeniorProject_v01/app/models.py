"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime
import googlemaps

# Create your models here.

class PermissionLevel(models.Model):
    level = models.IntegerField()
    level_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.level) + ' - ' + self.level_name


class State(models.Model):
    state_name = models.CharField(max_length = 100, default = '')
    abbreviation = models.CharField(max_length = 2, default = '')

    def __str__(self):
        return self.state_name;


class Region(models.Model):
    region_name = models.CharField(max_length=255, default = '')
    abbreviation = models.CharField(max_length=6, default = '')

    def __str__(self):
        return self.region_name
    

class District(models.Model):
    district_name = models.CharField(max_length=255, default = '')
    pointman_ID = models.ForeignKey(User)
    region_ID = models.ForeignKey(Region)

    def __str__(self):
        return self.district_name


class Troop(models.Model):
    troop_number = models.IntegerField(default = 0)
    state = models.ForeignKey(State)
    district = models.ForeignKey(District)
    admin_ID = models.ManyToManyField(User)

    def __str__(self):
        return str(self.troop_number)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length = 500, default = '', null=True, blank=True)
    troop_number = models.ForeignKey(Troop, default=0, null=True, blank=True)
    permissions = models.ForeignKey(PermissionLevel, default=0)
    
    def __str__(self):
        return str(self.user.username)
    
    def get_troop(self):
        try:
            t = Troop.objects.get(troop_number=self.troop_number.troop_number)
            return t.troop_number
        except:
            return Troop.objects.get(troop_number=0) #'profile.gettroop error'

    def get_district(self):
        try:
            t = Troop.objects.get(troop_number=self.troop_number.troop_number)
            d = District.objects.get(district_name=t.district)
            return d
        except:
            return 'profile.getdistrict error'

    def get_district_pk(self):
        try:
            t = Troop.objects.get(troop_number=self.troop_number.troop_number)
            d = District.objects.get(district_name=t.district)
            return int(d.pk)
        except:
            return 'profile.getdistrictpk error'

    def get_permissions(self):
        try:
            p = PermissionLevel.objects.get(level=self.permissions.level)
            return p.level
        except:
            return 0

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    
    
class EventType(models.Model):
    name = models.CharField(max_length = 255, default = '')
    description = models.TextField(default = '')
    icon = models.FileField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(help_text='Enter a description of the event.')
    event_type = models.ForeignKey(EventType)
    date_start = models.DateTimeField(default = datetime.now)
    date_end = models.DateTimeField(default = datetime.now)
    address = models.CharField(max_length = 500, default = '', help_text='Enter the address of the event')
    coord_x = models.CharField(max_length = 255, default = '', null=True, blank=True)
    coord_y = models.CharField(max_length = 255, default = '', null=True, blank=True)
    google_location = models.CharField(max_length = 300, default = '', null=True, blank=True)
    district = models.ForeignKey(District, default = '0', null=True, blank=True)
    payment_url = models.URLField(default = 'https://www.', null=True, blank=True)
    primary_contact_name = models.CharField(max_length=255, default='')
    primary_contact_info = models.CharField(max_length=255, default='', help_text='(123) 333-4445')
    primary_contact_info_type = models.IntegerField(null=True, blank=True)
    creation_date = models.DateTimeField(default = datetime.now)
    creation_user = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return self.name;

    def get_absolute_url(self):
        url = '/event/' + str(self.id)
        return u'<a href="%s">%s</a>' % (url, str(self.name))

    def get_troop(self):
        #u = self.creation_user
        #t = Troop.objects.get(troop_number=u.profile.get_troop())
        #return t.troop_number

        try:
            t = Troop.objects.get(troop_number=self.creation_user.profile.troop_number.troop_number)
            return t.troop_number
        except:
            return Troop.objects.get(troop_number=0) #'event.gettroop error'


class SearchEvent(models.Model):
    name = models.CharField(max_length = 255, blank=True, null=True)
    description = models.CharField(max_length=255, default = '', blank=True, null=True)
    event_type = models.ForeignKey(EventType, blank=True, null=True)
    date_start = models.DateField(default = '', blank=True, null=True)
    district = models.ForeignKey(District, blank=True, null=True)
    primary_contact_ID = models.ForeignKey(User, blank=True, null=True)


class ListEvent(models.Model):
    event_type = models.ForeignKey(EventType, blank=True, null=True)
    date_start = models.DateField(default = '', blank=True, null=True)
    district = models.ForeignKey(District, blank=True, null=True)


class autofill(models.Model):
    address = models.CharField(max_length=400)