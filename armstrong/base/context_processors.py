from django.conf import settings

def media_url(request):
    context = {}
    context['MEDIA_URL'] = request.is_secure() and settings.SECURE_MEDIA_URL or \
            settings.MEDIA_URL
    if hasattr(settings, 'UPLOADED_MEDIA_URL'):
        context['UPLOADED_MEDIA_URL'] = request.is_secure() and \
            settings.SECURE_UPLOADED_MEDIA_URL or \
            settings.UPLOADED_MEDIA_URL

    return context

