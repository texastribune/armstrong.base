from django.conf import settings

def secure_url_processor(setting_name):
    '''If the request is secure, replace SETTING with the value of SECURE_SETTING.'''
    secure_setting_name = 'SECURE_' + setting_name
    def processor(request):
        source_setting = secure_setting_name if request.is_secure() else \
            setting_name
        return {setting_name: getattr(settings, source_setting)}
    processor.func_name = setting_name.lower()
    return processor

media_url = secure_url_processor('MEDIA_URL')
static_url = secure_url_processor('STATIC_URL')
