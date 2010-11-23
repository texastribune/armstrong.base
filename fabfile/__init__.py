from ._utils import *

@task
def test():
    settings = {
        'INSTALLED_APPS': (
            'armstrong.base',
        ),
    }
    run_tests(settings, 'base')

