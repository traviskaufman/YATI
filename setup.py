#!/usr/bin/env python

from distutils.core import setup

setup(name='yati',
      version='0.8.0',
      description='Yet Another Twitter Interface: A Twitter CLI',
      author='Travis Kaufman',
      author_email='travis.kaufman@gmail.com',
      url='https://github.com/traviskaufman/YATI',
      download_url='https://github.com/traviskaufman/YATI/zipball/master',
      license='GPL',
      py_modules=['yati'],
      scripts=['bin/yati']
)
