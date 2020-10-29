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

def get_value_from_coins(galleons, sickles, knuts):
    return (galleons * 493) + (sickles * 29) + knuts

def get_coins_from_value(value):
    galleons = value // 493
    value = value % 493
    sickles = value // 29
    knuts = value % 29
    return [galleons, sickles, knuts]

class Card:
    def __init__(self, cardname, value):
        self.cardname = cardname
        self.value = value
        
common_cards = ["Albus Dumbledore", "Flavius Belby", "Uric the Oddball", "Adalbert Waffling", "Archibald Alderton", "Bowman Wright", "Burdock Muldoon", "Chauncey Oldridge", "Cassandra Vablatsky", "Godric Gryffindor", "Rowena Ravenclaw", "Helga Hufflepuff", "Salazar Slytherin"]
uncommon_cards = ["Gregory the Smarmy", "Gwenog Jones", "Herpo the Foul", "Mungo Bonham", "Bertie Bott", "Artemisia Lufkin", "Newt Scamander", "Elladora Ketteridge"]
rare_cards = ["Celestina Warbeck", "Circe", "Cornelius Agrippa", "Paracelsus", "Wendelin the Weird"]
epic_cards = ["Urg the Unclean", "Morgan le Fay", "Ptolemy"]
legendary_cards = ["Harry Potter", "Merlin"]

def get_random_card():
    rarity = random.randint(1, 100)
    if rarity < 43:
        name_index = random.randint(0, len(common_cards) - 1)
        return common_cards[name_index]
    elif rarity < 73:
        name_index = random.randint(0, len(uncommon_cards) - 1)
        return uncommon_cards[name_index]
    elif rarity < 93:
        name_index = random.randint(0, len(rare_cards) - 1)
        return rare_cards[name_index]
    elif rarity < 100:
        name_index = random.randint(0, len(epic_cards) - 1)
        return epic_cards[name_index]
    else:
        name_index = random.randint(0, len(legendary_cards) - 1)
        return legendary_cards[name_index]

class Item:
    def __init__(self, itemname, value):
        self.itemname = itemname
        self.value = value

def getGuideLinkText():
    return "\n\n____________\n\n" + "I am a bot. [Click here](https://www.reddit.com/user/ww-test-bot/comments/jjzc9n/a_guide_to_using_the_wizarding_world_currency_bot/) to learn how to use me."

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def insert_user(conn, user):
    sql = ''' INSERT INTO User(UserName,Galleons,Sickles,Knuts)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (user.username, user.galleons, user.sickles, user.knuts,))
    conn.commit()
    cur.close()
    
def update_user(conn, user):
    sql = ''' UPDATE User
              SET Galleons = ? ,
                  Sickles = ? ,
                  Knuts = ?
              WHERE UserName = ?'''
    cur = conn.cursor()
    cur.execute(sql, (user.galleons, user.sickles, user.knuts, user.username,))
    conn.commit()
    cur.close()

def get_user(conn, username):
    try:
        c = conn.cursor()
        sql_select_query = """select * from User where UserName = ?"""
        c.execute(sql_select_query, (username,))
        records = c.fetchone()
        if records is None:
            return 0
        user = User(records[0], records[1], records[2], records[3])
        c.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    return user
    
def insert_card(conn, cardname, username):
    sql = ''' INSERT INTO CardInventory(CardName, UserName)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (cardname, username,))
    conn.commit()
    cur.close()

def get_card(conn, cardname):
    try:
        c = conn.cursor()
        sql_select_query = """select * from Card where CardName = ?"""
        c.execute(sql_select_query, (cardname,))
        records = c.fetchone()
        if records is None:
            return 0
        card = Card(records[0], records[1])
        c.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    return card

