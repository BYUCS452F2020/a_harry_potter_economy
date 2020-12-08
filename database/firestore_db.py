import firebase_admin
from firebase_admin import credentials, firestore
from database.database import IDatabase
from models.user import User
from models.card import Card
from models.item import Item
from models.exception import InsufficientFundsException, UnownedItemException
import google.cloud.firestore_v1 as firestore_api

class FirestoreDatabase(IDatabase):
    def __init__(self, cred_path) -> None:
        super(FirestoreDatabase, self).__init__()
        self.creds = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(self.creds)
        self.firestore_db = firestore.client()
        self.user_coll_name = u'Users'
        self.card_coll_name = u'Cards'
        self.item_coll_name = u'Items'

    # User methods
    def add_user(self, user:User):
        user_coll_ref = self.firestore_db.collection(self.user_coll_name)
        user_coll_ref.add(user.to_dict(), document_id=user.username)
    
    def update_user(self, user:User):
        user_doc_ref = self.firestore_db.collection(self.user_coll_name).document(user.username)
        user_doc_ref.update(user.to_dict())
    
    def get_user(self, user_name:str):
        snapshot = self.firestore_db.collection(self.user_coll_name).document(user_name).get()
        return User.from_dict(snapshot.to_dict())

    def delete_user(self, user_name:str):
        user_doc_ref = self.firestore_db.collection(self.user_coll_name).document(user_name)
        user_doc_ref.delete()

    # Card methods
    def add_card_to_user(self, card_name:str, user_name:str):
        card_cost = 377 # 13 sickles
        user_doc_ref = self.firestore_db.collection(self.user_coll_name).document(user_name)
        user = User.from_dict(user_doc_ref.get().to_dict())
        if user.total_currency_value > card_cost:
            new_value = user.total_currency_value - card_cost
            user.set_coins(*User.get_coins_from_value(new_value))
            card_doc_ref = self.firestore_db.collection(self.card_coll_name).document(card_name)
            user_doc_ref.update({
                u'cards': firestore_api.ArrayUnion([card_doc_ref.path]),
                u'galleons': user.galleons,
                u'sickles': user.sickles,
                u'knuts': user.knuts
            })
        else:
            raise InsufficientFundsException("You do not have enough wizard gold to purchase a chocolate frog", user=user)
            

    def get_card(self, card_name:str) -> Card:
        snapshot = self.firestore_db.collection(self.card_coll_name).document(card_name).get()
        return Card.from_dict(snapshot.to_dict()) 

    def sell_card(self, card_name:str, user_name:str):
        user_doc_ref = self.firestore_db.collection(self.user_coll_name).document(user_name)
        user = User.from_dict(user_doc_ref.get().to_dict())
        user_owned_cards = [ref.path.split("/")[-1] for ref in user.cards]
        card_doc_ref = self.firestore_db.collection(self.card_coll_name).document(card_name)
        card = Card.from_dict(card_doc_ref.get().to_dict())
        
        if card_name in user_owned_cards:
            new_value = user.total_currency_value + card.value
            user.set_coins(*User.get_coins_from_value(new_value))
            user_doc_ref.update({
                u'cards': firestore_api.ArrayRemove([card_doc_ref.path]),
                u'galleons': user.galleons,
                u'sickles': user.sickles,
                u'knuts': user.knuts
            })
        else: 
            raise UnownedItemException("You cannot sell that card because you do not own it.", user=user)
 

    # Item methods
    def get_item(self, item_name:str)-> Item:
        snapshot = self.firestore_db.collection(self.item_coll_name).document(item_name).get()
        return Item.from_dict(snapshot.to_dict())  
    
    def give_item_to_user(self, item_name:str, giver:str, receiver:str) -> bool:
        giver_doc_ref = self.firestore_db.collection(self.user_coll_name).document(giver)
        giver_user = User.from_dict(giver_doc_ref.get().to_dict())
        giver_owned_items = [ref.path.split("/")[-1] for ref in giver_user.inventory]
        item_doc_ref = self.firestore_db.collection(self.item_coll_name).document(item_name)
        
        if item_name in giver_owned_items:
            receiver_doc_ref = self.firestore_db.collection(self.user_coll_name).document(receiver)
            # Add item to receiver inventory
            receiver_doc_ref.update({u'inventory': firestore_api.ArrayUnion([item_doc_ref.path])})
            # Remove item from giver inventory
            giver_doc_ref.update({u'inventory': firestore_api.ArrayRemove([item_doc_ref.path])})
        else:
            raise UnownedItemException(f"You can't give {item_name} because you don't own it", user=giver_user, item_name=item_name)
    
    def add_item_to_user(self, item_name:str, user_name:str):
        user_doc_ref = self.firestore_db.collection(self.user_coll_name).document(user_name)
        user = User.from_dict(user_doc_ref.get().to_dict())
        item_doc_ref = self.firestore_db.collection(self.item_coll_name).document(item_name)
        item = Item.from_dict(item_doc_ref.get().to_dict())
        if user.total_currency_value > item.value:
            new_value = user.total_currency_value - item.value
            user.set_coins(*User.get_coins_from_value(new_value))
            user_doc_ref.update({
                u'iventory': firestore_api.ArrayUnion([item_doc_ref.path]),
                u'galleons': user.galleons,
                u'sickles': user.sickles,
                u'knuts': user.knuts
            }) 
        else:
            raise InsufficientFundsException(f"You do not have enough wizard gold to purchase {item_name}")
