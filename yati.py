#!/usr/bin/python
"""
YATI (Yet Another Twitter Interface) - A TWITTER CLI FOR GEEKS
****************************

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

import tweepy
import time
import os
import sys
import pickle
import HTMLParser
import argparse


class Yati:
    """Wrapper for the Twitter Command Line Interface"""

    def __init__(self):
        self._config = {
            'CONSUMER_KEY': '3PqhYFkJohEruGu1Oxh85g',
            'CONSUMER_SECRET': 'TNmjRcWKMMecAbTJm7WuB8H63xp5GJjvS9y1dWhC0',
            'AT_KEY': '',
            'AT_SEC': '',
            'USERDIR': os.getenv("HOME")
        }
        self._tweepy = None
        self._should_flush_prev_tweets = True
        self._got_tweets_before = False
        self._tweet_table = {}
        self._tweet_table_length = 0
        self._can_retweet = True

        #authorize the user
        auth = tweepy.OAuthHandler(self._config['CONSUMER_KEY'],
                                   self._config['CONSUMER_SECRET'])
        try:
            authfile = open(self._config['USERDIR'] + '/.yti', 'r')
            authkeys = authfile.readlines()
            self._config['AT_KEY'] = authkeys[0][:-1]
            self._config['AT_SEC'] = authkeys[1][:-1]
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
            self._config['AT_KEY'] = auth.access_token.key
            self._config['AT_SEC'] = auth.access_token.secret
            authkeys = ["%s\n" % self._config['AT_KEY'],
                        "%s\n" % self._config['AT_SEC'],
                        'end']
            try:
                authfile = open(self._config['USERDIR'] + '/.yti', 'w')
                authfile.writelines(authkeys)
                authfile.close()
                sys.stderr.write("Successfully authorized!\n")
            except IOError:
                sys.stderr.write("Error writing credentials to file. "\
                    "You may have to re-authorize when you use this app. "\
                    "To prevent this from happening, check disk space and/or "\
                    "file permissions and try again.")
        auth.set_access_token(self._config['AT_KEY'], self._config['AT_SEC'])

        # get the Tweepy API
        self._tweepy = tweepy.API(auth)
        try:
            self._tweet_table = pickle.load(open(
                            '%s/.__yt__tweets' % self._config['USERDIR'],
                            'r'))
            if not self._tweet_table:
                self._can_retweet = False
            else:
                self._tweet_table_length = len(self._tweet_table)
        except IOError:
            self._can_retweet = False

    def get_tweets(self, max_tweets=10):
        """Retrieve tweets from the authorized user's home timeline, starting
        with the newest and going in descending order.

        max: (optional) The maximum amount of tweets you'd like to retrieve.
        Defaults to 10

        returns: A list of tweepy status objects containing information about
        each tweet
        """
        the_tweets = self._tweepy.home_timeline(count=max_tweets)
        self.store_tweets(the_tweets)
        self._got_tweets_before = True
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
        self._should_flush_prev_tweets = False
        max_chars = 140
        if len(new_status) > max_chars:
            sys.stderr.write(
                    "Error: tweets cannot be more than 140 characters")
            return False
        return self._tweepy.update_status(unicode(new_status))

    def store_tweets(self, tweets):
        """
        Stores a list of teepy status objects into a hash table so they can be
        accessed in the future
        ---------------------------------------------------
        tweets: The list of twitter status objects to store
        """
        if self._should_flush_prev_tweets and not self._got_tweets_before:
            self._tweet_table = {}
            self._tweet_table_length = 0
        for tweet in tweets:
            self.store_tweet(tweet)

    def store_tweet(self, tweet):
        """
        Stores an individual tweet. Helpler method for store_tweets()
        --------------------------------
        tweet: The tweet to store
        """
        self._tweet_table[self._tweet_table_length] = tweet
        self._tweet_table_length = self._tweet_table_length + 1

    def retweet(self, tweet_id):
        """
        Retweets a tweet based on its ID
        --------------------------------
        tweet_id: The tweetTable key that corresponds to the tweet
        you'd like to retweet. Users will be able to identify this
        by the "#X" before each tweet, where X is the int value that
        corresponds to the dictionary's key.

        Returns: a tweepy.status object on success
        """
        try:
            if not self._can_retweet:
                return None
            else:
                the_tweet = self._tweet_table[tweet_id - 1]
                self._tweepy.retweet(the_tweet.id)
                return the_tweet
        except KeyError:
            return -1

    # Serialize tweetTable and write it to file
    def __del__(self):
        if self._should_flush_prev_tweets:
            try:
                tweet_file = open(self._config['USERDIR'] + '/.__yt__tweets',
                                  'w')
                pickle.dump(self._tweet_table, tweet_file)
            except IOError:
                print 'File write failed'


def main():
    """Where the magic happens"""
    parser = argparse.ArgumentParser(
            description="A Python-based Twitter CLI")
    parser.add_argument("-g", "--get_tweets",
                        dest="num_tweets_to_get",
                        type=int,
                        const=10,
                        nargs='?',
                        help="Retrieve a certain number of tweets from your" \
                        " home timeline (defaults to 10)")
    parser.add_argument("-u", "--update",
                        type=str,
                        dest='status_update',
                        help="Update your status")
    parser.add_argument("-r", "--retweet",
                        type=int,
                        dest='rt_tweet_id',
                        help="Retweet a status with ID #N, where N is the" \
                        " number that prefixes the status you'd like to" \
                        " retweet")
    args = parser.parse_args()

    yati = Yati()

    # Print usage if no args. Eventually, no args will kick the program into a
    # REPL
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit()

    if args.status_update:
        status = yati.update_status(args.status_update)
        if status:
            print 'Status update successful'
        else:
            print 'Could not update your status at this time'

    if args.rt_tweet_id:
        try:
            result = yati.retweet(args.rt_tweet_id)
        except tweepy.error.TweepError as tw_err:
            print tw_err
            sys.exit()
        if type(result) is int and result is 0:
            print 'Error: unknown failure. Check internet connection possibly'
            parser.print_usage()
            sys.exit()
        elif type(result) is int and result is -1:
            print '%s is not a valid key. Please enter a valid key and '\
                    'try again' % str(args.rt_tweet_id)
            parser.print_usage()
            sys.exit()
        elif not result:
            print 'Retweet failed. Perhaps you have not stored any tweets? '\
                'Try running just yati.py or yati.py [numTweets] and try again'
            sys.exit()
        else:  # was successful
            print 'Retweet of tweet #%s (%s...) by @%s successful!' % \
                  (str(args.rt_tweet_id),
                   result.text[:50].encode('utf8'),
                   result.user.screen_name)

    if args.num_tweets_to_get:
        tweets = yati.get_tweets(max_tweets=args.num_tweets_to_get)
        Yati.print_tweets(tweets)

if __name__ == "__main__":
    main()
