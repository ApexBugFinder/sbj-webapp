import datetime
from enum import Enum
from .handstatus import HandStatus
from sbj.db import db
# from db import db

class dbHand(db.Model):
    __tablename__ = "hands"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(
        db.String, default=HandStatus.ACTIVE.name, nullable=False)
    player_limit = db.Column(db.Integer, nullable=False, default=0)
    h_value = db.Column(db.Integer, nullable=False, default=0)
    l_value = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow(),
        nullable=False)

class Hand(dbHand):
            def __init__(self, lim, userid):
                self.cards = []
                # self.cards_count = self.cards_count()
                self.value = {"high": 0, "low": 0}
                self.h_value = None
                self.l_value= None
                self.has_ace = False
                self.player_limit = lim
                self.status = HandStatus.ACTIVE.name
                self.user_id = userid



            def setHandLimit(self, lim):
                self.player_limit = lim


            def serialize(self):
                return {
                'id':self.id,
                'status':self.status,
                'player_limit': self.player_limit,
                'h_value':self.h_value,
                'l_value':self.l_value,
          

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
                                                      self.cards.append(card)
                                          elif "A" in card.face and self.has_ace == True:
                                                      self.value["high"] += card.h_value
                                                      self.value["low"] += card.l_value
                                                      self.cards.append(card)
                                          else:
                                                      self.value["high"] += card.h_value
                                                      self.value["low"] += card.h_value
                                                      self.cards.append(card)

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


