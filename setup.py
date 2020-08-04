#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from jazzmin import version

REQUIRED_PYTHON = (3, 5)

setup(
    name='django-jazzmin',
    version=version,
    python_requires='>3.5',
    url='https://github.com/farridav/django-jazzmin',
    description="Drop-in theme for django admin, that utilises AdminLTE 3 & Bootstrap 4 to make yo' admin look jazzy",
    long_description=open('README.rst').read(),
    author='farridav',
    maintainer='farridav',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={},
    install_requires=[
        'django>=2',
    ]
)
