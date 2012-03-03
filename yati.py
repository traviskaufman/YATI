#!/usr/bin/python
"""
YATI (Yet Another Twitter Interface) - A TWITTER CLI FOR GEEKS
****************************
A bored-one-night hack, this gem scrapes your twitter feed for the 10 most recent posts, and displays them for you at the command line. More features to be added in the future. 

Fun things you can do with YATI:
---------------------------------
* Read your recent twitter feed without ever leaving the comfort of the command line. 
* Use it in a system call to leverage the data in a program in some way
* Write your tweets to a file for a nice twitter log (e.g. yati > ~/.tweets)
* Configure a crontab to write your tweets to a certain file, then use a program like Geek Tool (OS X) to cat the file and display it on your desktop (not that I do this or anything...)
"""
__author__ = "Travis Kaufman"
__version__ = "1.0.0"

import tweepy
import time
import os
import sys

CONSUMER_KEY='3PqhYFkJohEruGu1Oxh85g'
CONSUMER_SECRET='TNmjRcWKMMecAbTJm7WuB8H63xp5GJjvS9y1dWhC0'
AT_KEY = ''
AT_SEC = ''

def main():
    os.environ['TZ'] = 'America/New_York'
    time.tzset()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(AT_KEY, AT_SEC)
    tw = tweepy.API(auth)
    timeline = tw.home_timeline(count=10)
    title = "************* RECENT TWEETS ***************"
    print title.encode('utf8')
    print 'Last updated: ' + time.strftime('%I:%M%p')
    print ""
    for tl in timeline:
        print tl.user.screen_name + ' (' + tl.user.name + '):'
        print tl.text.encode('utf8')
        print '----------------------------'

if __name__ == "__main__":
    main()     
