#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Read requirements from the requirements.txt file
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

# Read README and HISTORY files
with open('README.md', 'r', encoding='utf-8') as rm_file:
    readme = rm_file.read()

with open('HISTORY.md', 'r', encoding='utf-8') as hist_file:
    history = hist_file.read()

setup(
    name='mega.py',
    version='1.0.57.dev0',
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/kagut57/mega.py/',
    description='Python library for the Mega.co.nz API',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    author="O'Dwyer Software",
    author_email='hello@odwyer.software',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    install_requires=install_requires,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
