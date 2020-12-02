from models.card import Card
from models.user import User
from models.item import Item


class InsufficientFundsException(Exception):
    def __init__(self, msg, user:User, item_name:str=None) -> None:
        self.msg = msg
        self.user = user
        self.item_name = item_name

    def __str__(self) -> str:
        return self.msg if self.msg is not None else f'Insufficient funds detected for {self.user.username}'

class UnownedItemException(Exception):
    def __init__(self, msg, user:User, item_name:str=None) -> None:
        self.msg = msg
        self.user = user
        self.item_name = item_name

    def __str__(self) -> str:
        return self.msg if self.msg is not None else f'Insufficient funds detected for {self.user.username}'