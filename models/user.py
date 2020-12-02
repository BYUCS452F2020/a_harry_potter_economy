from typing import Any, Dict, List
from models.item import Item
from models.card import Card


class User:
    def __init__(self, username:str, galleons:int=0, sickles:int=0, knuts:int=0, inventory:list=[], cards:list=[]) -> None:
        self.username:str = username
        self.galleons:int = galleons
        self.sickles:int = sickles
        self.knuts:int = knuts
        self.inventory:List[Item] = inventory
        self.cards:List[Card] = cards

    @staticmethod
    def from_dict(source:Dict):
        return User(source[u"username"], 
        source[u"galleons"], 
        source[u"sickles"], 
        source[u"knuts"], 
        inventory=source[u"inventory"], 
        cards=source[u"cards"])

    def to_dict(self) -> Dict[str, Any]:
        return {
            u"username": self.username,
            u"galleons": self.galleons,
            u"sickles": self.sickles,
            u"knuts": self.knuts,
            u"inventory": self.inventory,
            u"cards": self.cards,
        }
    
    @property
    def total_currency_value(self):
        return self._get_value_from_coins()


    def _get_value_from_coins(self):
        return (self.galleons * 493) + (self.sickles * 29) + self.knuts

    def set_coins(self, galleons, sickles, knuts):
        self.galleons = galleons
        self.sickles = sickles
        self.knuts = knuts

    @staticmethod
    def get_coins_from_value(value):
        galleons = value // 493
        value = value % 493
        sickles = value // 29
        knuts = value % 29
        return galleons, sickles, knuts

    def set_coins_from_value(self, value):
        self.galleons = value // 493
        value = value % 493
        self.sickles = value // 29
        self.knuts = value % 29

    def __repr__(self):
        return(
            f'User(\
                username={self.username}, \
                galleons={self.galleons}, \
                sickles={self.sickles} \
                knuts={self.knuts} \
                inventory={self.inventory} \
                cards={self.cards} \
            )'
        )
