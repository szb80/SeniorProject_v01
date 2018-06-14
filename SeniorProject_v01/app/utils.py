""" Modified from https://github.com/anentropic/django-tempocal """

import sys
import datetime, calendar
from calendar import HTMLCalendar, day_abbr, month_name, January
from django.template.loader import render_to_string

from app.models import Event

class TemplatedCalendar(HTMLCalendar):

    templates = {
        'day': 'tempocal/day.html',
        'week': 'tempocal/week.html',
        'weekday': 'tempocal/weekday.html',
        'weekheader': 'tempocal/weekheader.html',
        'monthname': 'tempocal/monthname.html',
        'month': 'tempocal/month.html',
        'year': 'tempocal/year.html',
        'yearpage': 'tempocal/yearpage.html',
        'emptymonth': 'tempocal/emptymonth.html',
    }

    def nextMonthYear(self, month, year):
        # returns the next month and year for a given month/year pair as int
        # increment month and return same year
        if month < 12:
            return month + 1, year
        # reset month to 1 and increment year
        elif month is 12:
            return 1, year + 1

    def prevMonthYear(self, month, year):
        # returns the prev month and year for a given month/year pair as int
        # decrement month and return same year
        if month > 1:
            return month - 1, year
        # reset month to 1 and increment year
        elif month is 1:
            return 12, year - 1

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        if day == 0:
            css_class = 'noday'
        else:
            css_class = self.cssclasses[weekday]
            
        events_str = ''
       
        # Apply CSS to calendar to highlight current day
        #if day == datetime.datetime.now().day:
        #    css_class += ' highlighted' 
        
        for event in events:
            if str(event.date_start.day) <= str(day) and str(event.date_end.day) >= str(day):
                events_str += '<div class="event-inner">'
                events_str += event.get_absolute_url()
                events_str += '</div>'

        return render_to_string(
            self.templates['day'],
            {
                'css_class': css_class,
                'day': day,
                'events_str': str(events_str),
            }
        )

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        return render_to_string(
            self.templates['week'],
            {
                'days': [self.formatday(d, wd, events) for (d, wd) in theweek],
            })

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return render_to_string(
            self.templates['weekday'],
            {
                'css_class': self.cssclasses[day],
                'day': day_abbr[day],
            })

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        return render_to_string(
            self.templates['weekheader'],
            {
                'days': [self.formatweekday(i) for i in self.iterweekdays()],
            })

    def formatmonthname(self, theyear, themonth, withyear=True):
        """
        Return a month name as a table row.
        """
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]

        return render_to_string(
            self.templates['monthname'],
            {
                'month_name': s,
            })

    # ------------ FORMATMONTH() FUNCTION ------------- #
    def formatmonth(self, theyear, themonth, events, withyear=True):
        """
        Return a formatted month as a table.
        """

        monthPP, yearPP = self.nextMonthYear(themonth, theyear)
        monthMM, yearMM = self.prevMonthYear(themonth, theyear)

        return render_to_string(
            self.templates['month'],
            {
                'monthPP': monthPP,
                'yearPP': yearPP,
                'monthMM': monthMM,
                'yearMM': yearMM,
                'month_name_row': self.formatmonthname(
                    theyear, themonth, withyear=withyear
                ),
                'week_header_row': self.formatweekheader(),
                'week_rows': [
                    self.formatweek(week, events)
                    for week in self.monthdays2calendar(theyear, themonth)
                ]
            }
        )

    def formatyear(self, theyear, width=3):
        """
        Return a formatted year as a table of tables.
        """
        rows = []
        for i in xrange(January, January + 12, width):
            row = []
            for m in xrange(i, 13):
                if m > i + width:
                    # this is new logic compared to HTMLCalendar, which would
                    # just not output any TD cells after the end of months in
                    # range. if you want that behaviour then have an empty
                    # template, or delete the template item from
                    # self.templates. Otherwise you can render emptymonth.html
                    if 'emptymonth' in self.templates:
                        row.append(
                            render_to_string(self.templates['emptymonth'])
                        )
                    else:
                        row.append(None)
                else:
                    row.append(self.formatmonth(theyear, m, withyear=False))
            rows.append(row)

        return render_to_string(
            self.templates['year'],
            {
                'colspan': max(width, 1),
                'year': theyear,
                'rows': rows,
            })

    def formatyearpage(self, theyear, width=3, css='calendar.css',
                       encoding=None):
        """
        Return a formatted year as a complete HTML page.
        """
        if encoding is None:
            encoding = sys.getdefaultencoding()

        return render_to_string(
            self.templates['yearpage'],
            {
                'encoding': encoding,
                'css': css,
                'theyear': theyear,
                'year': self.formatyear(theyear, width),
            })


def get_month_day_range(date):
    """ used from https://gist.github.com/waynemoore/1109153#gistcomment-1193720 """
    """
    For a date 'date' returns the start and end date for the month of 'date'.

    Month with 31 days:
    >>> date = datetime.date(2011, 7, 27)
    >>> get_month_day_range(date)
    (datetime.date(2011, 7, 1), datetime.date(2011, 7, 31))

    Month with 28 days:
    >>> date = datetime.date(2011, 2, 15)
    >>> get_month_day_range(date)
    (datetime.date(2011, 2, 1), datetime.date(2011, 2, 28))
    """
    first_day = date.replace(day = 1)
    last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1])
    return first_day, last_day

def date():
    date = datetime.datetime.now()
    day = date.day 

    return day


