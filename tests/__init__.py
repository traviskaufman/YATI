"""These are where all the automated tests for Yati will be stored"""
import os
import unittest
from yati import Yati
from mockito import *


class YatiTestBase(unittest.TestCase):
    """The base class for all Yati tests"""

    def setUp(self):
        cwd = os.getcwd()
        self.yati = Yati()
        self.yati._config['TWEET_CACHE'] = "%s/mock/tweetcache" % cwd
