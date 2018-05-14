"""
Definition of views.
"""

from django.views.generic.base import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import loader, RequestContext
from django.views import generic
from datetime import datetime
from django.db.models import Q

from .models import Event, District
from .utils import TemplatedCalendar, get_month_day_range
from .filters import EventFilter

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

def eventdetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'app/eventdetail.html', {'event': event, })


def search(request):
    """Renders the filter events page."""
    assert isinstance(request, HttpRequest)
    event_list = Event.objects.all()
    event_filter = EventFilter(request.GET, queryset=event_list)


    #if event_filter:
    #    event_short = [
    #        {
    #            'id': event_filter.id,
    #            'name': event_filter.name
    #        }
    #        for event in event_filter
    #    ]


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


###############################################################################
# TEST VIEWS                                                                  #
###############################################################################


def search2(request):
    """Renders the filter events page."""
    assert isinstance(request, HttpRequest)


    results = BlogPost.objects.filter(Q(title__icontains=your_search_query) | Q(intro__icontains=your_search_query) | Q(content__icontains=your_search_query))





    calendar = TemplatedCalendar()
    month_table = calendar.formatmonth(int(datetime.now().year), int(datetime.now().month), event_list)

    return render(
        request, 
        'app/search2.html', 
        {
            'title':'Search Events',
            'filter': event_filter,
            'month_table': month_table, 
            'event_list': event_list,
            'event_filter': event_filter,
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


