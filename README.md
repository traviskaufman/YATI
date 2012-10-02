YATI (Yet Another Twitter Interface) - A Twitter CLI
=====================================================
Starting as a bored-one-night hack home feed scraper, YATI is now (turning
into?) a full-blown twitter CLI, with the ability to retrieve any number of
tweets from your home timeline, post status updates, and retweet statuses. You
can do cool things with YATI, like hooking it up to a crontab and embedding a
subshell on your desktop to get the latest tweets right there, or integrate it
into your Jenkins servers for up-to-the-minute broadcasts on your build
statuses.

More features, such as being able to retrieve tweets from specific friends, get
mentions, etc. will be added in the future!


This program is made possible by the awesome [Tweepy library](https://github.com/tweepy/tweepy)
which, if you need to interface with
Twitter via Python, I HIGHLY recommend you make use of.

Installation:
-------------
1. If you don't have it already, [Install Setuptools](http://pypi.python.org/pypi/setuptools/#installation-instructions)
   

2. Run the following command: <code>$ [sudo] easy_install yati</code>

Get the Latest Development Version:
-----------------------------------
1. Checkout this repo

2. Run <code>$ python setup.py install</code>

How To Use:
------------
#### To get the 10 newest tweets on your home timeline: 
    $ yati [-g, --get_tweets]
#### To get the X newest tweets on your home timeline:
    $ yati [-g, --get_tweets X]
#### To update your status: 
    $ yati [-u, --update your_status_update]
#### To retweet a status: 
    $ yati [-r, --retweet tweet_id]
  *Note: The tweet_id will appear as the #N right before the tweet when you
  make a call to Yati. 
  e.g. $ yati -g #1, #2, etc.. && yati -r 2*
#### To reply to a tweet:
    $ yati [-i, --in-reply-to tweet_id] -u reply
Note that yati will automatically add in a reference to the user you are
replying to, so you don't have to worry about doing so. E.g. if you write

    $ yati -i 2 -u "I agree completely."

And the user who posted the tweet with id #2 has a screen name of awesomeguy32,
your tweet will show up on twitter as "@awesomeguy32 I agree completely."

If you supply an -i switch, the program will expect you to supply a -u switch
as well (after all, what good is a reply if you have nothing to reply with?).
If you don't supply a -u switch, the program will simply do nothing. The
`tweet_id` supplied is the same `tweet_id` used for retweeting.
#### TL;DR:
    $ usage: yati [-h] [-g, --get_tweets [NUM_TWEETS_TO_GET]]
                [-u, --update STATUS_UPDATE] [-r, --retweet RT_TWEET_ID] 
                [-i, --in-reply-to TWEET_ID]

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
