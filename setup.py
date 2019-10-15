import os
import setuptools
from os import path


README = open(path.join(path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(path.normpath(path.join(path.abspath(__file__), os.pardir)))

setuptools.setup(
    name='django-knockout',
    version='0.4.3',  # major.minor[.patch]
    packages=setuptools.find_packages(),
    install_requires=['django'],
    include_package_data=True,
    zip_safe=False,
    license='Apache',
    description='Generate knockout.js View Models from Django Models.',
    long_description=README,
    url='https://github.com/AntycSolutions/django-knockout',
    author='Rich Jones, Andrew B. Charles',
    author_email='andrew.charles@antyc.ca',
    classifiers=[
        'Development Status :: 2 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
