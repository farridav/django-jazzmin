#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from adminlteui import version

setup(
    name='django-adminlte-ui',
    version=version,
    url='https://github.com/wuyue92tree/django-adminlte-ui',
    description='django admin theme base on adminlte',
    long_description=open('README.rst').read(),
    author='wuyue',
    author_email='wuyue92tree@163.com',
    maintainer='wuyue',
    maintainer_email='wuyue92tree@163.com',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={},
    install_requires=[
        'django-treebeard==4.3'
    ],
)
