import datetime
from . import db, Hand

class Player(db.Model):
          __tablename__='players'
          id=db.Column(db.Integer, primary_key=True, autoincrement=True)
          name= db.Column(db.String(), nullable=False)
          limit=db.Column(db.Integer, default=0, nullable=False)


          def __init__(self, name):
            self.name = name
            self.limit = 0
            self.hand = Hand(self.limit)
