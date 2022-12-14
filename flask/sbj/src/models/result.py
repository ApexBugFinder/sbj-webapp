import datetime
from . import db

class Result(db.Model):
      __tablename__='results'
      id=db.Column(db.Integer, primary_key=True, autoincrement=True)
      game_id=db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
      pot=db.Column(db.Integer, nullable=False)
      user_id=db.Column(db.Integer, nullable=False)
      dealer_id=db.Column(db.Integer, nullable=False)
      player=db.Column(db.Integer, default=0, nullable=False)
      dealer=db.Column(db.Integer, default=0, nullable=False)
      

      def __init__(self, players):
          self.dealer = 0
          self.player = 0
          self.pot = 0
          self.winner = ''
          self.players = players