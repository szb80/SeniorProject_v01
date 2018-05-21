"""
Definition of urls for SeniorProject_v01.
"""

from datetime import datetime
from django.conf.urls import include, url
import django.contrib.auth.views
from django.contrib.auth import views as auth_views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^$', app.views.home, name='home'),
    url(r'^home$', app.views.home, name='home'),
    url(r'^events/$', app.views.events, name='events'),
    url(r'^search$', app.views.search, name='search'),
    url(r'^event/(?P<event_id>[0-9]+)/$', app.views.eventdetail, name='event detail'),
    url(r'^error$', app.views.error, name='error'),

    # TESTING URLS ###########################################################
    url(r'^upcoming$', app.views.upcoming, name='upcoming events'),
    url(r'^eventlist$', app.views.eventlist, name='eventlist'),
    url(r'^loginfb$', app.views.loginfb, name='loginfb'),

    # USER MANAGEMENT URLS ###################################################
     url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html', 
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),

    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    url(r'^register$', app.views.register, name='register'),

    url(r'^admin/', include(admin.site.urls)),
]
