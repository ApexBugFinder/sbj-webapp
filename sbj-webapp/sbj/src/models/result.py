import datetime
# from sbj.db import db
from sbj.app import db



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

    def dealer_won(self):

            self.dealer  = self.dealer + self.pot + 1
            self.pot = 0

            self.winner = self.players["dealer"].name
            print(f'WINNER: {self.winner}')
            return

    def player_won(self):

        self.player = self.player + self.pot + 1
        self.pot = 0

        self.winner = self.players["player"].name
        print(f'WINNER: {self.winner}')
        return

    def draw(self):
        self.pot += 1
        self.winner = "draw"
        print(f'WINNER: {self.winner.title()}')
        return