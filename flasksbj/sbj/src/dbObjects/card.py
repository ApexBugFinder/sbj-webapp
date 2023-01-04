from sbj.wsgi import db

class dbCard(db.Model):
        __tablename__='cards'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        h_value = db.Column(db.Integer, nullable=False, default=0)
        l_value = db.Column(db.Integer, nullable=False, default=0)
        face = db.Column(db.String(3), unique=True)
        suite= db.Column(db.String(8))
        url = db.Column(db.Text)






