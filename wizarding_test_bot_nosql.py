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


common_cards = ["Albus Dumbledore", "Flavius Belby", "Uric the Oddball", "Adalbert Waffling", "Archibald Alderton", "Bowman Wright", "Burdock Muldoon", "Chauncey Oldridge", "Cassandra Vablatsky", "Godric Gryffindor", "Rowena Ravenclaw", "Helga Hufflepuff", "Salazar Slytherin"]
uncommon_cards = ["Gregory the Smarmy", "Gwenog Jones", "Herpo the Foul", "Mungo Bonham", "Bertie Bott", "Artemisia Lufkin", "Newt Scamander", "Elladora Ketteridge"]
rare_cards = ["Celestina Warbeck", "Circe", "Cornelius Agrippa", "Paracelsus", "Wendelin the Weird"]
epic_cards = ["Urg the Unclean", "Morgan le Fay", "Ptolemy"]
legendary_cards = ["Harry Potter", "Merlin"]

card_links = {
    "Albus Dumbledore": "[Albus Dumbledore](https://harrypotter.fandom.com/wiki/Albus_Dumbledore_(Chocolate_Frog_Card))",
    "Flavius Belby": "[Flavius Belby](https://harrypotter.fandom.com/wiki/Flavius_Belby)",
    "Uric the Oddball": "[Uric the Oddball](https://harrypotter.fandom.com/wiki/Uric_the_Oddball)",
    "Adalbert Waffling": "[Adalbert Waffling](https://harrypotter.fandom.com/wiki/Adalbert_Waffling)",
    "Archibald Alderton": "[Archibald Alderton](https://harrypotter.fandom.com/wiki/Archibald_Alderton)",
    "Bowman Wright": "[Bowman Wright](https://harrypotter.fandom.com/wiki/Bowman_Wright)",
    "Burdock Muldoon": "[Burdock Muldoon](https://harrypotter.fandom.com/wiki/Burdock_Muldoon)",
    "Chauncey Oldridge": "[Chauncey Oldridge](https://harrypotter.fandom.com/wiki/Chauncey_Oldridge)",
    "Cassandra Vablatsky": "[Cassandra Vablatsky](https://harrypotter.fandom.com/wiki/Cassandra_Vablatsky)",
    "Godric Gryffindor": "[Godric Gryffindor](https://harrypotter.fandom.com/wiki/Godric_Gryffindor)",
    "Rowena Ravenclaw": "[Rowena Ravenclaw](https://harrypotter.fandom.com/wiki/Rowena_Ravenclaw)",
    "Helga Hufflepuff": "[Helga Hufflepuff](https://harrypotter.fandom.com/wiki/Helga_Hufflepuff)",
    "Salazar Slytherin": "[Salazar Slytherin](https://harrypotter.fandom.com/wiki/Salazar_Slytherin)",
    "Gregory the Smarmy": "[Gregory the Smarmy](https://harrypotter.fandom.com/wiki/Gregory_the_Smarmy)",
    "Gwenog Jones": "[Gwenog Jones](https://harrypotter.fandom.com/wiki/Gwenog_Jones)",
    "Herpo the Foul": "[Herpo the Foul](https://harrypotter.fandom.com/wiki/Herpo_the_Foul)",
    "Mungo Bonham": "[Mungo Bonham](https://harrypotter.fandom.com/wiki/Mungo_Bunham)",
    "Bertie Bott": "[Bertie Bott](https://harrypotter.fandom.com/wiki/Bertie_Bott)",
    "Artemisia Lufkin": "[Artemisia Lufkin](https://harrypotter.fandom.com/wiki/Artemisia_Lufkin)",
    "Newt Scamander": "[Newt Scamander](https://harrypotter.fandom.com/wiki/Newton_Scamander)",
    "Elladora Ketteridge": "[Elladora Ketteridge](https://harrypotter.fandom.com/wiki/Elladora_Ketteridge)",
    "Celestina Warbeck": "[Celestina Warbeck](https://harrypotter.fandom.com/wiki/Celestina_Warbeck)",
    "Circe": "[Circe](https://harrypotter.fandom.com/wiki/Circe)",
    "Cornelius Agrippa": "[Cornelius Agrippa](https://harrypotter.fandom.com/wiki/Cornelius_Agrippa)",
    "Paracelsus": "[Paracelsus](https://harrypotter.fandom.com/wiki/Phillipus_von_Hohenheim)",
    "Wendelin the Weird": "[Wendelin the Weird](https://harrypotter.fandom.com/wiki/Wendelin_the_Weird)",
    "Urg the Unclean": "[Urg the Unclean](https://harrypotter.fandom.com/wiki/Urg_the_Unclean)",
    "Morgan le Fay": "[Morgan le Fay](https://harrypotter.fandom.com/wiki/Morgan_le_Fay)",
    "Ptolemy": "[Ptolemy](https://harrypotter.fandom.com/wiki/Ptolemy)",
    "Harry Potter": "[Harry Potter](https://harrypotter.fandom.com/wiki/Harry_Potter)",
    "Merlin": "[Merlin](https://harrypotter.fandom.com/wiki/Merlin)"
}

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

