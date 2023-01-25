import datetime, random

# from sbj.src.dbObjects.deck import dbDeck

#         # decks = db.relationship('Deck', backref='game', cascade='all, delete')



# from db import db
from sbj.db import db


class dbDeck(db.Model):
        __tablename__ = 'decks'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        created_at = db.Column(db.DateTime,
                                default=datetime.datetime.utcnow(), nullable=False)
class Deck(dbDeck):
        def __init__(self):
                self.created_at = datetime.datetime.now()

        def card_count(self):
                return len(self.deck)


        def add_to_deck(self, card):
                self.deck.append(card)
                # print('added card to deck: ', card.face)

        def deal_from_deck(self, amnt_of_cards):
                count =0
                cards_dealt = set()
                while count < amnt_of_cards:
                        cards_dealt.add(self.deck.pop(random.randrange(0, len(self.deck))))
                        count += 1

                return cards_dealt

        def print_deck(self):
                for i in self.deck:
                        print(i.face, i.value)

        def shuffle_deck(self):
                # print("PRE SHUFFLE")
                # for i in self.deck:
                #       print(i.face)

                random.shuffle(self.deck)
                # print("POST SHUFFLE")
                # for i in self.deck:
                #       print(i.face)

        def deck_count(self):
                return len(self.deck)

        def serialize(self):
                return {
                'id': self.id,
                'created_at': self.created_at
                }


