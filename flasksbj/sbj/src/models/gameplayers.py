from . import db

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
    )
)
