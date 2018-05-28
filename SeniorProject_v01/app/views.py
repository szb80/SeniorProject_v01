"""
Definition of views.
"""

from django.views.generic.base import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import loader, RequestContext
from django.views import generic
from datetime import datetime, date
from django.utils.timezone import get_current_timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Event, District, SearchEvent
from .utils import TemplatedCalendar, get_month_day_range
from app.forms import searchform, createform


###############################################################################
# UTILITY FUNCTIONS
###############################################################################

def validateMonthYear(month, year):
    # checks if a month and year are valid
    # returns boolean True is they are valid
    try:
        # is month in a valid range?
        if int(month) not in range(0, 13):
            return False  # nope!
        # is year in a valid range?
        if int(year) not in range(2000, 2501):
            return False  # nope!
    except TypeError:  # catch non-int type exceptions
        return False
    return True  # passes all tests, is valid


def setCurrentMonthYear():
    # returns two variables 'month', 'year' as int
    # with values of the current month and year
    return int(datetime.now().month), int(datetime.now().year)


def buildCalendar(request, month=None, year=None):
    # generates a calendar object with the passed event dictionary
    # accepts a queryset of events
    # returns an instance of TemplatedCalendar() HTMLCalendar
    assert isinstance(request, HttpRequest)

    calendar = TemplatedCalendar()
    calendar.setfirstweekday(6)

    # if date range is not valid, set to current month #####################################################################
    if not validateMonthYear(month, year):
        month, year = setCurrentMonthYear()
    
    month_table = calendar.formatmonth(
        int(year),
        int(month), 
        Event.objects.filter(date_start__range=(get_month_day_range(date(int(year), int(month), 1))))
        )

    return month_table


###############################################################################
# LOGIN VIEWS
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


def login(request):
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
            'title':'Home Page',
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

    # if date range is not valid, set to current month
    if not validateMonthYear(month, year):
        month, year = setCurrentMonthYear()

    month = request.GET.get('month')
    year = request.GET.get('year')
    
    return render(request,
        'app/events.html', 
        {
            'title': 'Events',
            'month_table': buildCalendar(request, month, year), 
            'events': events,
        }
    )


def eventdetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'app/eventdetail.html', {'event': event, })


def search(request, month=None, year=None):
    # Renders the filter events page
    assert isinstance(request, HttpRequest)

    params = searchform()
    month_table = buildCalendar(request)  # default current month
    event_list = Event.objects.filter(date_start__range=(get_month_day_range(datetime.now())))

    if request.method == "GET":
        params = searchform(request.GET)
        if params.is_valid():
            if 'district' in request.GET and request.GET['district']:  # REQUIRED FIELD
                q = request.GET['district']
                event_list = Event.objects.filter(district__exact=q)

            if 'event_type' in request.GET and request.GET['event_type']:
                q = request.GET['event_type']
                event_list = event_list.filter(event_type__exact=q)

            if 'date_start_month' in request.GET and request.GET['date_start_month']:
                if request.GET.get('date_start_month') is not '0':
                    search_date = date(int(request.GET.get('date_start_year')), 
                                        int(request.GET.get('date_start_month')),
                                        int(request.GET.get('date_start_day')))
                    event_list = Event.objects.filter(date_start__contains=search_date)

            if 'name' in request.GET and request.GET['name']:
                q = request.GET['name']
                event_list = event_list.filter(name__icontains=q)

            if 'description' in request.GET and request.GET['description']:
                q = request.GET['description']
                event_list = event_list.filter(description__icontains=q)

        month_table = buildCalendar(event_list)

        #else: # searchform is invalid
            #return HttpResponseRedirect('/error')l

    return render(
        request, 
        'app/search.html', 
        {
            'title':'Search Events',
            'filter': params,
            'month_table': month_table,
        }
    )


@login_required
def create(request):
    if request.user.has_perm('app.event.add'):
        if request.method == "POST":
            form = createform(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.save()
                return HttpResponseRedirect('/events')
            else:
                return HttpResponseRedirect('/error')

        elif request.method == "GET":
            form = createform()
            return render(request, "app/create.html", {'form': form})
    else:
        return render(
            request,
            'app/error.html',
            {
                'title': 'Error Page',
                'year': datetime.now().year,
                'error_code': 'Permission Denied',
                'error_msg': 'You do not have permission to access this page.',
            }
        )



def register(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Register a new account',
            'year':datetime.now().year,
        }
    )


###############################################################################
# TEST VIEWS
###############################################################################

def eventlist(request):
    """Displays all Events after the current date"""
    eventlist = Event.objects.order_by('name')
    template = loader.get_template('app/eventlist.html')
    context = { 'eventlist': eventlist, }
    return HttpResponse(template.render(context, request))


def upcoming(request):
    """Displays all upcoming Events after the current date"""
    upcoming = Event.objects.filter(date_start__gte=datetime.now()).order_by('date_start')
    template = loader.get_template('app/upcoming.html')
    context = { 'upcoming': upcoming, }
    return HttpResponse(template.render(context, request))
