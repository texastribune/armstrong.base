from django.http import HttpRequest
import fudge
import random

from ._utils import TestCase

from .. import context_processors
from ..context_processors import media_url, static_url

class TestOfMediaUrlContextProcessor(TestCase):
    def generate_fake_request(self, is_secure=False):
        request = fudge.Fake(HttpRequest)
        request.provides('is_secure').returns(is_secure)
        return request

    def generate_fake_media_settings_and_result(self, is_secure=False):
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

    def test_returns_media_url_from_settings(self):
        request = self.generate_fake_request()
        fake_settings, expected_result = self.generate_fake_media_settings_and_result()
        with fudge.patched_context(context_processors, 'settings', fake_settings):
            self.assertEquals(media_url(request), expected_result)

    def test_returns_secure_media_url_from_settings_on_is_secure(self):
        request = self.generate_fake_request(is_secure=True)
        fake_settings, expected_result = self.generate_fake_media_settings_and_result(is_secure=True)
        with fudge.patched_context(context_processors, 'settings', fake_settings):
            self.assertEquals(media_url(request), expected_result)

    def generate_fake_static_settings_and_result(self, is_secure=False):
        static_url_pattern = '%%sexample.com/static/%d/' % random.randint(100, 200)
        fake_settings = fudge.Fake()
        fake_settings.has_attr(**{
            'STATIC_URL': static_url_pattern % 'http://',
            'SECURE_STATIC_URL': static_url_pattern % 'https://secure.',
        })
        expected_result = {
            'STATIC_URL': getattr(fake_settings,
                'SECURE_STATIC_URL' if is_secure else 'STATIC_URL'),
        }
        return fake_settings, expected_result

    def test_returns_static_url_from_settings(self):
        request = self.generate_fake_request()
        fake_settings, expected_result = self.generate_fake_static_settings_and_result()
        with fudge.patched_context(context_processors, 'settings', fake_settings):
            self.assertEquals(static_url(request), expected_result)

    def test_returns_secure_static_url_from_settings_on_is_secure(self):
        request = self.generate_fake_request(is_secure=True)
        fake_settings, expected_result = self.generate_fake_static_settings_and_result(is_secure=True)
        with fudge.patched_context(context_processors, 'settings', fake_settings):
            self.assertEquals(static_url(request), expected_result)
