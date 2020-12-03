#!/tmp/reddit_bot_app/lib/python3.7/site-packages/
# coding: utf-8
#from /tmp/dumbledore-reddit-app/lib/python3.7/site-packages/praw import praw
import praw
#praw.path.insert(0, 'tmp/dumbledore-reddit-app/lib/python3.7/site-packages/')
import pdb
import re
import os
import sys
import time
import random
import sqlite3
from sqlite3 import Error
from database.firestore_db import FirestoreDatabase


def getGuideLinkText():
    return "\n\n____________\n\n" + "I am a bot. [Click here](https://www.reddit.com/user/ww-test-bot/comments/jjzc9n/a_guide_to_using_the_wizarding_world_currency_bot/) to learn how to use me."

def search(reddit, db, posts_replied_to):
    for results in reddit.subreddit('thetestingzone').comments():
        #if results.id not in posts_replied_to:
        if not results.saved:
            results.save()
            body = results.body  # Grab the Comment
            body = body.lower()	
            found = body.find('!redditgalleon')
            if found != -1:
                try:
                    results.reply("bot is running")
                except:
                    break

def main():
    assert os.environ['HP_FIREBASE_CREDS']
    db = FirestoreDatabase(os.environ['HP_FIREBASE_CREDS'])
    reddit = praw.Reddit(client_id="-4ByKCJuYOID4A", client_secret="we-8e_TZOCFsHmhmF8rZEPJTWLI", password="&2@X3G5BX6*v5K%a", username="ww-test-bot", user_agent="ww-test 1.0")
    
    # if not os.path.isfile("posts_replied_to.txt"):
    #     posts_replied_to = []
    # else:
    #     with open("posts_replied_to.txt", "r") as f:
    #         posts_replied_to = f.read()
    #         posts_replied_to = posts_replied_to.split("\n")

    posts_replied_to = 2
    search(reddit, db, posts_replied_to)
    
    # with open("posts_replied_to.txt", "w") as f:
    #     for post_id in posts_replied_to:
    #         f.write(post_id + "\n")

main()