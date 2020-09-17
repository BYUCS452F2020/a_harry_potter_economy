#!/tmp/reddit_bot_app/lib/python3.7/site-packages/
# coding: utf-8
#from /tmp/dumbledore-reddit-app/lib/python3.7/site-packages/praw import praw
import praw
#praw.path.insert(0, 'tmp/dumbledore-reddit-app/lib/python3.7/site-packages/')
import pdb
import re
import os
import time
import random
import sqlite3
from sqlite3 import Error

class User:
  def __init__(self, username, galleons, sickles, knuts):
      self.username = username
      self.galleons = galleons
      self.sickles = sickles
      self.knuts = knuts

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn
    
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.close()
    except Error as e:
        print(e)

def insert_user(conn, user):
    sql = ''' INSERT INTO users(username,galleons,sickles,knuts)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (user.username, user.galleons, user.sickles, user.knuts,))
    conn.commit()
    cur.close()
    
def update_user(conn, user):
    sql = ''' UPDATE users
              SET galleons = ? ,
                  sickles = ? ,
                  knuts = ?
              WHERE username = ?'''
    cur = conn.cursor()
    cur.execute(sql, (user.galleons, user.sickles, user.knuts, user.username,))
    conn.commit()
    cur.close()

def get_user(conn, username):
    try:
        c = conn.cursor()
        sql_select_query = """select * from users where username = ?"""
        c.execute(sql_select_query, (username,))
        records = c.fetchone()
        if records is None:
            return 0
        user = User(records[0], records[1], records[2], records[3])
        c.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    return user
    
def get_total_awards(conn):
    try:
        c = conn.cursor()
        sql_select_query = """select sum(galleons+sickles+knuts) from users"""
        c.execute(sql_select_query)
        records = c.fetchone()
        if records is None:
            return 0
        total_awards = records[0]
        c.close()
    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    return total_awards
    
def get_total_users(conn):
    try:
        c = conn.cursor()
        sql_select_query = """select count(*) from users"""
        c.execute(sql_select_query)
        records = c.fetchone()
        if records is None:
            return 0
        total_users = records[0]
        c.close()
    except sqlite3.Error as error:
        print("Failed to read data from table", error)
    return total_users
    
def search():
    reddit = praw.Reddit('ww-test-bot')
    
    # Have we run this code before? If not, create an empty list
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    
    # If we have run the code before, load the list of posts we have replied to
    else:
        # Read the file into a list and remove any empty values
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))
            
    for results in reddit.subreddit('thetestingzone').comments():	#Grab all the Recent Comments. This will return 100 of the newest comments
        if results.id not in posts_replied_to:
            if not results.saved:
                body = results.body  #Grab the Comment
                body=body.lower()	
                found=body.find('!redditgalleon')
                if found != -1: 
                    try:
                        posts_replied_to.append(results.id)
                        results.save()
                        name = results.parent().author.name
                        if results.author.name != name:
                            conn = create_connection(r"currency_sqlite_test.db")
                            if conn is not None:
                                create_statement = """ CREATE TABLE IF NOT EXISTS users (
                                                                    username text PRIMARY KEY,
                                                                    galleons integer,
                                                                    sickles integer,
                                                                    knuts integer
                                                                ); """
                                create_table(conn, create_statement)
                            else:
                                print("Error! cannot create the database connection.")
                            with conn:
                                user = get_user(conn, name)
                                if user == 0:
                                    user = User(name, 0, 0, 0)
                                    insert_user(conn, user)
                                galleons = user.galleons + 1
                                user.galleons = galleons
                                update_user(conn, user)
                                galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                                sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                                knutString = " knut." if user.knuts == 1 else " knuts."
                                reply = "You have given u/" + name + " a Reddit Galleon.\n\nu/" + name + " has received a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                results.reply(reply)
                    except:
                        break
                else:
                    found=body.find('!redditsickle')
                    if found != -1: 		
                        try:
                            posts_replied_to.append(results.id)
                            results.save()
                            name = results.parent().author.name
                            if results.author.name != name:
                                conn = create_connection(r"currency_sqlite_test.db")
                                if conn is not None:
                                    create_statement = """ CREATE TABLE IF NOT EXISTS users (
                                                                        username text PRIMARY KEY,
                                                                        galleons integer,
                                                                        sickles integer,
                                                                        knuts integer
                                                                    ); """
                                    create_table(conn, create_statement)
                                else:
                                    print("Error! cannot create the database connection.")
                                with conn:
                                    user = get_user(conn, name)
                                    if user == 0:
                                        user = User(name, 0, 0, 0)
                                        insert_user(conn, user)
                                    sickles = user.sickles + 1
                                    if sickles == 17:
                                        galleons = user.galleons + 1
                                        user.galleons = galleons
                                        sickles = 0
                                    user.sickles = sickles
                                    update_user(conn, user)
                                    galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                                    sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                                    knutString = " knut." if user.knuts == 1 else " knuts."
                                    reply = "You have given u/" + name + " a Reddit Sickle.\n\nu/" + name + " has received a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                    results.reply(reply)
                        except:
                            break
                    else:
                        found=body.find('!redditknut')
                        if found != -1:
                            try:
                                posts_replied_to.append(results.id)
                                results.save()
                                name = results.parent().author.name
                                if results.author.name != name:
                                    conn = create_connection(r"currency_sqlite_test.db")
                                    if conn is not None:
                                        create_statement = """ CREATE TABLE IF NOT EXISTS users (
                                                                            username text PRIMARY KEY,
                                                                            galleons integer,
                                                                            sickles integer,
                                                                            knuts integer
                                                                        ); """
                                        create_table(conn, create_statement)
                                    else:
                                        print("Error! cannot create the database connection.")
                                    with conn:
                                        user = get_user(conn, name)
                                        if user == 0:
                                            user = User(name, 0, 0, 0)
                                            insert_user(conn, user)
                                        knuts = user.knuts + 1
                                        if knuts == 29:
                                            sickles = user.sickles + 1
                                            user.sickles = sickles
                                            knuts = 0
                                        user.knuts = knuts
                                        update_user(conn, user)
                                        galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                                        sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                                        knutString = " knut." if user.knuts == 1 else " knuts."
                                        reply = "You have given u/" + name + " a Reddit Knut.\n\nu/" + name + " has received a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                        results.reply(reply)
                            except:
                                break
                        else:
                            found=body.find("!gringotts")
                            if found != -1:
                                try:
                                    posts_replied_to.append(results.id)
                                    results.save()
                                    name = results.author.name
                                    conn = create_connection(r"currency_sqlite_test.db")
                                    if conn is not None:
                                        create_statement = """ CREATE TABLE IF NOT EXISTS users (
                                                                            username text PRIMARY KEY,
                                                                            galleons integer,
                                                                            sickles integer,
                                                                            knuts integer
                                                                        ); """
                                        create_table(conn, create_statement)
                                    else:
                                        print("Error! cannot create the database connection.")
                                    with conn:
                                        user = get_user(conn, name)
                                        if user == 0:
                                            user = User(name, 0, 0, 0)
                                            insert_user(conn, user)
                                        galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                                        sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                                        knutString = " knut." if user.knuts == 1 else " knuts."
                                        total_awards = 0
                                        total_users = 0
                                        total_awards = get_total_awards(conn)
                                        total_users = get_total_users(conn)
                                        if total_awards != 0 and total_users != 0:
                                            reply = "You have been given a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString + "\n\n____________\n\n" + "I have given " + str(total_users) + " users a total of " + str(total_awards) + " awards."
                                        else:
                                            reply = "You have been given a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                        results.reply(reply)
                                except:
                                    break
    # Write our updated list back to the file
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")

search()