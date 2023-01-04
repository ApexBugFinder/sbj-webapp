# from . import db
from ..dbObjects.card import dbCard
class Card(dbCard):
        def __init__(self,face:str=None, suite:str=None, h_value:int=0, l_value:int=0, url:str=None):
                self.id=None
                self.face = face
                self.suite = suite
                self.value = h_value
                self.h_value = h_value
                self.l_value = l_value
                self.url = url
                self.possible_values = (h_value, l_value)

        def serialize(self):

                return  {
                        'id': self.id,
                        'face': self.face,
                        'suite': self.suite,

                        'h_value': self.h_value,
                        'l_value': self.l_value,
                        'url': self.url
                        }
        def set_deck_id(self, deck_id:int):
                  self.deck_id =deck_id

