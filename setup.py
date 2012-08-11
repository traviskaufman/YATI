#!/usr/bin/env python
from setuptools import setup, find_packages

long_desc = """
Starting as a bored-one-night hack home feed scraper, YATI is now (turning
into?) a full-blown twitter CLI, with the ability to retrieve any number of
tweets from your home timeline, post status updates, and retweet statuses. You
can do cool things with YATI, like hooking it up to a crontab and embedding a
subshell on your desktop to get the latest tweets right there, or integrate it
into your Jenkins servers for up-to-the-minute broadcasts on your build
statuses.

More features, such as being able to retrieve tweets from specific friends, get
mentions, etc. will be added in the future!
"""

setup(name='yati',
      version='1.0.0dev',
      description='Yet Another Twitter Interface: A Twitter CLI',
      author='Travis Kaufman',
      author_email='travis.kaufman@gmail.com',
      url='https://github.com/traviskaufman/YATI',
      download_url='http://pypi.python.org/packages/source/y/yati/yati-1.0.0dev.tar.gz',
      license='GPL',
      packages=find_packages(),
      install_requires=['tweepy==1.10'],
      entry_points={
          'console_scripts': [
              'yati = yati:main'
          ]
      },
      py_modules=['yati'],
      long_description=long_desc
)
