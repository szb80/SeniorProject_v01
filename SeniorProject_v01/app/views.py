"""
Definition of views.
"""
from django.contrib import messages

import requests, json

from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.views.generic.base import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import loader, RequestContext
from django.views import generic
from django.views.generic import UpdateView
from django.conf import settings
from datetime import datetime, date, time
from django.utils.timezone import get_current_timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Event, District, SearchEvent, Troop
from .utils import TemplatedCalendar, get_month_day_range
from app.forms import searchform, createform, editForm, listform
from app.templatetags import in_group
import googlemaps

from app.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from bootstrap_datepicker_plus import DateTimePickerInput


###############################################################################
# UTILITY FUNCTIONS
###############################################################################
def validateMonthYear(month, year):
    # checks if a month and year are valid
    # returns boolean True is they are valid
    try:
        # is month in a valid range?
        if int(month) not in range(1, 13):
            return False  # nope!
        # is year in a valid range?
        if int(year) not in range(1999, 2501):
            return False  # nope!
        else:
            return True
    except TypeError:  # catch non-int type exceptions
        return False


def setCurrentMonthYear():
    # returns two variables 'month', 'year' as int
    # with values of the current month and year
    return int(datetime.now().month), int(datetime.now().year)


def buildCalendar(request, month=None, year=None, params=None):
    # generates a calendar object
    # returns an instance of TemplatedCalendar() HTMLCalendar

    # default to current month, then overwrite if request is different
    setmonth = datetime.now().month
    setyear = datetime.now().year

    # check if request parameters are valid and set local variables
    if validateMonthYear(request.GET.get('month'), request.GET.get('year')):
        setmonth = request.GET.get('month')
        setyear = request.GET.get('year')
    elif validateMonthYear(month, year):
        setmonth = month
        setyear = year

    # if search for month, make calendar for that month
    if 'date_start_month' in request.GET and request.GET['date_start_month'] is not '0':
        setmonth = request.GET.get('date_start_month')

    # if search includes year, make calendar for that year
    if 'date_start_year' in request.GET and request.GET['date_start_year'] is not '0':
        setyear = request.GET.get('date_start_year')

    # create calendar instance and perform initial formatting
    calendar = TemplatedCalendar()
    calendar.setfirstweekday(6) # start on sunday
    
    # no searchform provided, create dict with date to render
    if not params:
        params = {'month': setmonth,
                  'year': setyear,
                  }

    # build calendar with cleaned date
    month_table = calendar.formatmonth(
        int(setyear),
        int(setmonth), 
        getEvents(request, params),
        )

    return month_table


def getEvents(request, params=None):
    # receives request
    # returns QuerySet of Events matching date and parameters

    # get date of interest
    if params:
        month = params['month']
        year = params['year']

    # default to all events in given month
    # initialize eventList before applying any filtering logic
    eventList = Event.objects.filter(date_start__range=(get_month_day_range(date(int(year), int(month), 1))))

    # if no search filters provided, return month from request
    if not params:
        return eventList

    # if request is GET from the search page, apply filtering on parameters
    if request.method == "GET":
        if params:
            if 'district' in request.GET and request.GET['district']:  # REQUIRED FIELD
                q = request.GET['district']
                eventList = eventList.filter(district__exact=q)

            if 'event_type' in request.GET and request.GET['event_type']:
                q = request.GET['event_type']
                eventList = eventList.filter(event_type__exact=q)

            if 'date_start_month' in request.GET and request.GET['date_start_month'] is not '0':
                if request.GET.get('date_start_day') is not '0':
                    if request.GET.get('date_start_year') is not '0':
                        search_date = date(int(request.GET.get('date_start_year')), 
                                            int(request.GET.get('date_start_month')),
                                            int(request.GET.get('date_start_day')))
                        eventList = eventList.filter(date_start__contains=search_date)

            if 'name' in request.GET and request.GET['name']:
                q = request.GET['name']
                eventList = eventList.filter(name__icontains=q)

            if 'description' in request.GET and request.GET['description']:
                q = request.GET['description']
                eventList = eventList.filter(description__icontains=q)

        return eventList


###############################################################################
# LOGIN AND SIGNUP VIEWS
###############################################################################