def sell_card(conn, cardname, username):
    cur = conn.cursor()
    sql = ''' SELECT * FROM CardInventory
              WHERE CardName = ? AND UserName = ? '''
    cur.execute(sql, (cardname, username,))
    records = cur.fetchone()
    cur.close()
    if records is None:
        return "You do not own the " + cardname + " chocolate frog card." + getGuideLinkText()
    
    sql_delete = ''' DELETE FROM CardInventory
                     WHERE CardId = (SELECT MIN(CardId) FROM CardInventory WHERE CardName = ? AND UserName = ?) '''
    cur = conn.cursor()
    cur.execute(sql_delete, (cardname, username,))
    conn.commit()
    cur.close()
    
    user = get_user(conn, username)
    card = get_card(conn, cardname)
    new_value = get_value_from_coins(user.galleons, user.sickles, user.knuts) + card.value
    coins = get_coins_from_value(new_value)
    user.galleons = coins[0]
    user.sickles = coins[1]
    user.knuts = coins[2]
    update_user(conn, user)
    
    galleonString = " galleon, " if user.galleons == 1 else " galleons, "
    sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
    knutString = " knut." if user.knuts == 1 else " knuts."
    reply = "You sold your " + cardname + " chocolate frog card!\n\n" + "Your Gringotts vault now has a balance of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
    return reply + getGuideLinkText()
    
