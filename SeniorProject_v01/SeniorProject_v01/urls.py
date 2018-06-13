from datetime import datetime
from django.conf.urls import include, url
import django.contrib.auth.views
from django.contrib.auth import views as auth_views

import app.views as core_views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', app.views.home, name='home'),
    url(r'^home$', app.views.home, name='home'),
    url(r'^events', app.views.events, name='events'),
    url(r'^search$', app.views.search, name='search'),
    url(r'^event/(?P<event_id>[0-9]+)/$', app.views.eventdetail, name='eventdetail'),
    url(r'^upcoming$', app.views.upcoming, name='upcoming'),    
    url(r'^event/edit/(?P<pk>\d+)/$', app.views.EditEvent.as_view(), name='editevent'),
    url(r'^create$', app.views.create, name='create'),
    url(r'^error$', app.views.error, name='error'),
   
   # USER REGISTRATION URLS ##################################################
    url(r'^signup/$', app.views.signup,  name='signup'),
    url(r'^confirm_email/$', app.views.signup,  name='user_confirmation'),
    url(r'^successful_confirmation/$', app.views.signup,  name='successful_confirmation'),
    url(r'^invalid_activation_link/$', app.views.signup,  name='invalid_activation'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        app.views.activate, name='activate'),

    # USER PASSWORD RESET URLS ##################################################
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),


    # TESTING URLS ###########################################################
  
    url(r'^eventlist$', app.views.eventlist, name='eventlist'),
    url(r'^test', app.views.test, name='test'),



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

    url(r'^admin/', include(admin.site.urls)),
]
