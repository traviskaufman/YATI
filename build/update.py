"""
YATI Update Script
==================
Upgrades v1.0.0 to v1.0.1

author: Travis Kaufman
version: 1.0.1dev
"""
import os
import shutil
import sys


def _move(source, target):
    if not os.path.exists(target) and \
           os.path.exists(source):
        shutil.move(source, target)


def main():
    sys.stdout.write("Running config update script...")
    sys.stdout.flush()

    home = os.getenv("HOME")
    old_auth_file = home + "/.yti"
    old_tweets_file = home + "/.__yt__tweets"
    new_directory = home + "/.yati"
    new_auth_file = new_directory + "/auth"
    new_tweets_file = new_directory + "/tweetcache"

    if not os.path.exists(new_directory):
        os.mkdir(new_directory)

    _move(old_auth_file, new_auth_file)
    _move(old_tweets_file, new_tweets_file)

    print "Done"

if __name__ == "__main__":
    main()
