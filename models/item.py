from typing import Any, Dict


class Item:
    def __init__(self, itemName:str, value:str) -> None:
        self.itemName:str = itemName
        self.value:int = value

    @staticmethod
    def from_dict(source):
        return Item(source[u"itemName"], source[u"value"])

    def to_dict(self) -> Dict[str, Any]:
        return {
            u"itemName": self.itemName,
            u"value": self.value
        }

    def __repr__(self):
        return(
            f'Item(\
                name={self.itemName}, \
                value={self.value} \
            )'
        )

