from enum import Enum
import datetime
from . import db
# from . import Result
class GameStatus(Enum):
            PRE = 1
            ACTIVE = 2
            COMPLETE = 3
class Game(db.Model):
        __tablename__='games'
        id = db.Column(db.Integer,primary_key=True, autoincrement=True)
        game_status = db.Column(db.String(), nullable=False)
        player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
        dealer_id = db.Column(db.Integer, db.ForeignKey('players.id'),  nullable=False)
        started_at = db.Column(
                              db.DateTime,
                              default=datetime.datetime.utcnow(),
                              nullable=False
                              )
        finished_at = db.Column(
                              db.DateTime,
                              nullable=True
        )
        # decks = db.relationship('Deck', backref='game', cascade='all, delete')



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



