from enum import Enum
import datetime
from sbj.src.dbObjects.game import dbGame

class GameStatus(Enum):
            PRE = 1
            ACTIVE = 2
            COMPLETE = 3
class Game(dbGame):
        def __init__(self, players):
                id = self.id
                self.game_status = GameStatus.COMPLETE.name
                self.player = players["player"]

                self.player_id = self.player.id
                print('*****HELLO PLAYER ID: ', self.player_id)
                self.dealer=players["dealer"]
                self.dealer_id = self.dealer.id
                # self.results=Result(players)
                self.deck = None
                self.play = False
                self.used_pile =[]


        def sortDeck(self, deck):
                self.deck.shuffle_deck()


        def serialize(self):
                return {
                'id': self.id,
                'game_status': self.game_status,
                'started_at': self.started_at,
                'finished_at': self.finished_at
                }



