YATI (Yet Another Twitter Interface) - A Twitter CLI
=====================================================
Starting as a bored-one-night hack home feed scraper, YATI is now (turning into?) a full-blown twitter CLI, with the ability to retrieve any number of tweets from your home timeline, post status updates, and retweet statuses. You can do cool things with YATI, like hooking it up to a crontab and embedding a subshell on your desktop to get the latest tweets right there, or integrate it into your Jenkins servers for up-to-the-minute broadcasts on your build statuses.

More features, such as being able to retrieve tweets from specific friends, get mentions, etc. will be added in the future!


This program is made possible by the awesome [Tweepy library](https://github.com/tweepy/tweepy) which, if you need to interface with Twitter via Python, I HIGHLY recommend you make use of.

Installation:
-------------
1. If you don't have it already, [Install Setuptools](http://pypi.python.org/pypi/setuptools/#installation-instructions)

2. Run the following command:
    $ [sudo] easy_install yati

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
  *Note: The tweet_id will appear as the #N right before the tweet when you make a call to Yati. 
  e.g. $ yati.py # #1, #2, etc.. && yati.py --rt 2*
#### TL;DR:
    $ usage: yati [-h] [-g, --get_tweets [NUM_TWEETS_TO_GET]]
                [-u, --update STATUS_UPDATE] [-r, --retweet RT_TWEET_ID] 

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