def loginfb(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/login-fb.html',
        {
            'title':'Facebook Login',
            'message':'Login using your Facebook account.',
            'year':datetime.now().year,
        }
    )


def login(request,user):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        username = request.POST.get('id_username','')
        password = request.POST.get('id_password','')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                request.session.set_expiry(86400) # sets the exp. value of the session 
                login(request, user) # the user is now logged in

        return HttpResponseRedirect('/events')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Successful Signup..')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'app/user_registration.html', {'title': 'Sign up', 'form': form})


###############################################################################
# OPERATIONAL VIEWS
###############################################################################

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home',
            'year':datetime.now().year,
        }
    )


def error(request, error_code=None, error_msg=None):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    if not error_code:
        error_code = 'Error'

    if not error_msg:
        error_msg = "We can't make that work :("

    return render(
        request,
        'app/error.html',
        {
            'title': 'Error Page',
            'year': datetime.now().year,
            'error_code': error_code,
            'error_msg': error_msg,
        }
    )


def events(request, month=None, year=None):
    """ displays a calendar of events and defaults to current month """
    assert isinstance(request, HttpRequest)

    return render(request,
        'app/events.html', 
        {
            'title': 'Calendar',
            'month_table': buildCalendar(request), 
        }
    )



def upcoming(request):
    """Displays all upcoming Events after the current date"""
    upcoming = Event.objects.filter(date_start__gte=datetime.now()).order_by('date_start')

    if request.method == "GET":
        filters = listform(request.GET)
        
        if 'district' in request.GET and request.GET['district']:
            district = request.GET['district']
            upcoming = upcoming.filter(district__exact=district)
        if 'event_type' in request.GET and request.GET['event_type']:
            event_type = request.GET['event_type']
            upcoming = upcoming.filter(event_type__exact=event_type)

        eventList = [dict(id=e.pk, name=e.name) for e in upcoming]

    else: # searchform is invalid or not submitted yet
        filters = listform()
        
    return render(
        request, 
        'app/upcoming.html', 
        {
            'title':'Upcoming Events',
            'upcoming': upcoming,
            'filters': filters,
        }
    )


@login_required
def eventdetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    url = 'https://www.google.com/maps/dir/?api=1&destination='
    place = event.address
    place = place.replace(" ", "+")
    url += place
    et = Event.objects.get(pk=event_id).get_troop()

    try:
        p = request.user.profile.get_permissions()
        ut = request.user.profile.get_troop()
    except AttributeError:  # catch AnonymousUser or user not logged in
        p = 0
        ut = Troop.objects.get(troop_number=0)

    return render(request,
                  'app/eventdetail.html',
                  {
                      'title': event.name,
                      'event': event,
                      'url': url,
                      'permissions': p,
                      'event_troop': et,
                      'user_troop': ut,
                  }
                  )


def search(request, month=None, year=None):
    # Renders the search events page

    assert isinstance(request, HttpRequest)

    if request.method == "GET":
        searchParams = searchform(request.GET)
        month_table = buildCalendar(request, searchParams)

    else: # searchform is invalid or not submitted yet
        searchParams = searchform()
        month_table = buildCalendar(request)  # default current month

    return render(
        request, 
        'app/search.html', 
        {
            'title':'Search',
            'filter': searchParams,
            'month_table': month_table,
        }
    )


