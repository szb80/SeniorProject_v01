
from django.contrib import admin
from .models import EventType, Region, District, Troop, Person, Event, State


admin.site.register(State);

admin.site.register(District);
admin.site.register(Region);
admin.site.register(EventType);

admin.site.register(Troop);

admin.site.register(Person);

admin.site.register(Event);