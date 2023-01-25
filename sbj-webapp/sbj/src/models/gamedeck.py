from sbj.app import db
# from sbj.db import db

game_deck_table = db.Table(
    'gamedecks',
    db.Column(
        'game_id', db.Integer,
        db.ForeignKey('games.id'),
        primary_key=True
    ),
    db.Column(
        'deck_id', db.Integer,
        db.ForeignKey('decks.id'),
        primary_key=True
    )
)
