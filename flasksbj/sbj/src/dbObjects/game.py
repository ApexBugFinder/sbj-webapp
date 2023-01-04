import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from enum import Enum


class GameStatus(Enum):
    PRE = 1
    ACTIVE = 2
    COMPLETE = 3
class dbGame(db.Model):
        __tablename__='games'
        id = db.Column(db.Integer,primary_key=True, autoincrement=True)
        game_status = db.Column(db.String(), default= "Complete",nullable=False)
        started_at = db.Column(
                        db.DateTime,
                        default=datetime.datetime.utcnow(),
                        nullable=False
                        )
        finished_at = db.Column(
                        db.DateTime,
                        nullable=True
        )




