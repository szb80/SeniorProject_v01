"""
Definition of urls for SeniorProject_v01.
"""

from datetime import datetime
from django.conf.urls import include, url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    # Examples:
   
    url(r'^events/$', app.views.events, name='events'),
    url(r'^search$', app.views.search, name='search'),
    url(r'^event/(?P<event_id>[0-9]+)/$', app.views.eventdetail, name='event detail'),


    # TESTING URLS #########################################################################################
    url(r'^upcoming$', app.views.upcoming, name='upcoming events'),
    url(r'^eventlist$', app.views.eventlist, name='eventlist'),
    url(r'^search2$', app.views.search2, name='search2'),





    url(r'^loginfb$', app.views.loginfb, name='loginfb'),
    #url(r'^about', app.views.about, name='about'),
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
    url(r'^$', django.contrib.auth.views.login,
        
        {
                    
            'template_name': 'app/index.html', 
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            },
       
        name='home'),
    

    #url(r'^accounts/login/$', include(django.contrib.auth.views.login)),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
