import fudge
import urllib

from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import SafeData

from .._utils import TestCase
from ...templatetags import text_helpers


def generate_random_request(match="some",
                            url_template="http://localhost/?q=%s"):
    request = fudge.Fake()
    request.has_attr(META={"HTTP_REFERER": url_template % match})
    fudge.clear_calls()
    return request


def generate_random_request_and_context(text, match="some",
                            url_template="http://localhost/?q=%s"):
    request = generate_random_request(match=match, url_template=url_template)
    context = {
        "request": request,
        "text": text,
    }
    return request, context


class HelloWorld(TestCase):
    def test_data_returns_is_marked_as_safe(self):
        text = "This is some text"
        request, context = generate_random_request_and_context(text)

        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        self.assertIsInstance(result, SafeData)

    def test_gracefully_returns_when_lacking_request_object(self):
        text = "This is some text"
        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render({"text": text})
        self.assertEqual(text, result)

    def test_raises_exception_when_debug_is_on(self):
        settings = fudge.Fake()
        settings.has_attr(DEBUG=True)

        text = "This is some text"
        node = text_helpers.HighlightedSearchTermNode("text")

        with fudge.patched_context(text_helpers, 'settings', settings):
            self.assertRaises(ImproperlyConfigured, node.render, {"text": text})

    def test_works_with_referrers_with_no_q_get_param(self):
        text = "This is some text"
        request, context = generate_random_request_and_context(
                "", url_template="http://localhost/%s", match="")
        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render({"text": text})
        self.assertEqual(text, result)

    def test_replaces_words_with_highlighted_word(self):
        text = "This is some text"
        request, context = generate_random_request_and_context(text)

        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)

        expected = 'This is <span class="search_term">some</span> text'
        self.assertEqual(expected, result)

    def test_can_handle_mismatched_case(self):
        text = "This is SOME text"
        request, context = generate_random_request_and_context(text)

        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        expected = 'This is <span class="search_term">SOME</span> text'
        self.assertEqual(expected, result)

    def test_can_handle_mixed_case(self):
        text = "This is Some TeXT"
        request, context = generate_random_request_and_context(text,
                                                               match="text")

        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        expected = 'This is Some <span class="search_term">TeXT</span>'
        self.assertEqual(expected, result)

    def test_matches_spaces_as_urlencoded_values(self):
        text = "This is some text"
        match = '%20text'
        request, context = generate_random_request_and_context(text,
                                                               match=match)
        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        expected = 'This is some<span class="search_term"> text</span>'
        self.assertEqual(expected, result)

    def test_matches_spaces_as_pluses(self):
        text = "This is some text"
        match = '+text'
        request, context = generate_random_request_and_context(text,
                                                               match=match)
        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        expected = 'This is some<span class="search_term"> text</span>'
        self.assertEqual(expected, result)

    def test_matches_spaces(self):
        text = "This is some text"
        match = ' text'
        request, context = generate_random_request_and_context(text,
                                                               match=match)
        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        expected = 'This is some<span class="search_term"> text</span>'
        self.assertEqual(expected, result)

    def test_matches_numbers(self):
        text = "This is some0text"
        match = '0text'
        request, context = generate_random_request_and_context(text,
                                                               match=match)
        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        expected = 'This is some<span class="search_term">0text</span>'
        self.assertEqual(expected, result)

    def test_matches_underscores(self):
        text = "This is some_text"
        match = '_text'
        request, context = generate_random_request_and_context(text,
                                                               match=match)
        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        expected = 'This is some<span class="search_term">_text</span>'
        self.assertEqual(expected, result)

    def test_matches_hyphens(self):
        text = "This is some-text"
        match = '-text'
        request, context = generate_random_request_and_context(text,
                                                               match=match)
        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        expected = 'This is some<span class="search_term">-text</span>'
        self.assertEqual(expected, result)


    def test_only_responds_to_a_subset_of_characters(self):
        text = "<p>This is some text</p>"
        match = urllib.quote("<p")
        request, context = generate_random_request_and_context(text,
                                                               match=match)
        node = text_helpers.HighlightedSearchTermNode("text")
        result = node.render(context)
        self.assertEqual(text, result)
