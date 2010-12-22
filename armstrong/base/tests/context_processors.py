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
        media_url_pattern = '%%sexample.com/media/%d/' % random.randint(100, 200)
        fake_settings = fudge.Fake()
        fake_settings.has_attr(**{
            'MEDIA_URL': media_url_pattern % 'http://',
            'SECURE_MEDIA_URL': media_url_pattern % 'https://secure.',
        })
        expected_result = {
            'MEDIA_URL': getattr(fake_settings,
                'SECURE_MEDIA_URL' if is_secure else 'MEDIA_URL'),
        }
        return fake_settings, expected_result

    def generate_fake_settings_and_result_with_uploaded(self, is_secure=False):
        fake_settings, expected_result = self.generate_fake_settings_and_result(is_secure=is_secure)
        uploads_pattern = '%suploads/'
        fake_settings.has_attr(**{
            'UPLOADED_MEDIA_URL': uploads_pattern % fake_settings.MEDIA_URL,
            'SECURE_UPLOADED_MEDIA_URL': uploads_pattern %
                fake_settings.SECURE_MEDIA_URL,
        })
        expected_result['UPLOADED_MEDIA_URL'] = getattr(fake_settings,
            'SECURE_UPLOADED_MEDIA_URL' if is_secure else 'UPLOADED_MEDIA_URL')
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

