import datetime
from ...wsgi import db
from ..models.handstatus import HandStatus

# from ..api import hand




class dbHand(db.Model):
            __tablename__= "hands"
            id = db.Column(db.Integer, primary_key=True, autoincrement=True)
            status=db.Column(db.String, default=HandStatus.ACTIVE.name, nullable=False)
            player_limit=db.Column(db.Integer, nullable=False, default=0)
            h_value=db.Column(db.Integer, nullable=False, default=0)
            l_value=db.Column(db.Integer, nullable=False, default=0)
            created_at=db.Column(
                              db.DateTime,
                              default=datetime.datetime.utcnow(),
                              nullable=False)

#             # cards=db.relationship(
#             #   'Card', backref='hand')
