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

    """ retrieve events for current month """
    events = Event.objects.filter(date_start__range=(get_month_day_range(datetime.now())))

    calendar = TemplatedCalendar()
    calendar.setfirstweekday(6)
    month_table = calendar.formatmonth(int(datetime.now().year), int(datetime.now().month), events)
    

    return render_to_response(
        'app/events2.html', 
        {
            'title': 'Events',
            'month_table': month_table, 
            'events': events
        }
    )


def buildCalendar(event_list=None):
    """ generates a calendar object with the passed event dictionary """

    calendar = TemplatedCalendar()
    calendar.setfirstweekday(6)

    """ if event_list variable is empty, set events to current month """
    if event_list is not None:
        month_table = calendar.formatmonth(int(datetime.now().year), int(datetime.now().month), event_list)
    else:
        month_table = calendar.formatmonth(int(datetime.now().year), int(datetime.now().month), Event.objects.all())

    return month_table


def eventdetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'app/eventdetail.html', {'event': event, })


def search(request):
    """Renders the filter events page."""
    assert isinstance(request, HttpRequest)
    event_list = Event.objects.all()
    event_filter = EventFilter(request.GET, queryset=event_list)

    calendar = TemplatedCalendar()
    month_table = calendar.formatmonth(int(datetime.now().year), int(datetime.now().month), event_list)

    return render(
        request, 
        'app/search.html', 
        {
            'title':'Search Events',
            'filter': event_filter,
            'month_table': month_table, 
            'event_list': event_list,
            'event_filter': event_filter,
        }
    )


def search2(request):
    """Renders the filter events page."""

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
                q = request.POST['date_start']
                event_list = event_list.filter(date_start__exact=q)

            if 'name' in request.POST and request.POST['name']:
                q = request.POST['name']
                event_list = event_list.filter(name__icontains=q)

            if 'description' in request.POST and request.POST['description']:
                q = request.POST['description']
                event_list = event_list.filter(description__icontains=q)


            month_table = buildCalendar(event_list)

            return render(
                request, 
                'app/search2.html', 
                {
                    'title':'Search Events',
                    'filter': event_list,
                    'month_table': month_table, 
                }
            )

        else:
            return HttpResponseRedirect('/error')

    elif request.method == "GET":
        params = searchform()
        month_table = buildCalendar(Event.objects.all())
        return render(
            request, 
            'app/search2.html', 
            {
                'title':'Search Events',
                'filter': params,
                'month_table': month_table,
            }
        )



"""
###############################################################################
TEST VIEWS                                                                  
###############################################################################
"""

def search3(request):
    assert isinstance(request, HttpRequest)
    event_list = Event.objects.all()
    event_filter = EventFilter(request.GET, queryset=event_list)

    event_list = Event.objects.all()
    event_filter = EventFilter(request.GET, queryset=event_list)
    event_selection = {}

    for event in event_filter.qs:
        {event.ID: event.name}

    """
    {% for doc in filter.qs %}
    <tr>
        <td>{{ doc.department }}</td>
        <td><a href="{{ doc.source_file.url }}" target="_blank">{{ doc.title }}</a></td>
        <td>{{ doc.description }}</td>
    </tr>
    {% endfor %}
    """

    month_table = buildCalendar(request, event_filter)

    """
    results = BlogPost.objects.filter(Q(title__icontains=your_search_query) | Q(intro__icontains=your_search_query) | Q(content__icontains=your_search_query))
    """

    return render(
        request, 
        'app/search2.html', 
        {
            'title':'Search Events',
            'filter': event_filter,
            'month_table': month_table, 
        }
    )

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


