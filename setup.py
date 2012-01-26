from setuptools import setup

setup(
    name='armstrong.base',
    version='0.2.0',
    description='Base functionality that needs to be shared widely',
    author='Texas Tribune',
    author_email='tech@texastribune.org',
    url='http://github.com/texastribune/armstrong.base/',
    packages=[
        'armstrong.base',
        'armstrong.base.templatetags',
        'armstrong.base.tests',
        'armstrong.base.tests.templatetags',
    ],
    namespace_packages=[
        "armstrong",
    ],
    install_requires=[
        'setuptools',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
