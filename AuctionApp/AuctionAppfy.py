__author__ = 'Bilal'
import re
from django.utils.html import escape

def html_to_content(h):
    return escape(h)

def content_to_html(s):
    s= re.sub('\n','<br>\n',s)
    s= re.sub(
            r'\{\{\w+\}\}',
            (lambda n: '<a href="/' + n.group(0)[2:-2] + '">' + n.group(0)[2:-2] + '</a>' ),
            s)
    return s
