import datetime

from sbj.src.dbObjects.deck import dbDeck

#         # decks = db.relationship('Deck', backref='game', cascade='all, delete')

class Deck(dbDeck):
        def __init__(self):
                self.created_at = datetime.datetime.now()

        def serialize(self):
                return {
                'id': self.id,
                'created_at': self.created_at
                }


