# !/usr/bin/env python

from setuptools import setup

setup(
    name='helpscout-api',
    packages=['helpscout_api'],
    version='0.1.0',
    description='A Python interface to Helpscout API',
    author='Michael Erasmus',
    license='MIT',
    author_email='michael@buffer.com',
    url='https://github.com/bufferapp/helpscout-api',
    keywords=['helpscout'],
    install_requires=['tortilla', 'pandas']
)
