"""
Definition of views.
"""

from django.views.generic.base import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import loader, RequestContext
from django.views import generic
from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import Event, District, SearchEvent
from .utils import TemplatedCalendar, get_month_day_range
from app.forms import searchform

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


def error(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/error.html',
        {
            'title':'Error Page',
            'year':datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def events(request):
    """ defaults to current month """
    assert isinstance(request, HttpRequest)
    
    return render(request,
        'app/events.html', 
        {
            'title': 'Events',
            'month_table': buildCalendar(), 
            'events': events,
        }
    )


def buildCalendar(event_list=None):
    # generates a calendar object with the passed event dictionary
    # accepts a queryset of events
    # returns an instance of TemplatedCalendar() HTMLCalendar

    calendar = TemplatedCalendar()
    calendar.setfirstweekday(6)

    # if event_list variable is empty, set events to current month
    if event_list is not None:  # passed list of events
        month_table = calendar.formatmonth(
            int(datetime.now().year),
            int(datetime.now().month), event_list
            )
    else: # no events passed, default to pull all events for current month
        month_table = calendar.formatmonth(
            int(datetime.now().year),
            int(datetime.now().month),
            Event.objects.filter(date_start__range=(get_month_day_range(datetime.now())))
            )

    return month_table


def eventdetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'app/eventdetail.html', {'event': event, })


def search(request):
    # Renders the filter events page
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        params = searchform(request.POST)
        if params.is_valid():

            if 'district' in request.POST and request.POST['district']:  # REQUIRED FIELD
                q = request.POST['district']
                event_list = Event.objects.filter(district__exact=q)

            if 'event_type' in request.POST and request.POST['event_type']:
                q = request.POST['event_type']
                event_list = event_list.filter(event_type__exact=q)

            if 'date_start' in request.POST and request.POST['date_start']: #################################################################
                if request.POST.get('date_start_month') is not '0' and request.POST.get(date_start_day) is not '0' and request.POST.get(date_start_year) is not '0':
                    m = request.POST.get('date_start_month')
                    d = request.POST.get('date_start_day')
                    y = request.POST.get('date_start_year')
                
                    search_date = datetime.date(y, m, d)

                    event_list = event_list.filter(search_date__exact=q)

            if 'name' in request.POST and request.POST['name']:
                q = request.POST['name']
                event_list = event_list.filter(name__icontains=q)

            if 'description' in request.POST and request.POST['description']:
                q = request.POST['description']
                event_list = event_list.filter(description__icontains=q)

            month_table = buildCalendar(event_list)

            return render(
                request, 
                'app/search.html', 
                {
                    'title':'Search Events',
                    'filter': event_list,
                    'month_table': month_table,
                    #'date': search_date,
                }
            )

        else:
            return HttpResponseRedirect('/error')

    elif request.method == "GET":
        params = searchform()
        month_table = buildCalendar()
        return render(
            request, 
            'app/search.html', 
            {
                'title':'Search Events',
                'filter': params,
                'month_table': month_table,
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
                request.session.set_expiry(86400) #sets the exp. value of the session 
                login(request, user) #the user is now logged in

        return HttpResponseRedirect('/events')