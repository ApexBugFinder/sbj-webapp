import datetime
from .handstatus import  HandStatus
# from sbj.db import db
from .hand import Hand
from sbj.app import db


class dbPlayer(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True,  nullable=False)
    limit = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow(),
        nullable=False
    )
class Player(dbPlayer):
          def __init__(self, name:str):
            self.name = name
            self.limit = 0
            self.hand = None
            self.id = None

          def initHand(self):
              if self.id != None:
                  print('PLAYER ID: ', self.id)
                  self.hand = Hand(lim=self.limit)
                  self.hand.setUserId(self.id)
                  self.hand.status = HandStatus.ACTIVE.name

              else:
                  print("Player does not have an id yet")


          def serialize(self):
                  return {
                    'id': self.id,
                    'name': self.name,
                    'limit': self.limit
                  }


          def change_limit(self, new_limit):

                    self.limit = new_limit
                    if self.hand != None:

                            self.hand.player_limit = new_limit

                    return self.limit

          def add_to_hand(self, cards ):
                if self.hand.status == HandStatus.ACTIVE.name:


                      self.hand.add_to_hand(cards)