def get_value_from_coins(galleons, sickles, knuts):
    return (galleons * 493) + (sickles * 29) + knuts

def get_coins_from_value(value):
    galleons = value // 493
    value = value % 493
    sickles = value // 29
    knuts = value % 29
    return [galleons, sickles, knuts]

def getGuideLinkText():
    return "\n\n____________\n\n" + "I am a bot. [Click here](https://www.reddit.com/user/ww-test-bot/comments/jjzc9n/a_guide_to_using_the_wizarding_world_currency_bot/) to learn how to use me."

def search(reddit, db, posts_replied_to):
    for results in reddit.subreddit('thetestingzone').comments():
        if results.id not in posts_replied_to:
            if not results.saved:
                body = results.body  # Grab the Comment
                body = body.lower()	
                found = body.find('!redditgalleon')
                if found != -1:
                    try:
                        # results.reply("bot is running")
                        posts_replied_to.append(results.id)
                        results.save()
                        name = results.parent().author.name
                        if results.author.name != name:
                            user = db.get_user(name)
                            if user == 0:
                                user = User(name, 0, 0, 0)
                                db.add_user(user)
                            galleons = user.galleons + 1
                            user.galleons = galleons
                            db.update_user(user)
                            galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                            sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                            knutString = " knut." if user.knuts == 1 else " knuts."
                            reply = "You have given u/" + name + " a Reddit Galleon.\n\nu/" + name + " has a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                            reply = reply + getGuideLinkText()
                            results.reply(reply)
                    except:
                        break
                else:
                    found = body.find('!redditsickle')
                    if found != -1:
                        try:
                            posts_replied_to.append(results.id)
                            results.save()
                            name = results.parent().author.name
                            if results.author.name != name:
                                db.get_user(name)
                                if user == 0:
                                    user = User(name, 0, 0, 0)
                                    db.add_user(user)
                                sickles = user.sickles + 1
                                if sickles == 17:
                                    galleons = user.galleons + 1
                                    user.galleons = galleons
                                    sickles = 0
                                user.sickles = sickles
                                db.update_user(user)
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
                                    user = db.get_user(name)
                                    if user == 0:
                                        user = User(name, 0, 0, 0)
                                        db.add_user(user)
                                    knuts = user.knuts + 1
                                    if knuts == 29:
                                        sickles = user.sickles + 1
                                        user.sickles = sickles
                                        knuts = 0
                                    user.knuts = knuts
                                    db.update_user(user)
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
                                    user = dbget_user(name)
                                    if user == 0:
                                        user = User(name, 0, 0, 0)
                                        db.add_user(user)
                                    galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                                    sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                                    knutString = " knut." if user.knuts == 1 else " knuts."
                                    reply = "You have a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                                    # reply = db.get_user_items_and_cards(conn, user.username, reply)
                                    if len(user.inventory) > 0:
                                        reply = reply + "\n\n" + "## You have the following items in your vault:\n"
                                        for item in user.inventory:
                                            reply = reply + "\n- " + item[0]
                                    if len(user.cards) > 0:
                                        reply = reply + "\n\n" + "## You have the following chocolate frog cards in your collection:\n"
                                        for card in user.cards:
                                            reply = reply + "\n- " + card_links.get(card[0])
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
                                        user = db.get_user(name)
                                        if user == 0:
                                            user = User(name, 0, 0, 0)
                                            db.add_user(user)
                                        user_value = get_value_from_coins(user.galleons, user.sickles, user.knuts)
                                        if user_value < 377:
                                            results.reply("You do not have enough wizard gold to purchase a chocolate frog. You need 13 Sickles.")
                                        else:
                                            coins = get_coins_from_value(user_value - 377)
                                            user.galleons = coins[0]
                                            user.sickles = coins[1]
                                            user.knuts = coins[2]
                                            db.update_user(user)
                                            
                                            cardname = get_random_card()
                                            db.add_card_to_user(cardname, user.username)
                                            
                                            galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                                            sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                                            knutString = " knut." if user.knuts == 1 else " knuts."
                                            reply = "You got the " + card_links.get(cardname) + " chocolate frog card!\n\n" + "13 sickles have been removed from your Gringotts vault, and you now have a balance of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
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
                                            reply = db.sell_card("Gwenog Jones", results.author.name)
                                            results.reply(reply)
                                        except:
                                            break
                                    else:
                                        found=body.find('!sellcassandra')
                                        if found != -1:
                                            try:
                                                posts_replied_to.append(results.id)
                                                results.save()
                                                reply = db.sell_card("Cassandra Vablatsky", results.author.name)
                                                results.reply(reply)
                                            except:
                                                break
                                        else:
                                            found=body.find('!sellalbus')
                                            if found != -1:
                                                try:
                                                    posts_replied_to.append(results.id)
                                                    results.save()
                                                    reply = db.sell_card("Albus Dumbledore", results.author.name)
                                                    results.reply(reply)
                                                except:
                                                    break
                                            else:
                                                found=body.find('!sellflavius')
                                                if found != -1:
                                                    try:
                                                        posts_replied_to.append(results.id)
                                                        results.save()
                                                        reply = db.sell_card("Flavius Belby", results.author.name)
                                                        results.reply(reply)
                                                    except:
                                                        break
                                                else:
                                                    found=body.find('!selluric')
                                                    if found != -1:
                                                        try:
                                                            posts_replied_to.append(results.id)
                                                            results.save()
                                                            reply = db.sell_card("Uric the Oddball", results.author.name)
                                                            results.reply(reply)
                                                        except:
                                                            break
                                                    else:
                                                        found=body.find('!selladalbert')
                                                        if found != -1:
                                                            try:
                                                                posts_replied_to.append(results.id)
                                                                results.save()
                                                                
                                                                reply =db.sell_card("Adalbert Waffling", results.author.name)
                                                                results.reply(reply)
                                                            except:
                                                                break
                                                        else:
                                                            found=body.find('!sellarchibald')
                                                            if found != -1:
                                                                try:
                                                                    posts_replied_to.append(results.id)
                                                                    results.save()
                                                                    
                                                                    
                                                                    reply =db.sell_card("Archibald Alderton", results.author.name)
                                                                    results.reply(reply)
                                                                except:
                                                                    break
                                                            else:
                                                                found=body.find('!sellbowman')
                                                                if found != -1:
                                                                    try:
                                                                        posts_replied_to.append(results.id)
                                                                        results.save()
                                                                        
                                                                        
                                                                        reply =db.sell_card("Bowman Wright", results.author.name)
                                                                        results.reply(reply)
                                                                    except:
                                                                        break
                                                                else:
                                                                    found=body.find('!sellchauncey')
                                                                    if found != -1:
                                                                        try:
                                                                            posts_replied_to.append(results.id)
                                                                            results.save()
                                                                            
                                                                            
                                                                            reply =db.sell_card("Chauncey", results.author.name)
                                                                            results.reply(reply)
                                                                        except:
                                                                            break
                                                                    else:
                                                                        found=body.find('!sellburdock')
                                                                        if found != -1:
                                                                            try:
                                                                                posts_replied_to.append(results.id)
                                                                                results.save()
                                                                                
                                                                                
                                                                                reply =db.sell_card("Burdock Muldoon", results.author.name)
                                                                                results.reply(reply)
                                                                            except:
                                                                                break
                                                                        else:
                                                                            found=body.find('!sellgodric')
                                                                            if found != -1:
                                                                                try:
                                                                                    posts_replied_to.append(results.id)
                                                                                    results.save()
                                                                                    
                                                                                    
                                                                                    reply =db.sell_card("Godric Gryffindor", results.author.name)
                                                                                    results.reply(reply)
                                                                                except:
                                                                                    break
                                                                            else:
                                                                                found=body.find('!sellrowena')
                                                                                if found != -1:
                                                                                    try:
                                                                                        posts_replied_to.append(results.id)
                                                                                        results.save()
                                                                                        
                                                                                        
                                                                                        reply =db.sell_card("Rowena Ravenclaw", results.author.name)
                                                                                        results.reply(reply)
                                                                                    except:
                                                                                        break
                                                                                else:
                                                                                    found=body.find('!sellhelga')
                                                                                    if found != -1:
                                                                                        try:
                                                                                            posts_replied_to.append(results.id)
                                                                                            results.save()
                                                                                            
                                                                                            
                                                                                            reply =db.sell_card("Helga Hufflepuff", results.author.name)
                                                                                            results.reply(reply)
                                                                                        except:
                                                                                            break
                                                                                    else:
                                                                                        found=body.find('!sellsalazar')
                                                                                        if found != -1:
                                                                                            try:
                                                                                                posts_replied_to.append(results.id)
                                                                                                results.save()
                                                                                                
                                                                                                
                                                                                                reply =db.sell_card("Salazar Slytherin", results.author.name)
                                                                                                results.reply(reply)
                                                                                            except:
                                                                                                break
                                                                                        else:
                                                                                            found=body.find('!sellgregory')
                                                                                            if found != -1:
                                                                                                try:
                                                                                                    posts_replied_to.append(results.id)
                                                                                                    results.save()
                                                                                                    
                                                                                                    
                                                                                                    reply =db.sell_card("Gregory the Smarmy", results.author.name)
                                                                                                    results.reply(reply)
                                                                                                except:
                                                                                                    break
                                                                                            else:
                                                                                                found=body.find('!sellherpo')
                                                                                                if found != -1:
                                                                                                    try:
                                                                                                        posts_replied_to.append(results.id)
                                                                                                        results.save()
                                                                                                        
                                                                                                        
                                                                                                        reply =db.sell_card("Herpo the Foul", results.author.name)
                                                                                                        results.reply(reply)
                                                                                                    except:
                                                                                                        break
                                                                                                else:
                                                                                                    found=body.find('!sellmungo')
                                                                                                    if found != -1:
                                                                                                        try:
                                                                                                            posts_replied_to.append(results.id)
                                                                                                            results.save()
                                                                                                            
                                                                                                            
                                                                                                            reply =db.sell_card("Mungo Bonham", results.author.name)
                                                                                                            results.reply(reply)
                                                                                                        except:
                                                                                                            break
                                                                                                    else:
                                                                                                        found=body.find('!sellbertie')
                                                                                                        if found != -1:
                                                                                                            try:
                                                                                                                posts_replied_to.append(results.id)
                                                                                                                results.save()
                                                                                                                
                                                                                                                
                                                                                                                reply =db.sell_card("Bertie Bott", results.author.name)
                                                                                                                results.reply(reply)
                                                                                                            except:
                                                                                                                break
                                                                                                        else:
                                                                                                            found=body.find('!sellartemisia')
                                                                                                            if found != -1:
                                                                                                                try:
                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                    results.save()
                                                                                                                    
                                                                                                                    
                                                                                                                    reply =db.sell_card("Artemisia Lufkin", results.author.name)
                                                                                                                    results.reply(reply)
                                                                                                                except:
                                                                                                                    break
                                                                                                            else:
                                                                                                                found=body.find('!sellnewt')
                                                                                                                if found != -1:
                                                                                                                    try:
                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                        results.save()
                                                                                                                        
                                                                                                                        
                                                                                                                        reply =db.sell_card("Newt Scamander", results.author.name)
                                                                                                                        results.reply(reply)
                                                                                                                    except:
                                                                                                                        break
                                                                                                                else:
                                                                                                                    found=body.find('!sellelladora')
                                                                                                                    if found != -1:
                                                                                                                        try:
                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                            results.save()
                                                                                                                            
                                                                                                                        
                                                                                                                            reply =db.sell_card("Elladora Ketteridge", results.author.name)
                                                                                                                            results.reply(reply)
                                                                                                                        except:
                                                                                                                            break
                                                                                                                    else:
                                                                                                                        found=body.find('!sellcelestina')
                                                                                                                        if found != -1:
                                                                                                                            try:
                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                results.save()
                                                                                                                                
                                                                                                                                
                                                                                                                                reply =db.sell_card("Celestina Warbeck", results.author.name)
                                                                                                                                results.reply(reply)
                                                                                                                            except:
                                                                                                                                break
                                                                                                                        else:
                                                                                                                            found=body.find('!sellcirce')
                                                                                                                            if found != -1:
                                                                                                                                try:
                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                    results.save()
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    reply =db.sell_card("Circe", results.author.name)
                                                                                                                                    results.reply(reply)
                                                                                                                                except:
                                                                                                                                    break
                                                                                                                            else:
                                                                                                                                found=body.find('!sellcornelius')
                                                                                                                                if found != -1:
                                                                                                                                    try:
                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                        results.save()
                                                                                                                                        
                                                                                                                                        
                                                                                                                                        reply =db.sell_card("Cornelius Agrippa", results.author.name)
                                                                                                                                        results.reply(reply)
                                                                                                                                    except:
                                                                                                                                        break
                                                                                                                                else:
                                                                                                                                    found=body.find('!sellparacelsus')
                                                                                                                                    if found != -1:
                                                                                                                                        try:
                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                            results.save()
                                                                                                                                            
                                                                                                                                            
                                                                                                                                            reply =db.sell_card("Paracelsus", results.author.name)
                                                                                                                                            results.reply(reply)
                                                                                                                                        except:
                                                                                                                                            break
                                                                                                                                    else:
                                                                                                                                        found=body.find('!sellwendelin')
                                                                                                                                        if found != -1:
                                                                                                                                            try:
                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                results.save()
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                reply =db.sell_card("Wendelin the Weird", results.author.name)
                                                                                                                                                results.reply(reply)
                                                                                                                                            except:
                                                                                                                                                break
                                                                                                                                        else:
                                                                                                                                            found=body.find('!sellurg')
                                                                                                                                            if found != -1:
                                                                                                                                                try:
                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                    results.save()
                                                                                                                                                    
                                                                                                                                                    
                                                                                                                                                    reply =db.sell_card("Urg the Unclean", results.author.name)
                                                                                                                                                    results.reply(reply)
                                                                                                                                                except:
                                                                                                                                                    break
                                                                                                                                            else:
                                                                                                                                                found=body.find('!sellmorgan')
                                                                                                                                                if found != -1:
                                                                                                                                                    try:
                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                        results.save()
                                                                                                                                                        
                                                                                                                                                        
                                                                                                                                                        reply =db.sell_card("Morgan le Fay", results.author.name)
                                                                                                                                                        results.reply(reply)
                                                                                                                                                    except:
                                                                                                                                                        break
                                                                                                                                                else:
                                                                                                                                                    found=body.find('!sellptolemy')
                                                                                                                                                    if found != -1:
                                                                                                                                                        try:
                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                            results.save()
                                                                                                                                                            
                                                                                                                                                            
                                                                                                                                                            reply =db.sell_card("Ptolemy", results.author.name)
                                                                                                                                                            results.reply(reply)
                                                                                                                                                        except:
                                                                                                                                                            break
                                                                                                                                                    else:
                                                                                                                                                        found=body.find('!sellharry')
                                                                                                                                                        if found != -1:
                                                                                                                                                            try:
                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                results.save()
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                reply =db.sell_card("Harry Potter", results.author.name)
                                                                                                                                                                results.reply(reply)
                                                                                                                                                            except:
                                                                                                                                                                break
                                                                                                                                                        else:
                                                                                                                                                            found=body.find('!sellmerlin')
                                                                                                                                                            if found != -1:
                                                                                                                                                                try:
                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                    results.save()
                                                                                                                                                                    
                                                                                                                                                                    
                                                                                                                                                                    reply =db.sell_card("Merlin", results.author.name)
                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                except:
                                                                                                                                                                    break
                                                                                                                                                            else:
                                                                                                                                                                found=body.find('!buygryffindorrobes')
                                                                                                                                                                if found != -1:
                                                                                                                                                                    try:
                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                        results.save()
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        reply = db.add_item_to_user("Gryffindor Robes", results.author.name)
                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                    except:
                                                                                                                                                                        break
                                                                                                                                                                else:
                                                                                                                                                                    found=body.find('!buyhufflepuffrobes')
                                                                                                                                                                    if found != -1:
                                                                                                                                                                        try:
                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                            results.save()
                                                                                                                                                                            
                                                                                                                                                                        
                                                                                                                                                                            reply = db.add_item_to_user("Hufflepuff Robes", results.author.name)
                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                        except:
                                                                                                                                                                            break
                                                                                                                                                                    else:
                                                                                                                                                                        found=body.find('!buyravenclawrobes')
                                                                                                                                                                        if found != -1:
                                                                                                                                                                            try:
                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                results.save()
                                                                                                                                                                                
                                                                                                                                                                                
                                                                                                                                                                                reply = db.add_item_to_user("Ravenclaw Robes", results.author.name)
                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                            except:
                                                                                                                                                                                break
                                                                                                                                                                        else:
                                                                                                                                                                            found=body.find('!buyslytherinrobes')
                                                                                                                                                                            if found != -1:
                                                                                                                                                                                try:
                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                    results.save()
                                                                                                                                                                                    
                                                                                                                                                                                    
                                                                                                                                                                                    reply = db.add_item_to_user("Slytherin Robes", results.author.name)
                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                except:
                                                                                                                                                                                    break
                                                                                                                                                                            else:
                                                                                                                                                                                found=body.find('!buydressrobes')
                                                                                                                                                                                if found != -1:
                                                                                                                                                                                    try:
                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                        results.save()
                                                                                                                                                                                        
                                                                                                                                                                                        
                                                                                                                                                                                        reply = db.add_item_to_user("Dress Robes", results.author.name)
                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                    except:
                                                                                                                                                                                        break
                                                                                                                                                                                else:
                                                                                                                                                                                    found=body.find('!buyhistory')
                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                        try:
                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                            results.save()
                                                                                                                                                                                            
                                                                                                                                                                                            
                                                                                                                                                                                            reply = db.add_item_to_user("Hogwarts, a History", results.author.name)
                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                        except:
                                                                                                                                                                                            break
                                                                                                                                                                                    else:
                                                                                                                                                                                        found=body.find('!buyquidditch')
                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                            try:
                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                results.save()
                                                                                                                                                                                                
                                                                                                                                                                                                
                                                                                                                                                                                                reply = db.add_item_to_user("Quidditch Through the Ages", results.author.name)
                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                            except:
                                                                                                                                                                                                break
                                                                                                                                                                                        else:
                                                                                                                                                                                            found=body.find('!buybeasts')
                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                try:
                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                    
                                                                                                                                                                                                    
                                                                                                                                                                                                    reply = db.add_item_to_user("Fantastic Beasts and Where to Find Them", results.author.name)
                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                except:
                                                                                                                                                                                                    break
                                                                                                                                                                                            else:
                                                                                                                                                                                                found=body.find('!buypewtercauldron')
                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                    try:
                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                        
                                                                                                                                                                                                        
                                                                                                                                                                                                        reply = db.add_item_to_user("Pewter Cauldron", results.author.name)
                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                    except:
                                                                                                                                                                                                        break
                                                                                                                                                                                                else:
                                                                                                                                                                                                    found=body.find('!buygoldcauldron')
                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                        try:
                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                            
                                                                                                                                                                                                            
                                                                                                                                                                                                            reply = db.add_item_to_user("Solid Gold Cauldron", results.author.name)
                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                        except:
                                                                                                                                                                                                            break
                                                                                                                                                                                                    else:
                                                                                                                                                                                                        found=body.find('!buytoad')
                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                            try:
                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                
                                                                                                                                                                                                                
                                                                                                                                                                                                                reply = db.add_item_to_user("Toad", results.author.name)
                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                            except:
                                                                                                                                                                                                                break
                                                                                                                                                                                                        else:
                                                                                                                                                                                                            found=body.find('!buybarnowl')
                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                try:
                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                    
                                                                                                                                                                                                                    
                                                                                                                                                                                                                    reply = db.add_item_to_user("Barn Owl", results.author.name)
                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                except:
                                                                                                                                                                                                                    break
                                                                                                                                                                                                            else:
                                                                                                                                                                                                                found=body.find('!buysnowyowl')
                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                        
                                                                                                                                                                                                                        
                                                                                                                                                                                                                        reply = db.add_item_to_user("Snowy Owl", results.author.name)
                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                        break
                                                                                                                                                                                                                else:
                                                                                                                                                                                                                    found=body.find('!buyblackcat')
                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                            
                                                                                                                                                                                                                            
                                                                                                                                                                                                                            reply = db.add_item_to_user("Black Cat", results.author.name)
                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                            break
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                        found=body.find('!buycleansweep')
                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                reply = db.add_item_to_user("Cleansweep 7", results.author.name)
                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                break
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                            found=body.find('!buynimbus2000')
                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                    reply = db.add_item_to_user("Nimbus 2000", results.author.name)
                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                found=body.find('!buynimbus2001')
                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                        reply = db.add_item_to_user("Nimbus 2001", results.author.name)
                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                    found=body.find('!buyfirebolt')
                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                            reply = db.add_item_to_user("Firebolt", results.author.name)
                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                        found=body.find('!buydragonliver')
                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                reply = db.add_item_to_user("Dragon Liver", results.author.name)
                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                            found=body.find('!buybeans')
                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                    reply = db.add_item_to_user("Bertie Bott's Every Flavor Beans", results.author.name)
                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                found=body.find('!buylicoricewand')
                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                        reply = db.add_item_to_user("Licorice Wand", results.author.name)
                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                    found=body.find('!givegryffindorrobes')
                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                            reply = db.give_item_to_user("Gryffindor Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        found=body.find('!givehufflepuffrobes')
                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                reply = db.give_item_to_user("Hufflepuff Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            found=body.find('!giveravenclawrobes')
                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                    reply = db.give_item_to_user("Ravenclaw Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                found=body.find('!giveslytherinrobes')
                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                        reply = db.give_item_to_user("Slytherin Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                    found=body.find('!givedressrobes')
                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                            reply = db.give_item_to_user("Dress Robes", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                        found=body.find('!givehistory')
                                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                reply = db.give_item_to_user("Hogwarts, a History", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                            found=body.find('!givequidditch')
                                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                    reply = db.give_item_to_user("Quidditch Through the Ages", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                found=body.find('!givebeasts')
                                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                        reply = db.give_item_to_user("Fantastic Beasts and Where to Find Them", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                    found=body.find('!givepewtercauldron')
                                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                            reply = db.give_item_to_user("Pewter Cauldron", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                        found=body.find('!givegoldcauldron')
                                                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                reply = db.give_item_to_user("Solid Gold Cauldron", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                            found=body.find('!givetoad')
                                                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                    reply = db.give_item_to_user("Toad", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                found=body.find('!givebarnowl')
                                                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                        reply = db.give_item_to_user("Barn Owl", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                    found=body.find('!givesnowyowl')
                                                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                            reply = db.give_item_to_user("Snowy Owl", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                        found=body.find('!giveblackcat')
                                                                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                reply = db.give_item_to_user("Black Cat", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                            found=body.find('!givecleansweep')
                                                                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                    reply = db.give_item_to_user("Cleansweep 7", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                found=body.find('!givenimbus2000')
                                                                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                        reply = db.give_item_to_user("Nimbus 2000", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                    found=body.find('!givenimbus2001')
                                                                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                            reply = db.give_item_to_user("Nimbus 2001", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                        found=body.find('!givefirebolt')
                                                                                                                                                                                                                                                                                                                        if found != -1:
                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                                results.save()
                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                                                reply = db.give_item_to_user("Firebolt", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                                results.reply(reply)
                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                break
                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                            found=body.find('!givedragonliver')
                                                                                                                                                                                                                                                                                                                            if found != -1:
                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                                    results.save()
                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                    reply = db.give_item_to_user("Dragon Liver", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                                    results.reply(reply)
                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                    break
                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                found=body.find('!givebeans')
                                                                                                                                                                                                                                                                                                                                if found != -1:
                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                                        results.save()
                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                                        reply = db.give_item_to_user("Bertie Bott's Every Flavor Beans", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                                        results.reply(reply)
                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                        break
                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                    found=body.find('!givelicoricewand')
                                                                                                                                                                                                                                                                                                                                    if found != -1:
                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                                                                                                                                                                                                            results.save()
                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                                                            reply = db.give_item_to_user("Licorice Wand", results.author.name, results.parent().author.name)
                                                                                                                                                                                                                                                                                                                                            results.reply(reply)
                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                            break


                    

def main():
    assert os.environ['HP_FIREBASE_CREDS']
    db = FirestoreDatabase(os.environ['HP_FIREBASE_CREDS'])
    reddit = praw.Reddit(client_id="-4ByKCJuYOID4A", client_secret="we-8e_TZOCFsHmhmF8rZEPJTWLI", password="&2@X3G5BX6*v5K%a", username="ww-test-bot", user_agent="ww-test 1.0")
    
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")

    # posts_replied_to = 2
    search(reddit, db, posts_replied_to)
    
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")

main()