#!/usr/bin/python
"""
YATI (Yet Another Twitter Interface) - A TWITTER CLI FOR GEEKS
****************************

HOW TO USE:
---------------------------------
* To get the 10 newest tweets on your home timeline: $ python yati.py
* To get the X newest tweets on your home timeline: $ python yati.py X
* To update your status: $ python yati.py --update [your_status_update]
* To retweet a status (NEW!!): $ python yati.py --rt [tweet_#]
        **Note: The tweet # will appear as the #N right before the tweet when
        you make a call to Yati.
        e.g. $ yati.py # #1, #2, etc.. && yati.py --rt 2

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
import HTMLParser

USERDIR = os.getenv("HOME")
DEBUG = 0


class Yati:
    """Wrapper for the Twitter Command Line Interface"""

    def __init__(self):
        self.config = {
            'CONSUMER_KEY': '3PqhYFkJohEruGu1Oxh85g',
            'CONSUMER_SECRET': 'TNmjRcWKMMecAbTJm7WuB8H63xp5GJjvS9y1dWhC0',
            'AT_KEY': '',
            'AT_SEC': '',
            'timeZone': 'America/New_York'
        }

        self.should_flush_prev_tweets = True
        # set true on first call to get_tweets()
        self.got_tweets_before = False
        #set the current locale
        os.environ['TZ'] = self.config['timeZone']
        time.tzset()

        #authorize the user
        auth = tweepy.OAuthHandler(self.config['CONSUMER_KEY'],
                                   self.config['CONSUMER_SECRET'])
        try:
            authfile = open(USERDIR + '/.yti', 'r')
            authkeys = authfile.readlines()
            self.config['AT_KEY'] = authkeys[0][:-1]
            if DEBUG:
                print 'AT_KEY: ' + self.config['AT_KEY'] + '\n'
            self.config['AT_SEC'] = authkeys[1][:-1]
            if DEBUG:
                print 'AT_SEC: ' + self.config['AT_SEC'] + '\n'
        except IOError:
            auth_url = auth.get_authorization_url()
            sys.stderr.write(
                "***NOTICE: Authorization required.***\nA URL will soon open "\
                "that will guide you through app authorization. Once you have"\
                " authorized the app, enter the PIN you receive below.\nIf it"\
                " doesn't open, please paste the following into your web "\
                " browser: %s\n" % auth_url)
            time.sleep(3)
            os.system('open ' + auth_url)
            verifier = raw_input('PIN: ').strip()
            auth.get_access_token(verifier)
            self.config['AT_KEY'] = auth.access_token.key
            self.config['AT_SEC'] = auth.access_token.secret
            authkeys = ["%s\n" % self.config['AT_KEY'],
                        "%s\n" % self.config['AT_SEC'],
                        'end']
            try:
                authfile = open(USERDIR + '/.yti', 'w')
                authfile.writelines(authkeys)
                authfile.close()
                sys.stderr.write("Successfully authorized!\n")
            except IOError:
                sys.stderr.write("Error writing credentials to file. "\
                    "You may have to re-authorize when you use this app. "\
                    "To prevent this from happening, check disk space and/or "\
                    "file permissions and try again.")
        auth.set_access_token(self.config['AT_KEY'], self.config['AT_SEC'])

        # get the Tweepy API
        self.tweepy = tweepy.API(auth)
        # them, work with them, etc.
        self.tweet_table = {}
        self.tweet_table_length = 0
        # Load the latest tweets gotten by the program into tweetTable
        self.can_retweet = True
        try:
            self.tweet_table = pickle.load(open('%s/.__yt__tweets' % USERDIR,
                                          'r'))
            if not self.tweet_table:
                self.can_retweet = False
            else:
                self.tweet_table_length = len(self.tweet_table)
        except IOError:
            print 'Failed to retrieve stored tweets. Make sure you have '\
                  'tweets stored and/or you have file permissions set '\
                  'correctly.'
            self.can_retweet = False

    def get_tweets(self, max_tweets=10):
        """Retrieve tweets from the authorized user's home timeline, starting
        with the newest and going in descending order.

        max: (optional) The maximum amount of tweets you'd like to retrieve.
        Defaults to 10

        returns: A list of tweepy status objects containing information about
        each tweet
        """
        the_tweets = self.tweepy.home_timeline(count=max_tweets)
        self.store_tweets(the_tweets)
        self.got_tweets_before = True
        return the_tweets

    @classmethod
    def print_tweets(cls, tweets):
        """Print a list of tweets

        tweets: A list of tweepy status objects
        """
        html_parser = HTMLParser.HTMLParser()
        i = 0
        title = "************* RECENT TWEETS ***************"
        print title.encode('utf8')
        print 'Last updated: ' + time.strftime('%I:%M%p')
        print ""
        for tweet in tweets:
            i += 1
            print "#%s: %s (%s)" % (str(i),
                                    tweet.user.screen_name,
                                    tweet.user.name)
            print html_parser.unescape(tweet.text.encode('utf8'))
            print '----------------------------'

    def update_status(self, new_status):
        """
        Updates your Twitter Status from the command line
        ---------------------------------------
        new_status: Your status that you want to post.

        Returns: True if status update successful, False if not
        """
        # We aren't getting any new tweets so no reason to flush the tweetTable
        self.should_flush_prev_tweets = False
        max_chars = 140
        if len(new_status) > max_chars:
            sys.stderr.write(
                    "Error: tweets cannot be more than 140 characters")
            return False
        status = self.tweepy.update_status(unicode(new_status))
        if status:
            print status
            return True
        else:
            return False

    def store_tweets(self, tweets):
        """
        Stores a list of teepy status objects into a hash table so they can be
        accessed in the future
        ---------------------------------------------------
        tweets: The list of twitter status objects to store
        """
        if (DEBUG):
            print 'Tweets '
            print tweets
        if self.should_flush_prev_tweets and not self.got_tweets_before:
            self.tweet_table = {}
            self.tweet_table_length = 0
        for tweet in tweets[0]:
            self.store_tweet(tweet)

    def store_tweet(self, tweet):
        """
        Stores an individual tweet. Helpler method for store_tweets()
        --------------------------------
        tweet: The tweet to store
        """
        self.tweet_table[self.tweet_table_length] = tweet
        self.tweet_table_length = self.tweet_table_length + 1

    def retweet(self, tweet_id):
        """
        Retweets a tweet based on its ID
        --------------------------------
        @param tweet_id
            The tweetTable key that corresponds to the tweet
            you'd like to retweet.
            Users will be able to identify this by the "#X" before each tweet,
            where X is the int value that corresponds to the dictionary's key.

        Returns: a tweepy.status object on success
        """
        try:
            if not self.can_retweet:
                return None
            else:
                the_tweet = self.tweet_table[tweet_id - 1]
                self.tweepy.retweet(the_tweet.id)
                return the_tweet
        except KeyError:
            return -1

    # Serialize tweetTable and write it to file
    def __del__(self):
        if self.should_flush_prev_tweets:
            try:
                tweet_file = open(USERDIR + '/.__yt__tweets', 'w')
                pickle.dump(self.tweet_table, tweet_file)
            except IOError:
                print 'File write failed'


def print_usage():
    """Print program usage."""
    print 'Usage: '\
          ' python yati.py [numberOfTweets] [--update status] [--rt tweet_#]'


def main():
    """Where the magic happens"""
    num_tweets = 10
    tweet_id = None
    is_status_update = False
    is_retweet = False
    if len(sys.argv) > 1:
        # check integrity of sys.argv[2]
        if sys.argv[1] == "--update" and sys.argv[2] != None:
            is_status_update = True
        elif sys.argv[1] == "--rt" and sys.argv[2] != None:
            try:
                tweet_id = int(sys.argv[2])
                is_retweet = True
            except ValueError:
                print 'Error: bad argument %s. Retweet ID must be an integer' \
                        % sys.argv[1]
                print_usage()
                sys.exit()
        else:
            try:
                num_tweets = int(sys.argv[1])
            except ValueError:
                print 'Error: bad argument ' + sys.argv[1]
                print_usage()
                sys.exit()

    yati = Yati()
    if DEBUG:
        print yati.tweet_table
    if is_status_update:
        yati.update_status(sys.argv[2])
    elif is_retweet:
        result = yati.retweet(tweet_id)
        if type(result) is int and result is 0:
            print 'Error: unknown failure. Check internet connection possibly'
            print_usage()
            sys.exit()
        elif type(result) is int and result is -1:
            print '%s is not a valid key. Please enter a valid key and '\
                    'try again' % str(tweet_id)
            print_usage()
            sys.exit()
        elif not result:
            print 'Retweet failed. Perhaps you have not stored any tweets? '\
                'Try running just yati.py or yati.py [numTweets] and try again'
        else:  # was successful
            print 'Retweet of tweet #%s (%s...) by @%s successful!' % \
                  (str(tweet_id),
                   result.text[:50].encode('utf8'),
                   result.user.screen_name)

    else:
        tweets = yati.get_tweets(max_tweets=num_tweets)
        Yati.print_tweets(tweets)


if __name__ == "__main__":
    main()
