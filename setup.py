#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='yati',
      version='1.0.0dev',
      description='Yet Another Twitter Interface: A Twitter CLI',
      author='Travis Kaufman',
      author_email='travis.kaufman@gmail.com',
      url='https://github.com/traviskaufman/YATI',
      download_url='https://github.com/traviskaufman/YATI/zipball/master',
      license='GPL',
      packages=find_packages(),
      install_requires=['tweepy==1.10'],
      entry_points={
          'console_scripts': [
              'yati = yati:main'
          ]
      },
      py_modules=['yati'],
      long_description=open('README.md').read()
)
