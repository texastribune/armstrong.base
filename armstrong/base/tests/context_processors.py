from django.http import HttpRequest
import fudge
import random

from ._utils import TestCase

from .. import context_processors
from ..context_processors import media_url

class TestOfMediaUrlContextProcessor(TestCase):
    def generate_fake_request(self, is_secure=False):
        request = fudge.Fake(HttpRequest)
        request.has_attr(is_secure=is_secure)
        return request

    def generate_fake_settings_and_result(self, is_secure=False):
        expected_media_url = 'http://example.com/media/%d' % random.randint(100, 200)
        expected_result = {'MEDIA_URL': expected_media_url}
        fake_settings = fudge.Fake()
        if is_secure:
            fake_settings.has_attr(SECURE_MEDIA_URL=expected_media_url)
        else:
            fake_settings.has_attr(MEDIA_URL=expected_media_url)
        return fake_settings, expected_result

    def generate_fake_settings_and_result_with_uploaded(self, is_secure=False):
        fake_settings, expected_result = self.generate_fake_settings_and_result(is_secure=is_secure)
        expected_uploaded_media_url = expected_result['MEDIA_URL'] + "/uploads/"
        fake_settings.has_attr(UPLOADED_MEDIA_URL=expected_uploaded_media_url)
        if is_secure:
            fake_settings.has_attr(SECURE_UPLOADED_MEDIA_URL=expected_uploaded_media_url)
        expected_result['UPLOADED_MEDIA_URL'] = expected_uploaded_media_url
        return fake_settings, expected_result

    def test_returns_media_url_from_settings(self):
        request = self.generate_fake_request()
        fake_settings, expected_result = self.generate_fake_settings_and_result()
        with fudge.patched_context(context_processors, 'settings', fake_settings):
            self.assertEquals(media_url(request), expected_result)

    def test_returns_secure_media_url_from_settings_on_is_secure(self):
        request = self.generate_fake_request(is_secure=True)
        fake_settings, expected_result = self.generate_fake_settings_and_result(is_secure=True)
        with fudge.patched_context(context_processors, 'settings', fake_settings):
            self.assertEquals(media_url(request), expected_result)

    def test_includes_uploaded_media_url_if_present(self):
        request = self.generate_fake_request()
        fake_settings, expected_result = self.generate_fake_settings_and_result_with_uploaded()
        with fudge.patched_context(context_processors, 'settings', fake_settings):
            self.assertEquals(media_url(request), expected_result)

    def test_includes_secure_uploaded_media_url_if_present_and_is_secure(self):
        request = self.generate_fake_request(is_secure=True)
        fake_settings, expected_result = self.generate_fake_settings_and_result_with_uploaded(is_secure=True)
        with fudge.patched_context(context_processors, 'settings', fake_settings):
            self.assertEquals(media_url(request), expected_result)

