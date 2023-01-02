from . import db
import datetime
hand_cards_table = db.Table(
    'handcards',
    db.Column('hand_id', db.Integer,
              db.ForeignKey('hands.id'),
              primary_key=True
              ),
    db.Column('card_id', db.Integer,
              db.ForeignKey('cards.id'),
              primary_key=True
              ),
    db.Column(
        'added_to_hand_at', db.DateTime,
        default=datetime.datetime.utcnow(),
        nullable=False
    )
)
