#!/usr/bin/env python
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from setuptools.command.install import install as _install
from sys import hexversion, exit, stderr
from yati import __version__ as VERSION
import build.update as update


if hexversion < 0x02070000:
    stderr.write("Error: yati is only compatible with Python2.7+")
    exit(1)

long_desc = """
Starting as a bored-one-night hack home feed scraper, YATI is now (turning
into?) a full-blown twitter CLI, with the ability to retrieve any number of
tweets from your home timeline, post status updates, and retweet statuses. You
can do cool things with YATI, like hooking it up to a crontab and embedding a
subshell on your desktop to get the latest tweets right there, or integrate it
into your Jenkins servers for up-to-the-minute broadcasts on your build
statuses.

Currently, you can:
    * Get statuses from your home timeline
    * Update your status
    * Reply to tweets
    * Retweet tweets

In the future, you will be able to:
    * Get mentions
    * Favorite tweets
    * Update your location
    * Use this as a REPL
    * Stream tweets
    * and more!
"""


class install(_install):
    def run(self):
        _install.run(self)
        update.main()


setup(name='yati',
      cmdclass={'install': install},
      version=VERSION,
      description='Yet Another Twitter Interface: A Twitter CLI',
      author='Travis Kaufman',
      author_email='travis.kaufman@gmail.com',
      url='https://github.com/traviskaufman/YATI',
      download_url='http://pypi.python.org/packages/source/y' +
                   '/yati/yati-1.0.1dev.tar.gz',
      license='GPL',
      packages=find_packages(),
      install_requires=['tweepy==1.10'],
      entry_points={
          'console_scripts': [
              'yati = yati:main'
          ]
      },
      py_modules=['yati'],
      long_description=long_desc,
      tests_require=['nose>=1.1', 'mockito>=0.5'],
      test_suite='nose.collector'
)
