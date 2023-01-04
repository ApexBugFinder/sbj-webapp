import datetime
from ...wsgi import db

class dbPlayer(db.Model):
          __tablename__='players'
          id=db.Column(db.Integer, primary_key=True, autoincrement=True)
          name= db.Column(db.String(128),unique=True,  nullable=False)
          limit=db.Column(db.Integer, default=0, nullable=False)
          created_at = db.Column(
              db.DateTime,
              default=datetime.datetime.utcnow(),
              nullable=False
          )



