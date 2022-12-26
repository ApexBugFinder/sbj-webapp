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
            # cards=db.relationship(
            #   'Card', backref='hand')

            def __init__(self, lim):
                  self.cards = set()
                  # self.cards_count = self.cards_count()
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

            def set_game_id(self, gameid):
                    self.game_id = gameid

            def add_to_hand(self, cards):
                        # If 1st card is the first card that is an ACE then add to  hand and use high value
                        # If 2nd Ace added then use low value of card
                        #  Any other card just add the high value
                        # print("Adding cards to player hand")
                        if self.status == HandStatus.ACTIVE.name:
                              # print_cards(cards)
                              for card in cards:
                                    # print(f"Card being added to hand: {card.face}")
                                    if card.face != None:

                                          if "A" in card.face and self.has_ace == False:
                                                  self.value["high"] += card.h_value
                                                  self.value["low"] += card.l_value
                                                  self.has_ace = True
                                                  self.cards.add(card)
                                          elif "A" in card.face and self.has_ace == True:
                                                  self.value["high"] += card.l_value
                                                  self.value["low"] += card.l_value
                                                  self.cards.add(card)
                                          else:
                                                  self.value["high"] += card.h_value
                                                  self.value["low"] += card.h_value
                                                  self.cards.add(card)

                        return self.manage_status()

            def cards_count(self):
                                    return len(self.cards)

            def hand_status_active(self):
                  self.status = HandStatus.ACTIVE.name
                  # print(f"Hand status set to {self.status}")

            def hand_status_hold(self):
                  self.status = HandStatus.HOLD.name
                  # print(f"Hand status set to {self.status}")
            def hand_status_blackjack(self):
                  self.status = HandStatus.BLACKJACK.name
                  # print(f"Hand status set to {self.status}")
            def hand_status_bust(self):
                  self.status = HandStatus.BUST.name
                  # print(f"Hand status set to {self.status}")

            def manage_status(self):
                  # print("MANAGING STATUS")
                  # print(f"player limit: {self.player_limit}")
                  # print(f"self lower value: {self.value['low']}")
                  # print(f"self high value: {self.value['high']} ")
                  if self.value["high"] == 21 or self.value["low"] == 21:
                        self.hand_status_blackjack()
                  elif self.value["high"] < 21 and self.player_limit != 0 and self.value["high"] > self.player_limit:
                        self.hand_status_hold()
                  elif len(self.cards) == 5 and self.value["low"] < 21:
                        self.hand_status_blackjack()
                  elif self.value["low"] > 21:
                        # print('BUST')
                        self.hand_status_bust()
                        
                  elif self.player_limit !=0 and self.value["low"] >= self.player_limit and self.value["low"] < 21:

                        self.hand_status_hold()


                  else:
                        self.hand_status_active()
                  return self.status


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
    default=datetime.datetime.utcnow(),
    nullable=False
  )
)