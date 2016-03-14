# -*- coding: utf-8 -*-
from setuptools import setup

long_description = open('README.md').read()

setup(
    name='tissue',
    version='0.1',
    description="your project's issue tracker, in a text file",
    long_description=long_description,
    author=u'Martín Gaitán',
    author_email='gaitan@gmail.com',
    url='https://github.com/mgaitan/tissue',
    license='BSD',
    keywords="github issues tracking bugs markdown",
    packages=['tissue']
    install_requires=['recommonmark', 'pygithub', 'docopt'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
