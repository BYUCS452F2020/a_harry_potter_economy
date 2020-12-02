import praw
import os
import sys
from database.firestore_db import FirestoreDatabase


def getGuideLinkText():
    return "\n\n____________\n\n" + "I am a bot. [Click here](https://www.reddit.com/user/ww-test-bot/comments/jjzc9n/a_guide_to_using_the_wizarding_world_currency_bot/) to learn how to use me."

def search(reddit, db, posts_replied_to):
    for results in reddit.subreddit('thetestingzone').comments():
        if results.id not in posts_replied_to:
            body = results.body  # Grab the Comment
            body = body.lower()	
            found = body.find('!redditgalleon')

def main():
    assert os.environ['HP_FIREBASE_CREDS']
    db = FirestoreDatabase(os.environ['HP_FIREBASE_CREDS'])
    reddit = praw.Reddit('ww-test-bot')
    
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")

    # search(reddit, db, posts_replied_to)
    
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")

main()