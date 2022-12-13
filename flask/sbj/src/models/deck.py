from . import db
from .game  import game_deck
class Deck(db.Model):
          __tablename__='decks'
          id = db.Column(db.Integer, primary_key=True, autoincrement=True)
          deck_game = db.relationship(
            'Game', secondary=game_deck,
            lazy='subquery',
            backref=db.backref('gamedecks_decks', lazy=True)
          )

          def __init__(self):
                  id = self.id

          def serialize(self):
                  return {
                    'id': self.id
                  }