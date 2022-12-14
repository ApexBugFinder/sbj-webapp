import datetime
from . import db, Hand

class Player(db.Model):
          __tablename__='players'
          id=db.Column(db.Integer, primary_key=True, autoincrement=True)
          name= db.Column(db.String(128),unique=True,  nullable=False)
          limit=db.Column(db.Integer, default=0, nullable=False)


          def __init__(self, name:str):
            self.name = name
            self.limit = 0
            self.hand = Hand(self.limit)

          def serialize(self):
                  return {
                    'id': self.id,
                    'name': self.name,
                    'limit': self.limit
                  }