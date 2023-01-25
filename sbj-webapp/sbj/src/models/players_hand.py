# from sbj.db import db
from sbj.app import db

players_hand_table = db.Table(
    'playershands',
    db.Column(
        'player_id', db.Integer,
        db.ForeignKey('players.id'),
        primary_key=True
    ),
    db.Column(
        'hand_id', db.Integer,
        db.ForeignKey('hands.id'),
        primary_key=True
    )
)
