from enum import Enum
import random
from typing import Any, Dict

class Card:
    def __init__(self, cardName:str, rarityStr:str, value:str) -> None:
        self.cardName:str = cardName
        self.rarity:CardRarity = CardRarity[rarityStr]
        self.value:str = value
        

    @staticmethod
    def from_dict(source):
        return Card(source[u"cardName"], CardRarity[source[u"rarity"]], source[u"value"])

    def to_dict(self) -> Dict[str, Any]:
        return {
            u"cardName": self.cardName,
            u"rarity": self.rarity.name,
            u"value": self.value
        }

    def __repr__(self):
        return(
            f'Card(\
                name={self.cardName},\
                rarity={self.rarity.name},\
                value={self.value}\
            )'
        )

class CardRarity(Enum):
    common = "common",
    uncommon = "uncommon",
    rare = "rare",
    epic = "epic",
    legendary = "legendary"

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