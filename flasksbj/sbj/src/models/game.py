from enum import Enum
import datetime, random

# from db import db
from sbj.db import db

from enum import Enum


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

                self.player_id = self.player.id
                print('*****HELLO PLAYER ID: ', self.player_id)
                self.dealer=players["dealer"]
                self.dealer_id = self.dealer.id
                print('*****HELLO DEALER ID: ', self.dealer_id)
                # self.results=Result(players)
                self.deck = None
                self.play = False
                self.used_pile =[]


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



