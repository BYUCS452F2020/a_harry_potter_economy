import abc
from models.user import User
from models.card import Card
from models.item import Item


class IDatabase(abc.ABC):
    def __init__(self) -> None:
        pass

    # User methods
    @abc.abstractmethod
    def add_user(self, user:User):
        raise NotImplementedError("insert_user must be implemented by a concrete class")
    
    @abc.abstractmethod
    def update_user(self, user:User):
        raise NotImplementedError("update_user must be implemented by a concrete class")
    
    @abc.abstractmethod
    def get_user(self, user_name:str) -> User:
        raise NotImplementedError("get_user must be implemented by a concrete class")
   
    @abc.abstractmethod
    def delete_user(self, user_name:str):
        raise NotImplementedError("delete_user must be implemented by a concrete class")
    

    # Card methods
    @abc.abstractmethod
    def add_card_to_user(self, card_name:str, user_name:str):
        raise NotImplementedError("add_card_to_user must be implemented by a concrete class")

    @abc.abstractmethod
    def get_card(self, card_name:str) -> Card:
        raise NotImplementedError("get_card must be implemented by a concrete class")  

    @abc.abstractmethod
    def sell_card(self, card_name:str, user_name:str):
        raise NotImplementedError("sell_card must be implemented by a concrete class")  
 

    # Item methods
    @abc.abstractmethod
    def get_item(self, item_name:str)-> Item:
        raise NotImplementedError("get_item must be implemented by a concrete class")  
    
    @abc.abstractmethod
    def give_item_to_user(self, item_name:str, giver:str, receiver:str) -> bool:
        raise NotImplementedError("give_item_to_user must be implemented by a concrete class")  
    
    @abc.abstractmethod
    def add_item_to_user(self, item_name:str, user_name:str):
        raise NotImplementedError("add_item_to_user must be implemented by a concrete class")

