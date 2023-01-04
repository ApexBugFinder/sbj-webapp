import datetime
from .handstatus import  HandStatus
from ..dbObjects.player import dbPlayer


class Player(dbPlayer):
          def __init__(self, name:str):
            self.name = name
            self.limit = 0
            # self.hand = Hand(self.limit)

          def serialize(self):
                  return {
                    'id': self.id,
                    'name': self.name,
                    'limit': self.limit
                  }


          def change_limit(self, new_limit):

                    self.limit = new_limit
                    self.hand.player_limit = new_limit

                    return self.limit

          def add_to_hand(self, cards ):
                if self.hand.status == HandStatus.ACTIVE.name:


                      self.hand.add_to_hand(cards)
