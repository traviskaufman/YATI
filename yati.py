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

USERDIR = os.getenv("HOME")

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
            self.config['AT_KEY'] = authkeys[0][:-2]
            self.config['AT_SEC'] = authkeys[1][:-2]
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
        for tl in timeline:
            print tl.user.screen_name + ' (' + tl.user.name + '):'
            print tl.text.encode('utf8')
            print '----------------------------'

def main():
    yati = Yati()
    tweets = yati.getTweets()
    yati.printTweets(tweets)

if __name__ == "__main__":
    main()     
