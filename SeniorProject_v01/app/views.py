"""
Definition of views.
"""


from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader, RequestContext
from django.views import generic
from datetime import datetime

from .models import Event

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
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/events.html',
        {
            'title':'Events',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def upcoming(request):
    """Displays all upcoming Events after the current date"""
    upcoming = Event.objects.order_by('date_start')
    template = loader.get_template('app/upcoming.html')
    context = { 'upcoming': upcoming, }
    return HttpResponse(template.render(context, request))

def eventlist(request):
    """Displays all Events after the current date"""
    eventlist = Event.objects.order_by('name')
    template = loader.get_template('app/eventlist.html')
    context = { 'eventlist': eventlist, }
    return HttpResponse(template.render(context, request))

def eventdetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'app/eventdetail.html', {'event': event, })

def backend_events(request, start, end):
    # set SQL statement
    # bind post parameter to local variables
    # execute the saved SQL statement
    # save the result to a local variable
    # make an Event class array
    # split the result line items and create new Event objects, add to array
    # JSON the result array back

    result = Event.objects.filter(date_start__gte=start, date_end__lte=end)
    
    context = { 'result': result, }

    template = loader.get_template('app/eventlist.html')

    return HttpResponse(template.render(context, request))




    #    $.post(
    #    // URL to POST to
    #    "backend_events.php",
    #    // {} data set to send in request
    #    {
    #        start: start.toString()
    #        , end: end.toString()
    #    },
    #    // function to perform once data is received back
    #    function(data) {
    #        //console.log(data);
    #        // send received data to dp receiver
    #        dp.events.list = data;
    #        // run calendar update
    #        dp.update();
    #    }
    #)
