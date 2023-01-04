from ...wsgi import  db


deck_cards_table = db.Table(
    'deckcards',
    db.Column(
        'deck_id', db.Integer,
        db.ForeignKey('decks.id'),
        primary_key=True
    ),
    db.Column(
        'card_id', db.Integer,
        db.ForeignKey('cards.id'),
        primary_key=True
    ),
    db.Column(
        'used', db.Boolean,
        default=False

    )
)


