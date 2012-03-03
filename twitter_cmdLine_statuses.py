#!/usr/bin/python
import tweepy
import time
import os

CONSUMER_KEY='3PqhYFkJohEruGu1Oxh85g'
CONSUMER_SECRET='TNmjRcWKMMecAbTJm7WuB8H63xp5GJjvS9y1dWhC0'
AT_KEY = '44453270-cVLZXRsQRIlFsYREt2puHREHj2uJH6LsNVr7WUgh3'
AT_SEC = 'ZP4DdkC3jYmSsxOhproCNLY0ndIlA2f23C1iWeBbCro'

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
