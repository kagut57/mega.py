#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
from codecs import open

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as rm_file:
    readme = rm_file.read()

with open('HISTORY.md', 'r', encoding='utf-8') as hist_file:
    history = hist_file.read()

setup(name='mega.py',
      version='1.0.9.dev0',
      python_requires='>=3.6',
      packages=find_packages('src', exclude=('tests', )),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      url='https://github.com/pgp/mega.py',
      description='Python lib for the Mega.nz API',
      long_description=readme + '\n\n' + history,
      long_description_content_type='text/markdown',
      license='Creative Commons Attribution-Noncommercial-Share Alike license',
      install_requires=install_requires,
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Internet :: WWW/HTTP',
      ],
      entry_points={
          'console_scripts': [
              'meganz=mega.maincli:maincli'
          ]
      },
      )
