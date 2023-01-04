import datetime
from . import db

class dbResult(db.Model):
      __tablename__='results'
      id=db.Column(db.Integer, primary_key=True, autoincrement=True)

      pot=db.Column(db.Integer, nullable=False)

      player=db.Column(db.Integer, default=0, nullable=False)
      dealer=db.Column(db.Integer, default=0, nullable=False)
      # updated_at=db.Column(db.Datetime, default=datetime.datetime.utcnow(), nullable=False)


