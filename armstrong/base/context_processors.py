from django.conf import settings

def media_url(request):
    if request.is_secure:
        return {'MEDIA_URL': settings.SECURE_MEDIA_URL}
    return {'MEDIA_URL': settings.MEDIA_URL}

