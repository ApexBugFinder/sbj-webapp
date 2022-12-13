from . import db

class Game(db.Model):
        __tablename__='games'
        id = db.Column(db.Integer,primary_key=True, autoincrement=True)
        decks = db.relationship('Deck', backref='game', cascade='all, delete')
        def __init__(self):
                  id = self.id

        def serialize(self):
                  return {
                    'id': self.id
                  }


game_deck = db.Table(
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
