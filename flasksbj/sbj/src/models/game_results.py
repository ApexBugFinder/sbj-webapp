# from sbj.app import db
# from db import db
from sbj.db import db

game_results_table = db.Table(
    'gameresults',
    db.Column(
        'game_id', db.Integer,
        db.ForeignKey('games.id'),
        primary_key=True
    ),
    db.Column(
        'result_id', db.Integer,
        db.ForeignKey('results.id'),
        primary_key=True
    )
)
