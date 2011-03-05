import re
import urlparse

from django.conf import settings
from django.template.defaultfilters import mark_safe
from django.template.defaultfilters import stringfilter
from django import template
register = template.Library()


@register.filter
@stringfilter
def highlight_text(text, q):
    if re.match(r"[^a-z0-9 _-]", q):
        return text

    replacement = r'<span class="search_term">\1</span>'
    return mark_safe(re.sub(r'(?i)(%s)' % q, replacement, text))


class HighlightedSearchTermNode(template.Node):
    def __init__(self, text):
        self.text = template.Variable(text)

    def render(self, context):
        text = self.text.resolve(context)

        if not "request" in context:
            if settings.DEBUG:
                from django.core.exceptions import ImproperlyConfigured
                raise ImproperlyConfigured
            return text
        request = context['request']

        if not 'HTTP_REFERER' in request.META:
            return text

        referer = urlparse.urlparse(request.META['HTTP_REFERER'])
        query = urlparse.parse_qs(referer.query)
        if not 'q' in query:
            return text
        q = query['q'][0]

        return highlight_text(text, q)


@register.tag
def highlight_search_terms(parser, token):
    bits = token.split_contents()
    return HighlightedSearchTermNode(bits[1])
