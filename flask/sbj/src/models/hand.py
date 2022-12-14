import datetime
from . import db
from enum import Enum

class HandStatus(Enum):
      ACTIVE = 1
      HOLD = 2
      BLACKJACK = 3
      BUST = 4


class Hand(db.Model):
            __tablename__= "hands"
            id = db.Column(db.Integer, primary_key=True, autoincrement=True)
            status=db.Column(db.String, default=HandStatus.ACTIVE.name, nullable=False)
            player_limit=db.Column(db.Integer, nullable=False, default=0)
            h_value=db.Column(db.Integer, nullable=False, default=0)
            l_value=db.Column(db.Integer, nullable=False, default=0)
            user_id=db.Column(db.Integer,db.ForeignKey('players.id'),  nullable=False)
            game_id=db.Column(db.Integer, db.ForeignKey('games.id'),nullable=False)
            cards=db.relationship(
              'Card', backref='hand')

            def __init__(self, lim):
                  self.cards = set()
                  self.cards_count = self.cards_count()
                  self.value ={ "high": 0, "low":0}
                  self.has_ace = False
                  self.player_limit = lim
                  self.status = HandStatus.ACTIVE.name

            def serialize(self):
                    return {
                      'id':self.id,
                      'status':self.status,
                      'player_limit': self.player_limit,
                      'h_value':self.value['high'],
                      'l_value':self.value['low'],
                      'user_id': self.user_id,
                      'game_id': self.game_id
                    }








hand_cards_table=db.Table(
  'handcards',
  db.Column('hand_id', db.Integer,
            db.ForeignKey('hands.id'),
            primary_key=True
  ),
  db.Column('card_id', db.Integer,
            db.ForeignKey('cards.id'),
            primary_key=True
  ),
  db.Column(
    'added_to_hand_at', db.DateTime,
    default=datetime.datetime.utcnow,
    nullable=False
  )
)