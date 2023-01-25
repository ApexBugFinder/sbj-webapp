from flask import Blueprint, jsonify, abort, request
from flask_cors import CORS
from sbj.src.models.deck import Deck
from sbj.src.models.card import Card
from sbj.src.models.deckcard import DeckCard
from sbj.src.models.deckcard import deck_cards_table
from sbj.src.models.gamedeck import game_deck_table

from sbj.db import db

from sqlalchemy import create_engine, select, join
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo=True)

Sesson = sessionmaker(bind=engine)
session = Sesson()


import sqlalchemy

bp = Blueprint('decks', __name__, url_prefix='/api/decks')
CORS(bp)



# CREATE
@bp.route('/create', methods=['POST'])
def create_deck():

        game_id = request.json['game.id']

        if not game_id:
                abort(400, "Must include game ID")
        new_deck = Deck()
        session.add(new_deck)
        session.commit()
        cardsQuery = session.query(Card).all()
        docs = []
        for card in cardsQuery:

                new_card = DeckCard(
                        card, deck_id=new_deck.id, used=False)
                print(new_card.serialize())
                docs.append(new_card)
        try:
                        stmt2 = sqlalchemy.insert(game_deck_table).values(
                                game_id=game_id, deck_id=new_deck.id)
                        session.execute(stmt2)

                        rt = []
                        for card in docs:
                                rt.append(card.serialize())
                                stmt = sqlalchemy.insert(deck_cards_table).values(deck_id=card.deck_id, card_id=card.id, used=card.used)
                                session.execute(stmt)


                        session.commit()
                        return jsonify(rt)


        except:
                return jsonify(False)

# READ BY ID
@bp.route('/read/<int:id>', methods=['GET'])
def get_by_id(id:int):
        d = session.query(Deck).filter(Deck.id==id)
        for record in d:
                print(record.serialize())
        try:
                j = deck_cards_table.join(Card).join(Deck, Deck.id==deck_cards_table.c.deck_id)
                select_stmt = select([deck_cards_table, Card, Card]).select_from(j)

                filter_stmt = select_stmt.filter(deck_cards_table.c.deck_id == id)

                result = session.execute(filter_stmt)
                rt = []
                for rec in result:

                        print(rec)
                        a = {
                                "deck.id": rec['deck_id'],
                                "used": rec['used'],
                                "card": (rec['Card']).serialize()
                        }
                        rt.append(a)


                return jsonify(rt)
        except:
                return jsonify(False, {"message": "Operation Failed to get deckcards"})




# READ ALL
@bp.route('/show_all', methods=['GET'])
def index():

    decks= session.query(Deck).filter(Deck.id==110)
    result = []
    for deck in decks:
        result.append(deck.serialize())
    if len(result) == 0:
        return jsonify(False, {"message": "There are no decks"})
    return jsonify(result)





# DELETE
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):

        d = Deck.query.get_or_404(id)

        try:
                session.delete(d)
                session.commit()
                stmt = sqlalchemy.delete(game_deck_table).where(deck_id = d.id)
                session.execute(stmt)
                stmt2 = sqlalchemy.delete(deck_cards_table).where(deck_id = d.id)
                session.execute(stmt2)
                return jsonify(True)
        except:
                jsonify(False, {"message":"Something went wrong with Deck Delete"})

