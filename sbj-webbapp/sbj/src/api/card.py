from flask import Blueprint, jsonify, abort, request
from sbj.src.models.card import Card
# from src.models.card import Card
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
# from sbj.db import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo=True)

Sesson = sessionmaker(bind=engine)
session = Sesson()

bp = Blueprint('cards', __name__, url_prefix='/api/cards')



# CREATE
@bp.route('/', methods=['POST'])
def create():
        if 'face' not in request.json or 'suite'not in request.json or 'url' not in request.json:
                return abort(400)

        c = Card(
        face=request.json['face'],
        h_value=request.json['h_value'],
        l_value=request.json['l_value'],
        suite=request.json['suite'],
        url=request.json['url']
        )
        session.add(c)
        session.commit()
        return jsonify(c.serialize())


# READ ALL
@bp.route('/read/all', methods=['GET'])
def index():
        # cards = Card.query.all()
        cards = session.query(Card).all()
        result = []
        for card in cards:
                result.append(card.serialize())
        return jsonify(result)

# GET BY ID
@bp.route('/read/<int:id>', methods=['GET'])
def show_by_id(id:int):
        c = session.query(Card).where(Card.id == id)
        result = []
        for card in c:
                result.append(card.serialize())

        return jsonify(result)

# UPDATE
@bp.route('/<int:id>', methods=['PUT'])
def updateCard(id:int):
        c = Card.query.get_or_404(id)

        if 'url' in request.json:
                c.url = request.json['url']
        try:
                session.add(c)
                session.commit()
                return jsonify(c.serialize())
        except:
                return jsonify(False)


# DELETE
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
        c = Card.query.get_or_404(id)
        try:
                session.delete(c)
                session.commit()
                return jsonify(True)
        except:
                return jsonify(False)


