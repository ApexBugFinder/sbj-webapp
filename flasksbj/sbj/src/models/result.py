import datetime
from sbj.db import db
# from db import db



class dbResult(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    pot = db.Column(db.Integer, nullable=False)

    player = db.Column(db.Integer, default=0, nullable=False)
    dealer = db.Column(db.Integer, default=0, nullable=False)
    # updated_at=db.Column(db.Datetime, default=datetime.datetime.utcnow(), nullable=False)




class Result(dbResult):
    def __init__(self, players):
        self.dealer = 0
        self.player = 0
        self.pot = 0
        self.winner = ''
        self.players = players
        self.player.id = players["player"]
        self.dealer.id = players['dealer']
