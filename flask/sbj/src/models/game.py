from enum import Enum
import datetime
from . import db

class GameStatus(Enum):
            ACTIVE = 1
            COMPLETE = 2
class Game(db.Model):
        __tablename__='games'
        id = db.Column(db.Integer,primary_key=True, autoincrement=True)
        game_status = db.Column(db.String(), nullable=False)
        player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
        dealer_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
        started_at = db.Column(
                              db.DateTime,
                              default=datetime.datetime.utcnow,
                              nullable=False
                              )
        finished_at = db.Column(
                              db.DateTime,
                              nullable=True
        )
        decks = db.relationship('Deck', backref='game', cascade='all, delete')



        def __init__(self):
                  id = self.id
                  game_status = GameStatus.ACTIVE

        def serialize(self):
                  return {
                    'id': self.id,
                    'game_status': self.game_status,
                    'started_at': self.started_at,
                    'finished_at': self.finished_at
                  }


game_deck_table = db.Table(
  'gamedecks',
  db.Column(
    'game_id', db.Integer,
    db.ForeignKey('games.id'),
    primary_key=True
  ),
  db.Column(
    'deck_id', db.Integer,
    db.ForeignKey('decks.id'),
    primary_key=True
    )
)
