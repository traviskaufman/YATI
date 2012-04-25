#!/usr/bin/python
"""
TODO:
---------------------------------
1) Erase the current tweetable every time new tweets are written
2) Update This Description and README
"""
"""
YATI (Yet Another Twitter Interface) - A TWITTER CLI FOR GEEKS
****************************
Starting as a bored-one-night hack, this gem scrapes your twitter feed for the 10 most recent posts, and displays them for you at the command line. More features to be added in the future. 

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
__version__ = "2.1.x-dev"

import tweepy
import time
import os
import sys
import pickle

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
            aURL = auth.get_authorization_url()
            sys.stderr.write("***NOTICE: Authorization required.***\nA URL will soon open that will guide you through app authorization. Once you have authorized the app, enter the PIN you receive below.\nIf it doesn't open, please paste the following into your web browser: " + aURL + '\n')
            time.sleep(3)
            os.system('open ' + aURL)
            verifier = raw_input('PIN: ').strip()
            auth.get_access_token(verifier)
            self.config['AT_KEY'] = auth.access_token.key
            self.config['AT_SEC'] = auth.access_token.secret
            authkeys = [self.config['AT_KEY'] + '\n', self.config['AT_SEC'] + '\n', 'end']
            try:
                authfile = open(USERDIR + '/.yti', 'w')
                authfile.writelines(authkeys)
                authfile.close()
                sys.stderr.write("Successfully authorized!\n")
            except IOError:
                sys.stderr.write("Error writing credentials to file. You may have to re-authorize when you use this app. To prevent this from happening, check disk space and/or file permissions and try again.")
        auth.set_access_token(self.config['AT_KEY'], self.config['AT_SEC'])
        
        # get the Tweepy API
        self.tw = tweepy.API(auth);
        # Dictionary to hold the latest gotten tweets, in order to retweet
        # them, work with them, etc.
        self.tweetTable = {}; 
        # TODO: Refactor file paths into global variables
        # Load the latest tweets gotten by the program into tweetTable
        self.canReTweet = True
        try:
            self.tweetTable = pickle.load(open(USERDIR + '/.__yt__tweets', 'r'))
            if not self.tweetTable:
              print 'No stored tweets; cannot retweet. Try running "python yati.py" and try again' 
              self.canReTweet = False
        except IOError:
            print 'Failed to retrieve stored tweets. Make sure you have tweets stored and/or you have file permissions set correctly.'
            self.canReTweet = False;

    # get a certain number of tweets from the home timeline            
    def getTweets(self, max=10):
        theTweets = self.tw.home_timeline(count=max)
        self.storeTweets(theTweets)
        return theTweets

    # print the tweets
    def printTweets(self, tweets):
        i = 0
        title = "************* RECENT TWEETS ***************"
        print title.encode('utf8')
        print 'Last updated: ' + time.strftime('%I:%M%p')
        print ""
        for tweet in tweets:
            i += 1
            print "#" + str(i) + ": " + tweet.user.screen_name + ' (' + tweet.user.name + '):'
            print tweet.text.encode('utf8')
            print '----------------------------'

    """
    Updates your Twitter Status from the command line
    ---------------------------------------
    @param status 
        Your status that you want to post. Supports all UTF-8 characters
    @return boolean
        True if status update successful, false if not
    """
    def updateStatus(self, newStatus):
        maxChars = 140
        if len(newStatus) > maxChars:
            sys.stderr.write("Error: tweets cannot be more than 140 characters")
            return False
        status = self.tw.update_status(unicode(newStatus))
        if status:
            print status
            return True
        else:
            return False
    
    """
    Stores a list of teepy status objects into a hash table so they can be used
    in the future
    ---------------------------------------------------
    @param *tweets
        The list of twitter status objects to store
    """
    def storeTweets(self, *tweets):
        [self.storeTweet(tw) for tw in tweets] 

    """
    Stores an individual tweet. Helpler method for storeTweets()
    --------------------------------
    @param tweet
        The tweet to store
    """
    def storeTweet(self, tweet):
        self.tweetTable[len(self.tweetTable)] = tweet
    
    """
    Retweets a tweet based on its ID
    --------------------------------
    @param tweetID
        The tweetTable key that corresponds to the tweet you'd like to retweet.
        Users will be able to identify this by the "#X" before each tweet,
        where X is the integer value that corresponds to the dictionaries key.
        I know what you may be thinking, why don't I just use an array? The
        answer is because: 1) Since dictionaries are essentially ordered maps
        the functionality is more extendable 2) The overhead cost compared to
        arrays are very minimal 3) Pickle loads up its stored objects into a
        dictionary, so I'll stick with the way Pickle does it

    @return tweepy.status object | integer
        If sucessful, this will return the status object that was retweeted. If
        unsuccessful, it will return some sort of error code that will give an
        indication as to why the retweet failed. Error codes thus far are:
        0: The tweepy call failed
        -1: User input an integer key that did not exist
    """
    def retweet(self, tweetID):
        try:
            if not self.canReTweet:
                return None
            else:
                theTweet = self.tweetTable[tweetID]
                self.tw.retweet(theTweet.id)
                return theTweet
        except KeyError:
            return -1

    # Serialize tweetTable and write it to file
    def __del__(self):
        try:
          tweetFile = open(USERDIR + '/.__yt__tweets', 'w')
          pickle.dump(self.tweetTable, tweetFile)
        except IOError:
          print 'File write failed'

def printUsage():
    print 'Usage: python yati.py [numberOfTweets] [--update status]'

def main():
    numTweets = 10
    tweetID = None
    isStatusUpdate = False
    isRetweet = False
    if len(sys.argv) > 1:
        # check integrity of sys.argv[2]
        if sys.argv[1] == "--update" and sys.argv[2] != None:
            isStatusUpdate = True
        elif sys.argv[1] == "--rt" and sys.argv[2] != None:
            try:
                tweetID = int(sys.argv[2])
                isRetweet = True
            except ValueError:
                print 'Error: bad argument ' + sys.argv[1] + '. Retweet ID must be an integer'
                printUsage()
                sys.exit()
        else:
            try :
                numTweets = int(sys.argv[1])
            except ValueError:
                print 'Error: bad argument ' + sys.argv[1]
                printUsage()
                sys.exit()

    yati = Yati()
    if DEBUG:
        print yati.tweetTable
    if isStatusUpdate:
        yati.updateStatus(sys.argv[2])
    elif isRetweet:
          result = yati.retweet(tweetID)
          if result is 0:
              print 'Error: unknown failure. Check internet connection possibly'
              printUsage()
              sys.exit()
          elif result is -1:
              print str(tweetID) + ' is not a valid key. Please enter a valid key and try again'
              printUsage()
              sys.exit()
          elif not result:
              print 'Retweet failed'
          else: # was successful
              print 'Retweet of tweet #' + str(tweetID) + ' (' + result.text[:50].encode('utf8') + '...) by @' + result.user.screen_name + ' successful!'

    else:
        tweets = yati.getTweets(numTweets)
        yati.printTweets(tweets)
        yati.storeTweets(*tweets)

if __name__ == "__main__":
    main()     
