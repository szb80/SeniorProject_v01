
from django.contrib import admin
from .models import EventType, Region, District, Troop, Profile, Event, State, PermissionLevel

admin.site.register(State);

admin.site.register(District);
admin.site.register(Region);
admin.site.register(EventType);

admin.site.register(Troop);

admin.site.register(Profile);

admin.site.register(Event);

admin.site.register(PermissionLevel);