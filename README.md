YATI (Yet Another Twitter Interface) - A Twitter CLI
=====================================================
Starting as a bored-one-night hack home feed scraper, YATI is now (turning into?) a full-blown twitter CLI, with the ability to retrieve any number of tweets from your home timeline, post status updates, and retweet statuses.
More features, such as being able to retrieve tweets from specific friends, get mentions, etc. will be added in the future!


This program is made possible by the awesome [Tweepy library](https://github.com/tweepy/tweepy) which, if you need to interface with Twitter via Python, I HIGHLY recommend you make use of.

Installation:
-------------
*NOTE: you will soon be able to install this with easy_install*

1. If you don't have it already, install tweepy:

        $ [sudo] easy_install tweepy


2. Clone the repo    

        $ git clone https://github.com/traviskaufman/YATI.git


3. Run the setup script

        $ cd path/to/yati/
        $ python setup.py install
        
   Alternatively, if you like ruby and have rake installed (which if you're not, get on it):
   
        $ rake build          # Build, but don't install, the application
        $ rake buildinstall   # Build and install the application
        $ rake lint           # Lint the code (requires pyLint) 

How To Use:
------------
#### To get the 10 newest tweets on your home timeline: 
    $ yati [-g, --get-tweets]
#### To get the X newest tweets on your home timeline:
    $ yati [-g, --get-tweets X]
#### To update your status: 
    $ yati [-u, --update your_status_update]
#### To retweet a status: 
    $ yati [-r, --retweet tweet_id]
  *Note: The tweet_id will appear as the #N right before the tweet when you make a call to Yati. 
  e.g. $ yati.py # #1, #2, etc.. && yati.py --rt 2*
#### TL;DR:
    $ usage: yati [-h] [-g, --get-tweets [NUM_TWEETS_TO_GET]]
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
