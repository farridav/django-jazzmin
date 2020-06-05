#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from jazzmin import version

setup(
    name='django-jazzmin',
    version=version,
    url='https://github.com/farridav/django-jazzmin',
    description='Django admin theme based adminlte & bootstrap',
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
