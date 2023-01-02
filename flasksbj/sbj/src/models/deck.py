import datetime
# from . import db
# from .game import game_deck_table
from . import db



class Deck(db.Model):
          __tablename__='decks'
          id = db.Column(db.Integer, primary_key=True, autoincrement=True)
          created_at = db.Column(db.DateTime,
                                default=datetime.datetime.utcnow(), nullable=False)
          # deck_game = db.relationship(
          #   'Game', secondary=game_deck_table,
          #   lazy='subquery',
          #   backref=db.backref('gamedecks_decks', lazy=True)
          # )
          # cards=db.relationship('Card', backref='deck', cascade='all,delete')

          def __init__(self):
                  self.created_at = datetime.datetime.now()

          def serialize(self):
                  return {
                    'id': self.id,
                    'created_at': self.created_at
                  }


