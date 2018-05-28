""" used from https://simpleisbetterthancomplex.com/snippet/2016/08/22/dealing-with-querystring-parameters.html """
""" https://gist.github.com/benbacardi/d6cd0fb8c85e1547c3c60f95f5b2d5e1 """

from django import template

register = template.Library()

@register.simple_tag()
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url