@login_required
def create(request):
    # displays the "Create Event" page for users to create a new event

    # deny all access to non-admins
    if request.user.profile.get_permissions() < 2:
        return render(
            request,
            'app/error.html',
            {
                'title': 'Error Page',
                'year': datetime.now().year,
                'error_code': 'Permission Denied',
                'error_msg': 'You are not authorized to create events. Only designated troop leaders may add events. Contact your Troopmaster if you have an activity you wish to add to the calendar.',
            }
        )

    # initialize google maps instance
    gmaps = googlemaps.Client(key='AIzaSyA0aaavBcFWIBvn3Tnu86BYOpKHqYVqKR8')

    # pull permissions and districts for selected user
    p = request.user.profile.get_permissions()
    d = request.user.profile.get_district()

    if request.method == "POST":
        form = createform(request.POST, district=d, permissions=p)

        # process form if valid
        if form.is_valid():
            form = form.save(commit=False)

            # process geocode address
            geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(form.address)
            geocode_url = geocode_url + "&key={}".format(settings.GOOGLE_MAPS_API)
            results = requests.get(geocode_url)
            results = results.json()
            geocode_result = results['results'][0]
            # process geocode coordinates
            form.coord_x = geocode_result.get('geometry').get('location').get('lat')
            form.coord_y = geocode_result.get('geometry').get('location').get('lng')
            google_location = geocode_result.get('place_id')

            if 'date_start' in request.POST and request.POST['date_start']:
                form.date_start = datetime.strptime(request.POST['date_start'], "%m/%d/%Y %H:%M")

            if 'date_end' in request.POST and request.POST['date_end']:
                form.date_end = datetime.strptime(request.POST['date_end'], "%m/%d/%Y %H:%M")

            # interpret and assign primary contact info type
            type = 0  # default to none type
            if 'primary_contact_info_type1' in request.POST and request.POST['primary_contact_info_type1']:
                type = 1
            elif 'primary_contact_info_type2' in request.POST and request.POST['primary_contact_info_type2']:
                type = 2
            form.primary_contact_info_type = type

            # set owner to current user
            form.creation_date = datetime.now();
            form.creation_user = request.user

            form.save()
            return HttpResponseRedirect('/events')


        #else: # unhandled form error - DEBUG ONLY
        #    return render(
        #        request,
        #        'app/testpage.html',
        #        {
        #            'form': form,
        #            'district': request.user.profile.get_district(),
        #            'districtpk': request.user.profile.get_district_pk(),
        #            'troop': request.user.profile.get_troop(),
        #        }
        #    )

        else:
            return HttpResponseRedirect('/error')

    # new form
    elif request.method == "GET":
        form = createform(district=d, permissions=p)
        return render(request,
                      "app/create.html",
                      {
                          'title': 'Create New Event',
                          'form': form,
                          'permissions': request.user.profile.get_permissions(),
                      }
                      )


class EditEvent(UpdateView):
    model = Event
    #fields = ['name',
    #            'description',
    #            'address',
    #            'event_type',
    #            'payment_url',
    #            'primary_contact_name',
    #            'primary_contact_info',
    #            'coord_x',
    #            'coord_y',
    #            'google_location',
    #            ]
    form_class = editForm
    template_name = 'app/event_update.html'

    # test for user admin permissions
    # return boolean for if user is admin or not
    def get_admin_permissions(self, request):
        try:
            if request.user.profile.get_permissions() >= 2:
                return True
            return False
        except AttributeError:  # catch AnonymousUser or user not logged in
            return False

    # override dispatch method and test for request.user permissions and redirect as appropriate
    def dispatch(self, request, *args, **kwargs):
        if not self.get_admin_permissions(request):
            return render(
                request,
                'app/error.html',
                {
                    'title': 'Error Page',
                    'year': datetime.now().year,
                    'error_code': 'Permission Denied',
                    'error_msg': 'You are not authorized to edit events. Only designated troop leaders may modify events. Contact your Troopmaster or the event contact if you see an error in a listing.',
                }
            )

        return super(EditEvent, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('eventdetail', kwargs={
            'event_id': self.object.pk,
        })


###############################################################################
# USER ACCOUNTS VIEWS
###############################################################################

def signup(request):
    if request.user.is_authenticated:
        return redirect('/home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            

            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('app/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'app/user_confirmation.html')
    else:
        form = SignupForm()
    return render(request, 'app/user_registration.html', {'form': form})


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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'app/successful_confirmation.html')
    else:
        return render(request, 'app/invalid_activation.html')



###############################################################################
# TEST VIEWS
###############################################################################

def eventlist(request):
    """Displays all Events after the current date"""
    eventlist = Event.objects.order_by('name')
    template = loader.get_template('app/eventlist.html')
    context = { 'eventlist': eventlist, }
    return HttpResponse(template.render(context, request))


def test(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    p = request.user.profile.get_permissions()
    e = Event.objects.get(id=24)

    return render(
        request,
        'app/testpage.html',
        {
            'title':'Test Page',
            'year':datetime.now().year,
            'permissions': p,
            'district': request.user.profile.get_district(),
            'districtpk': request.user.profile.get_district_pk(),
            'troop': request.user.profile.get_troop(),
            'event': e,
            'eventtroop': e.get_troop(),
        }
    )

