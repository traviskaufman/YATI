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

Copyright (C) 2012 Travis Kaufman
----------------------------------
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses.
"""
__author__ = "Travis Kaufman"
__version__ = "2.0.0-dev"

import tweepy
import time
import os
import sys

USERDIR = os.getenv("HOME")
DEBUG = 0

class Yati:
    def __init__(self):
        self.config = {
            'CONSUMER_KEY':'3PqhYFkJohEruGu1Oxh85g',
            'CONSUMER_SECRET':'TNmjRcWKMMecAbTJm7WuB8H63xp5GJjvS9y1dWhC0',
            'AT_KEY':'',
            'AT_SEC':'',
            'timeZone':'America/New_York'
        }

        #set the current locale
        os.environ['TZ'] = self.config['timeZone']
        time.tzset()
        


        #authorize the user
        auth = tweepy.OAuthHandler(self.config['CONSUMER_KEY'], self.config['CONSUMER_SECRET']) 
        try:
            authfile = open(USERDIR + '/.yti', 'r')
            authkeys = authfile.readlines();
            self.config['AT_KEY'] = authkeys[0][:-1]
            if DEBUG:
                print 'AT_KEY: ' + self.config['AT_KEY'] + '\n'
            self.config['AT_SEC'] = authkeys[1][:-1]
            if DEBUG:
                print 'AT_SEC: ' + self.config['AT_SEC'] + '\n'
        except IOError:
            sys.stderr.write("NOTICE: Authorization required. Please copy and paste the following URL into your web browser, follow instructions, and then enter the PIN number you receive: " + auth.get_authorization_url() + '\n')
            verifier = raw_input('PIN: ').strip()
            auth.get_access_token(verifier)
            self.config['AT_KEY'] = auth.access_token.key
            self.config['AT_SEC'] = auth.access_token.secret
            authkeys = [self.config['AT_KEY'] + '\n', self.config['AT_SEC'] + '\n', 'end']
            try:
                authfile = open(USERDIR + '/.yti', 'w')
                authfile.writelines(authkeys)
                authfile.close()
            except IOError:
                sys.stderr.write("Error writing credentials to file. You may have to re-authorize when you use this app. To prevent this from happening, check disk space and/or file permissions and try again.")
        auth.set_access_token(self.config['AT_KEY'], self.config['AT_SEC'])

        self.tw = tweepy.API(auth);
    
    # get a certain number of tweets from the home timeline            
    def getTweets(self, max=10):
        return self.tw.home_timeline(count=max)

    # print the tweets
    def printTweets(self, tweets):
        title = "************* RECENT TWEETS ***************"
        print title.encode('utf8')
        print 'Last updated: ' + time.strftime('%I:%M%p')
        print ""
        for tweet in tweets:
            print tweet.user.screen_name + ' (' + tweet.user.name + '):'
            print tweet.text.encode('utf8')
            print '----------------------------'

def printUsage():
    print 'Usage: python yati.py [numberOfTweets]'

def main():
    numTweets = 10
    if len(sys.argv) > 1:
        try :
            numTweets = int(sys.argv[1])
        except ValueError:
            print 'Error: bad argument ' + sys.argv[1]
            printUsage()
            sys.exit()
    yati = Yati()
    tweets = yati.getTweets(numTweets)
    yati.printTweets(tweets)

if __name__ == "__main__":
    main()     