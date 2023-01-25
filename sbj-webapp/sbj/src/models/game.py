from enum import Enum
import datetime, random

from sbj.app import db
# from sbj.db import db

from enum import Enum
from sbj.src.models.handstatus import HandStatus

class GameStatus(Enum):
        PRE = 1
        ACTIVE = 2
        COMPLETE = 3


class dbGame(db.Model):
        __tablename__ = 'games'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        game_status = db.Column(
                db.String(), default="Complete", nullable=False)
        started_at = db.Column(
                db.DateTime,
                default=datetime.datetime.utcnow(),
                nullable=False
        )
        finished_at = db.Column(
                db.DateTime,
                nullable=True
        )


class Game(dbGame):
        def __init__(self, players):
                id = self.id
                self.game_status = GameStatus.PRE.name
                self.player = players["player"]


                self.player_id = None
                print('*****HELLO PLAYER ID: ', self.player_id)
                self.dealer=players["dealer"]
                self.dealer_id = None
                print('*****HELLO DEALER ID: ', self.dealer_id)
                # self.results=Result(players)
                self.deck = None
                self.play = False
                self.used_pile =[]

        def setplayerId(self,id):
                self.player_id = id

        def setdealerId(self, id):
            self.dealer_id = id
            
        def sortDeck(self):
                random.shuffle(self.deck)


        def setDeck(self, deck):
                self.deck = deck
                self.sortDeck

        def play_game(self):
                self.game_status= GameStatus.ACTIVE.name
                self.play = True

        def deal_from_deck(self, amnt_of_cards):
                count = 0
                cards_dealt = []
                while count< amnt_of_cards:
                        cards_dealt.append(self.deck.pop(random.randrange(0, len(self.deck))))
                        count += 1
                for cd in cards_dealt:
                        print(cd.serialize())
                        cd.used = True
                        print(cd.serialize())

                return cards_dealt


        def serialize(self):
                return {
                'id': self.id,
                'game_status': self.game_status,
                'started_at': self.started_at,
                'finished_at': self.finished_at
                }


        def set_score(self):
                if self.dealer.hand.status == HandStatus.BLACKJACK.name and self.player.hand.status == HandStatus.BLACKJACK.name:
                        self.results.draw()
                elif self.dealer.hand.status == HandStatus.BLACKJACK.name:
                        self.results.dealer_won()
                elif self.player.hand.status == HandStatus.BLACKJACK.name:
                        self.results.player_won()
                elif self.player.hand.status == HandStatus.HOLD.name and self.dealer.hand.status == HandStatus.HOLD.name:
                        p_low = 99
                        p_high = 99
                        player_low = 0
                        d_low = 99
                        d_high = 99
                        dealer_low = 0

                        if self.player.hand.value["high"] < 21:
                                p_high = 21 - self.player.hand.value["high"]

                        if self.player.hand.value["low"] < 21:
                                p_low = 21 - self.player.hand.value["high"]

                        if self.dealer.hand.value["high"] < 21:
                                d_high = 21 - self.dealer.hand.value["high"]

                        if self.dealer.hand.value["low"] < 21:
                                d_low = 21 - self.dealer.hand.value["low"]

                        player_low = min(p_high, p_low)
                        dealer_low = min(d_low, d_high)

                        if player_low == dealer_low:
                                self.results.draw()
                        elif player_low < dealer_low:
                                self.results.player_won()
                        else:
                                self.results.dealer_won()
                elif self.player.hand.status == HandStatus.BUST.name and self.dealer.hand.status == HandStatus.BUST.name:
                        self.results.draw()
                elif self.player.hand.status == HandStatus.BUST.name:
                        self.results.dealer_won()
                elif self.dealer.hand.status == HandStatus.BUST.name:
                        self.results.player_won()
