#!/tmp/reddit_bot_app/lib/python3.7/site-packages/
# coding: utf-8
#from /tmp/dumbledore-reddit-app/lib/python3.7/site-packages/praw import praw
import praw
#praw.path.insert(0, 'tmp/dumbledore-reddit-app/lib/python3.7/site-packages/')
import os
import random
from sqlite3 import Error
from database.firestore_db import FirestoreDatabase
from models.user import User


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

def search(reddit, db):
    posts_replied_to = []
    for results in reddit.subreddit('thetestingzone').comments():
        if results.id not in posts_replied_to:
            if not results.saved:
                body = results.body  # Grab the Comment
                body = body.lower()	
                found = body.find('!redditgalleon')
                if found != -1:
                    try:
                        posts_replied_to.append(results.id)
                        results.save()
                        name = results.parent().author.name
                        if results.author.name != name:
                            print("getting user")
                            user = db.get_user(name)
                            print("user got")
                            if user == 0:
                                user = User(name, 0, 0, 0)
                                print("adding user")
                                db.add_user(user)
                                print("user added")
                            galleons = user.galleons + 1
                            user.galleons = galleons
                            print("updating user")
                            db.update_user(user)
                            print("user updated")
                            galleonString = " galleon, " if user.galleons == 1 else " galleons, "
                            sickleString = " sickle, and " if user.sickles == 1 else " sickles, and "
                            knutString = " knut." if user.knuts == 1 else " knuts."
                            reply = "You have given u/" + name + " a Reddit Galleon.\n\nu/" + name + " has a total of " + str(user.galleons) + galleonString + str(user.sickles) + sickleString + str(user.knuts) + knutString
                            reply = reply + getGuideLinkText()
                            print("replying")
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
                                user = db.get_user(name)
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
                                    user = db.get_user(name)
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
                                            cardname = get_random_card()
                                            user = db.add_card_to_user(cardname, user.username)
                                            
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
                                    card_name = "Gwenog Jones"
                                    reply = f"Sold {card_name}"
                                    if found != -1:
                                        try:
                                            posts_replied_to.append(results.id)
                                            results.save()
                                            user = db.sell_card(card_name, results.author.name)
                                            results.reply(reply)
                                        except:
                                            break
                                    else:
                                        found=body.find('!sellcassandra')
                                        card_name = "Cassandra Vablatsky"
                                        reply = f"Sold {card_name}"
                                        if found != -1:
                                            try:
                                                posts_replied_to.append(results.id)
                                                results.save()
                                                user = db.sell_card(card_name, results.author.name)
                                                results.reply(reply)
                                            except:
                                                break
                                        else:
                                            found=body.find('!sellalbus')
                                            card_name = "Albus Dumbledore"
                                            reply = f"Sold {card_name}"
                                            if found != -1:
                                                try:
                                                    posts_replied_to.append(results.id)
                                                    results.save()
                                                    user = db.sell_card(card_name, results.author.name)
                                                    results.reply(reply)
                                                except:
                                                    break
                                            else:
                                                found=body.find('!sellflavius')
                                                card_name = "Flavius Belby"
                                                reply = f"Sold {card_name}"
                                                if found != -1:
                                                    try:
                                                        posts_replied_to.append(results.id)
                                                        results.save()
                                                        user = db.sell_card(card_name, results.author.name)
                                                        results.reply(reply)
                                                    except:
                                                        break
                                                else:
                                                    found=body.find('!selluric')
                                                    card_name = "Uric the Oddball"
                                                    reply = f"Sold {card_name}"
                                                    if found != -1:
                                                        try:
                                                            posts_replied_to.append(results.id)
                                                            results.save()
                                                            user = db.sell_card(card_name, results.author.name)
                                                            results.reply(reply)
                                                        except:
                                                            break
                                                    else:
                                                        found=body.find('!selladalbert')
                                                        card_name = "Adalbert Waffling"
                                                        reply = f"Sold {card_name}"
                                                        if found != -1:
                                                            try:
                                                                posts_replied_to.append(results.id)
                                                                results.save()
                                                                
                                                                user =db.sell_card(card_name, results.author.name)
                                                                results.reply(reply)
                                                            except:
                                                                break
                                                        else:
                                                            found=body.find('!sellarchibald')
                                                            card_name = "Archibald Alderton"
                                                            reply = f"Sold {card_name}"
                                                            if found != -1:
                                                                try:
                                                                    posts_replied_to.append(results.id)
                                                                    results.save()
                                                                    
                                                                    
                                                                    user =db.sell_card(card_name, results.author.name)
                                                                    results.reply(reply)
                                                                except:
                                                                    break
                                                            else:
                                                                found=body.find('!sellbowman')
                                                                card_name = "Bowman Wright"
                                                                reply = f"Sold {card_name}"
                                                                if found != -1:
                                                                    try:
                                                                        posts_replied_to.append(results.id)
                                                                        results.save()
                                                                        
                                                                        
                                                                        user =db.sell_card(card_name, results.author.name)
                                                                        results.reply(reply)
                                                                    except:
                                                                        break
                                                                else:
                                                                    found=body.find('!sellchauncey')
                                                                    card_name = "Chauncey"
                                                                    reply = f"Sold {card_name}"
                                                                    if found != -1:
                                                                        try:
                                                                            posts_replied_to.append(results.id)
                                                                            results.save()
                                                                            
                                                                            
                                                                            user =db.sell_card(card_name, results.author.name)
                                                                            results.reply(reply)
                                                                        except:
                                                                            break
                                                                    else:
                                                                        found=body.find('!sellburdock')
                                                                        card_name = "Burdock Muldoon"
                                                                        reply = f"Sold {card_name}"
                                                                        if found != -1:
                                                                            try:
                                                                                posts_replied_to.append(results.id)
                                                                                results.save()
                                                                                
                                                                                
                                                                                user =db.sell_card(card_name, results.author.name)
                                                                                results.reply(reply)
                                                                            except:
                                                                                break
                                                                        else:
                                                                            found=body.find('!sellgodric')
                                                                            card_name = "Godric Gryffindor"
                                                                            reply = f"Sold {card_name}"
                                                                            if found != -1:
                                                                                try:
                                                                                    posts_replied_to.append(results.id)
                                                                                    results.save()
                                                                                    
                                                                                    
                                                                                    user =db.sell_card(card_name, results.author.name)
                                                                                    results.reply(reply)
                                                                                except:
                                                                                    break
                                                                            else:
                                                                                found=body.find('!sellrowena')
                                                                                card_name = "Rowena Ravenclaw"
                                                                                reply = f"Sold {card_name}"
                                                                                if found != -1:
                                                                                    try:
                                                                                        posts_replied_to.append(results.id)
                                                                                        results.save()
                                                                                        
                                                                                        
                                                                                        user =db.sell_card(card_name, results.author.name)
                                                                                        results.reply(reply)
                                                                                    except:
                                                                                        break
                                                                                else:
                                                                                    found=body.find('!sellhelga')
                                                                                    card_name = "Helga Hufflepuff"
                                                                                    reply = f"Sold {card_name}"
                                                                                    if found != -1:
                                                                                        try:
                                                                                            posts_replied_to.append(results.id)
                                                                                            results.save()
                                                                                            
                                                                                            
                                                                                            user =db.sell_card(card_name, results.author.name)
                                                                                            results.reply(reply)
                                                                                        except:
                                                                                            break
                                                                                    else:
                                                                                        found=body.find('!sellsalazar')
                                                                                        card_name = "Salazar Slytherin"
                                                                                        reply = f"Sold {card_name}"
                                                                                        if found != -1:
                                                                                            try:
                                                                                                posts_replied_to.append(results.id)
                                                                                                results.save()
                                                                                                
                                                                                                
                                                                                                user =db.sell_card(card_name, results.author.name)
                                                                                                results.reply(reply)
                                                                                            except:
                                                                                                break
                                                                                        else:
                                                                                            found=body.find('!sellgregory')
                                                                                            card_name = "Gregory the Smarmy"
                                                                                            reply = f"Sold {card_name}"
                                                                                            if found != -1:
                                                                                                try:
                                                                                                    posts_replied_to.append(results.id)
                                                                                                    results.save()
                                                                                                    
                                                                                                    
                                                                                                    user =db.sell_card(card_name, results.author.name)
                                                                                                    results.reply(reply)
                                                                                                except:
                                                                                                    break
                                                                                            else:
                                                                                                found=body.find('!sellherpo')
                                                                                                card_name = "Herpo the Foul"
                                                                                                reply = f"Sold {card_name}"
                                                                                                if found != -1:
                                                                                                    try:
                                                                                                        posts_replied_to.append(results.id)
                                                                                                        results.save()
                                                                                                        
                                                                                                        
                                                                                                        user =db.sell_card(card_name, results.author.name)
                                                                                                        results.reply(reply)
                                                                                                    except:
                                                                                                        break
                                                                                                else:
                                                                                                    found=body.find('!sellmungo')
                                                                                                    card_name = "Mungo Bonham"
                                                                                                    reply = f"Sold {card_name}"
                                                                                                    if found != -1:
                                                                                                        try:
                                                                                                            posts_replied_to.append(results.id)
                                                                                                            results.save()
                                                                                                            
                                                                                                            
                                                                                                            user =db.sell_card(card_name, results.author.name)
                                                                                                            results.reply(reply)
                                                                                                        except:
                                                                                                            break
                                                                                                    else:
                                                                                                        found=body.find('!sellbertie')
                                                                                                        card_name = "Bertie Bott"
                                                                                                        reply = f"Sold {card_name}"
                                                                                                        if found != -1:
                                                                                                            try:
                                                                                                                posts_replied_to.append(results.id)
                                                                                                                results.save()
                                                                                                                
                                                                                                                
                                                                                                                user =db.sell_card(card_name, results.author.name)
                                                                                                                results.reply(reply)
                                                                                                            except:
                                                                                                                break
                                                                                                        else:
                                                                                                            found=body.find('!sellartemisia')
                                                                                                            card_name = "Artemisia Lufkin"
                                                                                                            reply = f"Sold {card_name}"
                                                                                                            if found != -1:
                                                                                                                try:
                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                    results.save()
                                                                                                                    
                                                                                                                    
                                                                                                                    user =db.sell_card(card_name, results.author.name)
                                                                                                                    results.reply(reply)
                                                                                                                except:
                                                                                                                    break
                                                                                                            else:
                                                                                                                found=body.find('!sellnewt')
                                                                                                                card_name = "Newt Scamander"
                                                                                                                reply = f"Sold {card_name}"
                                                                                                                if found != -1:
                                                                                                                    try:
                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                        results.save()
                                                                                                                        
                                                                                                                        
                                                                                                                        user =db.sell_card(card_name, results.author.name)
                                                                                                                        results.reply(reply)
                                                                                                                    except:
                                                                                                                        break
                                                                                                                else:
                                                                                                                    found=body.find('!sellelladora')
                                                                                                                    card_name = "Elladora Ketteridge"
                                                                                                                    reply = f"Sold {card_name}"
                                                                                                                    if found != -1:
                                                                                                                        try:
                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                            results.save()
                                                                                                                            
                                                                                                                        
                                                                                                                            user =db.sell_card(card_name, results.author.name)
                                                                                                                            results.reply(reply)
                                                                                                                        except:
                                                                                                                            break
                                                                                                                    else:
                                                                                                                        found=body.find('!sellcelestina')
                                                                                                                        card_name = "Celestina Warbeck"
                                                                                                                        reply = f"Sold {card_name}"
                                                                                                                        if found != -1:
                                                                                                                            try:
                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                results.save()
                                                                                                                                
                                                                                                                                
                                                                                                                                user =db.sell_card(card_name, results.author.name)
                                                                                                                                results.reply(reply)
                                                                                                                            except:
                                                                                                                                break
                                                                                                                        else:
                                                                                                                            found=body.find('!sellcirce')
                                                                                                                            card_name = "Circe"
                                                                                                                            reply = f"Sold {card_name}"
                                                                                                                            if found != -1:
                                                                                                                                try:
                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                    results.save()
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    user =db.sell_card(card_name, results.author.name)
                                                                                                                                    results.reply(reply)
                                                                                                                                except:
                                                                                                                                    break
                                                                                                                            else:
                                                                                                                                found=body.find('!sellcornelius')
                                                                                                                                card_name = "Cornelius Agrippa"
                                                                                                                                reply = f"Sold {card_name}"
                                                                                                                                if found != -1:
                                                                                                                                    try:
                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                        results.save()
                                                                                                                                        
                                                                                                                                        
                                                                                                                                        user =db.sell_card(card_name, results.author.name)
                                                                                                                                        results.reply(reply)
                                                                                                                                    except:
                                                                                                                                        break
                                                                                                                                else:
                                                                                                                                    found=body.find('!sellparacelsus')
                                                                                                                                    card_name = "Paracelsus"
                                                                                                                                    reply = f"Sold {card_name}"
                                                                                                                                    if found != -1:
                                                                                                                                        try:
                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                            results.save()
                                                                                                                                            
                                                                                                                                            
                                                                                                                                            user =db.sell_card(card_name, results.author.name)
                                                                                                                                            results.reply(reply)
                                                                                                                                        except:
                                                                                                                                            break
                                                                                                                                    else:
                                                                                                                                        found=body.find('!sellwendelin')
                                                                                                                                        card_name = "Wendelin the Weird"
                                                                                                                                        reply = f"Sold {card_name}"
                                                                                                                                        if found != -1:
                                                                                                                                            try:
                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                results.save()
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                user =db.sell_card(card_name, results.author.name)
                                                                                                                                                results.reply(reply)
                                                                                                                                            except:
                                                                                                                                                break
                                                                                                                                        else:
                                                                                                                                            found=body.find('!sellurg')
                                                                                                                                            card_name = "Urg the Unclean"
                                                                                                                                            reply = f"Sold {card_name}"
                                                                                                                                            if found != -1:
                                                                                                                                                try:
                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                    results.save()
                                                                                                                                                    
                                                                                                                                                    
                                                                                                                                                    user =db.sell_card(card_name, results.author.name)
                                                                                                                                                    results.reply(reply)
                                                                                                                                                except:
                                                                                                                                                    break
                                                                                                                                            else:
                                                                                                                                                found=body.find('!sellmorgan')
                                                                                                                                                card_name = "Morgan le Fay"
                                                                                                                                                reply = f"Sold {card_name}"
                                                                                                                                                if found != -1:
                                                                                                                                                    try:
                                                                                                                                                        posts_replied_to.append(results.id)
                                                                                                                                                        results.save()
                                                                                                                                                        
                                                                                                                                                        
                                                                                                                                                        user =db.sell_card(card_name, results.author.name)
                                                                                                                                                        results.reply(reply)
                                                                                                                                                    except:
                                                                                                                                                        break
                                                                                                                                                else:
                                                                                                                                                    found=body.find('!sellptolemy')
                                                                                                                                                    card_name = "Ptolemy"
                                                                                                                                                    reply = f"Sold {card_name}"
                                                                                                                                                    if found != -1:
                                                                                                                                                        try:
                                                                                                                                                            posts_replied_to.append(results.id)
                                                                                                                                                            results.save()
                                                                                                                                                            
                                                                                                                                                            
                                                                                                                                                            user =db.sell_card(card_name, results.author.name)
                                                                                                                                                            results.reply(reply)
                                                                                                                                                        except:
                                                                                                                                                            break
                                                                                                                                                    else:
                                                                                                                                                        found=body.find('!sellharry')
                                                                                                                                                        card_name = "Harry Potter"
                                                                                                                                                        reply = f"Sold {card_name}"
                                                                                                                                                        if found != -1:
                                                                                                                                                            try:
                                                                                                                                                                posts_replied_to.append(results.id)
                                                                                                                                                                results.save()
                                                                                                                                                                
                                                                                                                                                                
                                                                                                                                                                user =db.sell_card(card_name, results.author.name)
                                                                                                                                                                results.reply(reply)
                                                                                                                                                            except:
                                                                                                                                                                break
                                                                                                                                                        else:
                                                                                                                                                            found=body.find('!sellmerlin')
                                                                                                                                                            card_name = "Merlin"
                                                                                                                                                            reply = f"Sold {card_name}"
                                                                                                                                                            if found != -1:
                                                                                                                                                                try:
                                                                                                                                                                    posts_replied_to.append(results.id)
                                                                                                                                                                    results.save()
                                                                                                                                                                    
                                                                                                                                                                    
                                                                                                                                                                    user =db.sell_card(card_name, results.author.name)
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

    # posts_replied_to = 2
    search(reddit, db)

main()