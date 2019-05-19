#! /usr/bin/env python

from distutils.core import setup

setup(
    name='idlechk',
    author='Richard Neumann',
    author_email='<mail at richard dash neumann dot de>',
    packages=[
        'mcipc',
        'mcipc.query',
        'mcipc.query.proto',
        'mcipc.rcon',
        'mcipc.rcon.datastructures'],
    scripts=['files/rconclt', 'files/rconshell'],
    url='https://github.com/conqp/idlechk',
    license='GPLv3',
    description='A system service to check whether the system is idle.')
