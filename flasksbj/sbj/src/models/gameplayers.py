# from sbj.db import db
import datetime
from sbj.app import db

game_players_table = db.Table(
    'gameplayers',
    db.Column(
        'game_id', db.Integer,
        db.ForeignKey('games.id'),
        primary_key=True
    ),
    db.Column(
        'player_id', db.Integer,
        db.ForeignKey('players.id'),
        primary_key=True
    ),
    db.Column(
        'started_at', db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow(),
    )
)