def insert_item(conn, itemname, username):
    sql = ''' INSERT INTO ItemInventory(ItemName, UserName)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (itemname, username,))
    conn.commit()
    cur.close()

def get_item(conn, itemname):
    try:
        c = conn.cursor()
        sql_select_query = """select * from Item where ItemName = ?"""
        c.execute(sql_select_query, (itemname,))
        records = c.fetchone()
        if records is None:
            return 0
        item = Item(records[0], records[1])
        c.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    return item

def buy_item(conn, itemname, username):
    item = get_item(conn, itemname)
    user = get_user(conn, username)
    if user == 0:
        user = User(name, 0, 0, 0)
        insert_user(conn, user)
    user_value = get_value_from_coins(user.galleons, user.sickles, user.knuts)
    if user_value < item.value:
        return "You do not have enough wizard gold to purchase this item." + getGuideLinkText()
    else:
        coins = get_coins_from_value(user_value - item.value)
        user.galleons = coins[0]
        user.sickles = coins[1]
        user.knuts = coins[2]
        update_user(conn, user)
        
        insert_item(conn, itemname, username)
        
        galleonString = " galleon, " if user.galleons == 1 else " galleons, "
        sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
        knutString = " knut." if user.knuts == 1 else " knuts."
        reply = "One " + itemname + " has been added to your Gringotts vault!\n\n" + "You now have a balance of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
        return reply + getGuideLinkText()

def give_item(conn, itemname, giver, receiver):
    cur = conn.cursor()
    sql = ''' SELECT * FROM ItemInventory
              WHERE ItemName = ? AND UserName = ? '''
    cur.execute(sql, (itemname, giver,))
    records = cur.fetchone()
    cur.close()
    if records is None:
        return "You do not own that item." + getGuideLinkText()
    
    user = get_user(conn, receiver)
    if user == 0:
        user = User(receiver, 0, 0, 0)
        insert_user(conn, user)
    
    sql_delete = ''' DELETE FROM ItemInventory
                     WHERE ItemId = (SELECT MIN(ItemId) FROM ItemInventory WHERE ItemName = ? AND UserName = ?) '''
    cur = conn.cursor()
    cur.execute(sql_delete, (itemname, giver,))
    conn.commit()
    cur.close()
    
    insert_item(conn, itemname, receiver)
    
    return "You have given u/" + receiver + " one " + itemname + "! It has been removed from your Gringotts vault and added to theirs." + getGuideLinkText()

def get_user_items_and_cards(conn, username, reply):
    sql_get_items = ''' SELECT ItemName FROM ItemInventory
                        WHERE UserName = ? '''
    cur = conn.cursor()
    cur.execute(sql_get_items, (username,))
    rows = cur.fetchall()
    if rows is not None:
        reply = reply + "\n\n" + "## You have the following items in your vault:\n"
        for row in rows:
            reply = reply + "\n- " + row[0]
    cur.close()
    
    sql_get_cards = ''' SELECT CardName FROM CardInventory
                        WHERE UserName = ? '''
    cur = conn.cursor()
    cur.execute(sql_get_cards, (username,))
    rows = cur.fetchall()
    if rows is not None:
        reply = reply + "\n\n" + "## You have the following chocolate frog cards in your vault:\n"
        for row in rows:
            reply = reply + "\n- " + row[0]
    cur.close()
    return reply

def get_total_awards(conn):
    try:
        c = conn.cursor()
        sql_select_query = """select sum(Galleons+Sickles+Knuts) from User"""
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
        sql_select_query = """select count(*) from User"""
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
    
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = list(filter(None, posts_replied_to))
            
    for results in reddit.subreddit('thetestingzone').comments():
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
                                reply = "You have given u/" + name + " a Reddit Galleon.\n\nu/" + name + " has a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                reply = reply + getGuideLinkText()
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
                                    reply = "You have given u/" + name + " a Reddit Sickle.\n\nu/" + name + " has a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                    reply = reply + getGuideLinkText()
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
                                        reply = "You have given u/" + name + " a Reddit Knut.\n\nu/" + name + " has a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                        reply = reply + getGuideLinkText()
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
                                    with conn:
                                        user = get_user(conn, name)
                                        if user == 0:
                                            user = User(name, 0, 0, 0)
                                            insert_user(conn, user)
                                        galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                                        sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                                        knutString = " knut." if user.knuts == 1 else " knuts."
                                        reply = "You have a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                        reply = get_user_items_and_cards(conn, user.username, reply)
                                        reply = reply + getGuideLinkText()
                                        results.reply(reply)
                                except:
                                    break
                            else:
                                found=body.find('!chocolatefrog')
                                if found != -1:
                                    try:
                                        posts_replied_to.append(results.id)
                                        results.save()
                                        name = results.author.name
                                        conn = create_connection(r"currency_sqlite_test.db")
                                        with conn:
                                            user = get_user(conn, name)
                                            if user == 0:
                                                user = User(name, 0, 0, 0)
                                                insert_user(conn, user)
                                            user_value = get_value_from_coins(user.galleons, user.sickles, user.knuts)
                                            if user_value < 377:
                                                results.reply("You do not have enough wizard gold to purchase a chocolate frog. You need 13 Sickles.")
                                            else:
                                                coins = get_coins_from_value(user_value - 377)
                                                user.galleons = coins[0]
                                                user.sickles = coins[1]
                                                user.knuts = coins[2]
                                                update_user(conn, user)
                                                
                                                cardname = get_random_card()
                                                insert_card(conn, cardname, user.username)
                                                
                                                galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                                                sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                                                knutString = " knut." if user.knuts == 1 else " knuts."
                                                reply = "You got the " + cardname + " chocolate frog card!\n\n" + "13 sickles have been removed from your Gringotts vault, and you now have a balance of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                                reply = reply + getGuideLinkText()
                                                results.reply(reply)
                                    except:
                                        break
                                else:
                                    found=body.find('!sellgwenog')
                                    if found != -1:
                                        try:
                                            posts_replied_to.append(results.id)
                                            results.save()
                                            conn = create_connection(r"currency_sqlite_test.db")
                                            with conn:
                                                reply = sell_card(conn, "Gwenog Jones", results.author.name)
                                                results.reply(reply)
                                        except:
                                            break
                                    else:
                                        found=body.find('!sellcassandra')
                                        if found != -1:
                                            try:
                                                posts_replied_to.append(results.id)
                                                results.save()
                                                conn = create_connection(r"currency_sqlite_test.db")
                                                with conn:
                                                    reply = sell_card(conn, "Cassandra Vablatsky", results.author.name)
                                                    results.reply(reply)
                                            except:
                                                break
                                        else:
                                            found=body.find('!sellalbus')
                                            if found != -1:
                                                try:
                                                    posts_replied_to.append(results.id)
                                                    results.save()
                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                    with conn:
                                                        reply = sell_card(conn, "Albus Dumbledore", results.author.name)
                                                        results.reply(reply)
                                                except:
                                                    break
                                            else:
                                                found=body.find('!sellflavius')
                                                if found != -1:
                                                    try:
                                                        posts_replied_to.append(results.id)
                                                        results.save()
                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                        with conn:
                                                            reply = sell_card(conn, "Flavius Belby", results.author.name)
                                                            results.reply(reply)
                                                    except:
                                                        break
                                                else:
                                                    found=body.find('!selluric')
                                                    if found != -1:
                                                        try:
                                                            posts_replied_to.append(results.id)
                                                            results.save()
                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                            with conn:
                                                                reply = sell_card(conn, "Uric the Oddball", results.author.name)
                                                                results.reply(reply)
                                                        except:
                                                            break
                                                    else:
                                                        found=body.find('!selladalbert')
                                                        if found != -1:
                                                            try:
                                                                posts_replied_to.append(results.id)
                                                                results.save()
                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                with conn:
                                                                    reply = sell_card(conn, "Adalbert Waffling", results.author.name)
                                                                    results.reply(reply)
                                                            except:
                                                                break
                                                        else:
                                                            found=body.find('!sellarchibald')
                                                            if found != -1:
                                                                try:
                                                                    posts_replied_to.append(results.id)
                                                                    results.save()
                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                    with conn:
                                                                        reply = sell_card(conn, "Archibald Alderton", results.author.name)
                                                                        results.reply(reply)
                                                                except:
                                                                    break
                                                            else:
                                                                found=body.find('!sellbowman')
                                                                if found != -1:
                                                                    try:
                                                                        posts_replied_to.append(results.id)
                                                                        results.save()
                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                        with conn:
                                                                            reply = sell_card(conn, "Bowman Wright", results.author.name)
                                                                            results.reply(reply)
                                                                    except:
                                                                        break
                                                                else:
                                                                    found=body.find('!sellchauncey')
                                                                    if found != -1:
                                                                        try:
                                                                            posts_replied_to.append(results.id)
                                                                            results.save()
                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                            with conn:
                                                                                reply = sell_card(conn, "Chauncey", results.author.name)
                                                                                results.reply(reply)
                                                                        except:
                                                                            break
                                                                    else:
                                                                        found=body.find('!sellburdock')
                                                                        if found != -1:
                                                                            try:
                                                                                posts_replied_to.append(results.id)
                                                                                results.save()
                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                with conn:
                                                                                    reply = sell_card(conn, "Burdock Muldoon", results.author.name)
                                                                                    results.reply(reply)
                                                                            except:
                                                                                break
                                                                        else:
                                                                            found=body.find('!sellgodric')
                                                                            if found != -1:
                                                                                try:
                                                                                    posts_replied_to.append(results.id)
                                                                                    results.save()
                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                    with conn:
                                                                                        reply = sell_card(conn, "Godric Gryffindor", results.author.name)
                                                                                        results.reply(reply)
                                                                                except:
                                                                                    break
                                                                            else:
                                                                                found=body.find('!sellrowena')
                                                                                if found != -1:
                                                                                    try:
                                                                                        posts_replied_to.append(results.id)
                                                                                        results.save()
                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                        with conn:
                                                                                            reply = sell_card(conn, "Rowena Ravenclaw", results.author.name)
                                                                                            results.reply(reply)
                                                                                    except:
                                                                                        break
                                                                                else:
                                                                                    found=body.find('!sellhelga')
                                                                                    if found != -1:
                                                                                        try:
                                                                                            posts_replied_to.append(results.id)
                                                                                            results.save()
                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                            with conn:
                                                                                                reply = sell_card(conn, "Helga Hufflepuff", results.author.name)
                                                                                                results.reply(reply)
                                                                                        except:
                                                                                            break
                                                                                    else:
                                                                                        found=body.find('!sellsalazar')
                                                                                        if found != -1:
                                                                                            try:
                                                                                                posts_replied_to.append(results.id)
                                                                                                results.save()
                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                with conn:
                                                                                                    reply = sell_card(conn, "Salazar Slytherin", results.author.name)
                                                                                                    results.reply(reply)
                                                                                            except:
                                                                                                break
                                                                                        else:
                                                                                            found=body.find('!sellgregory')
                                                                                            if found != -1:
                                                                                                try:
                                                                                                    posts_replied_to.append(results.id)
                                                                                                    results.save()
                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                    with conn:
                                                                                                        reply = sell_card(conn, "Gregory the Smarmy", results.author.name)
                                                                                                        results.reply(reply)
                                                                                                except:
                                                                                                    break
                                                                                            else:
                                                                                                found=body.find('!sellherpo')
                                                                                                if found != -1:
                                                                                                    try:
                                                                                                        posts_replied_to.append(results.id)
                                                                                                        results.save()
                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                        with conn:
                                                                                                            reply = sell_card(conn, "Herpo the Foul", results.author.name)
                                                                                                            results.reply(reply)
                                                                                                    except:
                                                                                                        break
                                                                                                else:
                                                                                                    found=body.find('!sellmungo')
                                                                                                    if found != -1:
                                                                                                        try:
                                                                                                            posts_replied_to.append(results.id)
                                                                                                            results.save()
                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                            with conn:
                                                                                                                reply = sell_card(conn, "Mungo Bonham", results.author.name)
                                                                                                                results.reply(reply)
                                                                                                        except:
                                                                                                            break
                                                                                                    else:
                                                                                                        found=body.find('!sellbertie')
                                                                                                        if found != -1:
                                                                                                            try:
                                                                                                                posts_replied_to.append(results.id)
                                                                                                                results.save()
                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                with conn:
                                                                                                                    reply = sell_card(conn, "Bertie Bott", results.author.name)
                                                                                                                    results.reply(reply)
                                                                                                            except:
                                                                                                                break
                                                                                                        else:
                                                                                                            found=body.find('!sellartemisia')
                                                                                                            if found != -1:
                                                                                                                try:
                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                    results.save()
                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                    with conn:
                                                                                                                        reply = sell_card(conn, "Artemisia Lufkin", results.author.name)
                                                                                                                        results.reply(reply)
                                                                                                                except:
                                                                                                                    break
                                                                                                            else:
                                                                                                                found=body.find('!sellnewt')
                                                                                                                if found != -1:
                                                                                                                    try:
                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                        results.save()
                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                        with conn:
                                                                                                                            reply = sell_card(conn, "Newt Scamander", results.author.name)
                                                                                                                            results.reply(reply)
                                                                                                                    except:
                                                                                                                        break
                                                                                                                else:
                                                                                                                    found=body.find('!sellelladora')
                                                                                                                    if found != -1:
                                                                                                                        try:
                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                            results.save()
                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                            with conn:
                                                                                                                                reply = sell_card(conn, "Elladora Ketteridge", results.author.name)
                                                                                                                                results.reply(reply)
                                                                                                                        except:
                                                                                                                            break
                                                                                                                    else:
                                                                                                                        found=body.find('!sellcelestina')
                                                                                                                        if found != -1:
                                                                                                                            try:
                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                results.save()
                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                with conn:
                                                                                                                                    reply = sell_card(conn, "Celestina Warbeck", results.author.name)
                                                                                                                                    results.reply(reply)
                                                                                                                            except:
                                                                                                                                break
                                                                                                                        else:
                                                                                                                            found=body.find('!sellcirce')
                                                                                                                            if found != -1:
                                                                                                                                try:
                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                    results.save()
                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                    with conn:
                                                                                                                                        reply = sell_card(conn, "Circe", results.author.name)
                                                                                                                                        results.reply(reply)
                                                                                                                                except:
                                                                                                                                    break
                                                                                                                            else:
                                                                                                                                found=body.find('!sellcornelius')
                                                                                                                                if found != -1:
                                                                                                                                    try:
                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                        results.save()
                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                        with conn:
                                                                                                                                            reply = sell_card(conn, "Cornelius Agrippa", results.author.name)
                                                                                                                                            results.reply(reply)
                                                                                                                                    except:
                                                                                                                                        break
                                                                                                                                else:
                                                                                                                                    found=body.find('!sellparacelsus')
                                                                                                                                    if found != -1:
                                                                                                                                        try:
                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                            results.save()
                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                            with conn:
                                                                                                                                                reply = sell_card(conn, "Paracelsus", results.author.name)
                                                                                                                                                results.reply(reply)
                                                                                                                                        except:
                                                                                                                                            break
                                                                                                                                    else:
                                                                                                                                        found=body.find('!sellwendelin')
                                                                                                                                        if found != -1:
                                                                                                                                            try:
                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                results.save()
                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                with conn:
                                                                                                                                                    reply = sell_card(conn, "Wendelin the Weird", results.author.name)
                                                                                                                                                    results.reply(reply)
                                                                                                                                            except:
                                                                                                                                                break
                                                                                                                                        else:
                                                                                                                                            found=body.find('!sellurg')
                                                                                                                                            if found != -1:
                                                                                                                                                try:
                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                    results.save()
                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                    with conn:
                                                                                                                                                        reply = sell_card(conn, "Urg the Unclean", results.author.name)
                                                                                                                                                        results.reply(reply)
                                                                                                                                                except:
                                                                                                                                                    break
                                                                                                                                            else:
                                                                                                                                                found=body.find('!sellmorgan')
                                                                                                                                                if found != -1:
                                                                                                                                                    try:
                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                        results.save()
                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                        with conn:
                                                                                                                                                            reply = sell_card(conn, "Morgan le Fay", results.author.name)
                                                                                                                                                            results.reply(reply)
                                                                                                                                                    except:
                                                                                                                                                        break
                                                                                                                                                else:
                                                                                                                                                    found=body.find('!sellptolemy')
                                                                                                                                                    if found != -1:
                                                                                                                                                        try:
                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                            results.save()
                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                            with conn:
                                                                                                                                                                reply = sell_card(conn, "Ptolemy", results.author.name)
                                                                                                                                                                results.reply(reply)
                                                                                                                                                        except:
                                                                                                                                                            break
                                                                                                                                                    else:
                                                                                                                                                        found=body.find('!sellharry')
                                                                                                                                                        if found != -1:
                                                                                                                                                            try:
                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                results.save()
                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                with conn:
                                                                                                                                                                    reply = sell_card(conn, "Harry Potter", results.author.name)
                                                                                                                                                                    results.reply(reply)
                                                                                                                                                            except:
                                                                                                                                                                break
                                                                                                                                                        else:
                                                                                                                                                            found=body.find('!sellmerlin')
                                                                                                                                                            if found != -1:
                                                                                                                                                                try:
                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                    results.save()
                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                    with conn:
                                                                                                                                                                        reply = sell_card(conn, "Merlin", results.author.name)
                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                except:
                                                                                                                                                                    break
                                                                                                                                                            else:
                                                                                                                                                                found=body.find('!buygryffindorrobes')
                                                                                                                                                                if found != -1:
                                                                                                                                                                    try:
                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                        results.save()
                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                        with conn:
                                                                                                                                                                            reply = buy_item(conn, "Gryffindor Robes", results.author.name)
                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                    except:
                                                                                                                                                                        break
                                                                                                                                                                else:
                                                                                                                                                                    found=body.find('!buyhufflepuffrobes')
                                                                                                                                                                    if found != -1:
                                                                                                                                                                        try:
                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                            results.save()
                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                            with conn:
                                                                                                                                                                                reply = buy_item(conn, "Hufflepuff Robes", results.author.name)
                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                        except:
                                                                                                                                                                            break
                                                                                                                                                                    else:
                                                                                                                                                                        found=body.find('!buyravenclawrobes')
                                                                                                                                                                        if found != -1:
                                                                                                                                                                            try:
                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                results.save()
                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                with conn:
                                                                                                                                                                                    reply = buy_item(conn, "Ravenclaw Robes", results.author.name)
                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                            except:
                                                                                                                                                                                break
                                                                                                                                                                        else:
                                                                                                                                                                            found=body.find('!buyslytherinrobes')
                                                                                                                                                                            if found != -1:
                                                                                                                                                                                try:
                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                    results.save()
                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                    with conn:
                                                                                                                                                                                        reply = buy_item(conn, "Slytherin Robes", results.author.name)
                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                except:
                                                                                                                                                                                    break
                                                                                                                                                                            else:
                                                                                                                                                                                found=body.find('!buydressrobes')
                                                                                                                                                                                if found != -1:
                                                                                                                                                                                    try:
                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                        results.save()
                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                        with conn:
                                                                                                                                                                                            reply = buy_item(conn, "Dress Robes", results.author.name)
                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                    except:
                                                                                                                                                                                        break
                                                                                                                                                                                else:
                                                                                                                                                                                    found=body.find('!buyhistory')
                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                        try:
                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                            results.save()
                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                            with conn:
                                                                                                                                                                                                reply = buy_item(conn, "Hogwarts, a History", results.author.name)
                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                        except:
                                                                                                                                                                                            break
                                                                                                                                                                                    else:
                                                                                                                                                                                        found=body.find('!buyquidditch')
                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                            try:
                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                results.save()
                                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                with conn:
                                                                                                                                                                                                    reply = buy_item(conn, "Quidditch Through the Ages", results.author.name)
                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                            except:
                                                                                                                                                                                                break
                                                                                                                                                                                        else:
                                                                                                                                                                                            found=body.find('!buybeasts')
                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                try:
                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                    with conn:
                                                                                                                                                                                                        reply = buy_item(conn, "Fantastic Beasts and Where to Find Them", results.author.name)
                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                except:
                                                                                                                                                                                                    break
                                                                                                                                                                                            else:
                                                                                                                                                                                                found=body.find('!buypewtercauldron')
                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                    try:
                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                        with conn:
                                                                                                                                                                                                            reply = buy_item(conn, "Pewter Cauldron", results.author.name)
                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                    except:
                                                                                                                                                                                                        break
                                                                                                                                                                                                else:
                                                                                                                                                                                                    found=body.find('!buygoldcauldron')
                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                        try:
                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                            with conn:
                                                                                                                                                                                                                reply = buy_item(conn, "Solid Gold Cauldron", results.author.name)
                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                        except:
                                                                                                                                                                                                            break
                                                                                                                                                                                                    else:
                                                                                                                                                                                                        found=body.find('!buytoad')
                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                            try:
                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                with conn:
                                                                                                                                                                                                                    reply = buy_item(conn, "Toad", results.author.name)
                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                            except:
                                                                                                                                                                                                                break
                                                                                                                                                                                                        else:
                                                                                                                                                                                                            found=body.find('!buybarnowl')
                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                try:
                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                    with conn:
                                                                                                                                                                                                                        reply = buy_item(conn, "Barn Owl", results.author.name)
                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                except:
                                                                                                                                                                                                                    break
                                                                                                                                                                                                            else:
                                                                                                                                                                                                                found=body.find('!buysnowyowl')
                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                        with conn:
                                                                                                                                                                                                                            reply = buy_item(conn, "Snowy Owl", results.author.name)
                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                        break
                                                                                                                                                                                                                else:
                                                                                                                                                                                                                    found=body.find('!buyblackcat')
                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                            with conn:
                                                                                                                                                                                                                                reply = buy_item(conn, "Black Cat", results.author.name)
                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                            break
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                        found=body.find('!buycleansweep')
                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                with conn:
                                                                                                                                                                                                                                    reply = buy_item(conn, "Cleansweep 7", results.author.name)
                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                break
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                            found=body.find('!buynimbus2000')
                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                    with conn:
                                                                                                                                                                                                                                        reply = buy_item(conn, "Nimbus 2000", results.author.name)
                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                found=body.find('!buynimbus2001')
                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                        with conn:
                                                                                                                                                                                                                                            reply = buy_item(conn, "Nimbus 2001", results.author.name)
                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                    found=body.find('!buyfirebolt')
                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                            with conn:
                                                                                                                                                                                                                                                reply = buy_item(conn, "Firebolt", results.author.name)
                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                        found=body.find('!buydragonliver')
                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                with conn:
                                                                                                                                                                                                                                                    reply = buy_item(conn, "Dragon Liver", results.author.name)
                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                            found=body.find('!buybeans')
                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                    with conn:
                                                                                                                                                                                                                                                        reply = buy_item(conn, "Bertie Bott's Every Flavor Beans", results.author.name)
                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                found=body.find('!buylicoricewand')
                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                        with conn:
                                                                                                                                                                                                                                                            reply = buy_item(conn, "Licorice Wand", results.author.name)
                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                    found=body.find('!givegryffindorrobes')
                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                            with conn:
                                                                                                                                                                                                                                                                reply = give_item(conn, "Gryffindor Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        found=body.find('!givehufflepuffrobes')
                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                with conn:
                                                                                                                                                                                                                                                                    reply = give_item(conn, "Hufflepuff Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            found=body.find('!giveravenclawrobes')
                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                    with conn:
                                                                                                                                                                                                                                                                        reply = give_item(conn, "Ravenclaw Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                found=body.find('!giveslytherinrobes')
                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                        with conn:
                                                                                                                                                                                                                                                                            reply = give_item(conn, "Slytherin Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                    found=body.find('!givedressrobes')
                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                            with conn:
                                                                                                                                                                                                                                                                                reply = give_item(conn, "Dress Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                        found=body.find('!givehistory')
                                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                with conn:
                                                                                                                                                                                                                                                                                    reply = give_item(conn, "Hogwarts, a History", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                            found=body.find('!givequidditch')
                                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                    with conn:
                                                                                                                                                                                                                                                                                        reply = give_item(conn, "Quidditch Through the Ages", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                found=body.find('!givebeasts')
                                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                        with conn:
                                                                                                                                                                                                                                                                                            reply = give_item(conn, "Fantastic Beasts and Where to Find Them", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                    found=body.find('!givepewtercauldron')
                                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                            with conn:
                                                                                                                                                                                                                                                                                                reply = give_item(conn, "Pewter Cauldron", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                        found=body.find('!givegoldcauldron')
                                                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                with conn:
                                                                                                                                                                                                                                                                                                    reply = give_item(conn, "Solid Gold Cauldron", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                            found=body.find('!givetoad')
                                                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                    with conn:
                                                                                                                                                                                                                                                                                                        reply = give_item(conn, "Toad", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                found=body.find('!givebarnowl')
                                                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                        with conn:
                                                                                                                                                                                                                                                                                                            reply = give_item(conn, "Barn Owl", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                    found=body.find('!givesnowyowl')
                                                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                            with conn:
                                                                                                                                                                                                                                                                                                                reply = give_item(conn, "Snowy Owl", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                        found=body.find('!giveblackcat')
                                                                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                                with conn:
                                                                                                                                                                                                                                                                                                                    reply = give_item(conn, "Black Cat", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                            found=body.find('!givecleansweep')
                                                                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                                    with conn:
                                                                                                                                                                                                                                                                                                                        reply = give_item(conn, "Cleansweep 7", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                found=body.find('!givenimbus2000')
                                                                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                                        with conn:
                                                                                                                                                                                                                                                                                                                            reply = give_item(conn, "Nimbus 2000", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                    found=body.find('!givenimbus2001')
                                                                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                                            with conn:
                                                                                                                                                                                                                                                                                                                                reply = give_item(conn, "Nimbus 2001", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                        found=body.find('!givefirebolt')
                                                                                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                                                                                conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                                                with conn:
                                                                                                                                                                                                                                                                                                                                    reply = give_item(conn, "Firebolt", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                            found=body.find('!givedragonliver')
                                                                                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                                                                                    conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                                                    with conn:
                                                                                                                                                                                                                                                                                                                                        reply = give_item(conn, "Dragon Liver", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                found=body.find('!givebeans')
                                                                                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                                                                                        conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                                                        with conn:
                                                                                                                                                                                                                                                                                                                                            reply = give_item(conn, "Bertie Bott's Every Flavor Beans", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                    found=body.find('!givelicoricewand')
                                                                                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                                                                                            conn = create_connection(r"currency_sqlite_test.db")
                                                                                                                                                                                                                                                                                                                                            with conn:
                                                                                                                                                                                                                                                                                                                                                reply = give_item(conn, "Licorice Wand", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                            break
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")

search()