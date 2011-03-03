import re
import urlparse

from django import template
register = template.Library()


class HighlightedSearchTermNode(template.Node):
    def __init__(self, text):
        self.text = template.Variable(text)

    def render(self, context):
        text = self.text.resolve(context)

        # TODO: handle no request variable in context
        request = context['request']

        if not 'HTTP_REFERER' in request.META:
            return text

        referer = urlparse.urlparse(request.META['HTTP_REFERER'])
        query = urlparse.parse_qs(referer.query)
        if not 'q' in query:
            return text
        q = query['q'][0]

        replacement = r'<span class="search_term">\1</span>'
        return re.sub(r'(?i)(%s)' % q, replacement, text)


@register.tag
def highlight_search_terms(parser, token):
    bits = token.split_contents()
    return HighlightedSearchTermNode(bits[1])
