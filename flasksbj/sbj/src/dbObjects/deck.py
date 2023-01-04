import datetime

from ...wsgi import db



class dbDeck(db.Model):
          __tablename__='decks'
          id = db.Column(db.Integer, primary_key=True, autoincrement=True)
          created_at = db.Column(db.DateTime,
                                default=datetime.datetime.utcnow(), nullable=False)
