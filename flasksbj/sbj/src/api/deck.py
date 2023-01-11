from flask import Blueprint, jsonify, abort, request
from sbj.src.models.deck import Deck
from sbj.src.models.card import Card
from sbj.src.models.deckcard import DeckCard
from sbj.src.models.deckcard import deck_cards_table
from sbj.src.models.gamedeck import game_deck_table

from sbj.db import db
# from src.models.deck import Deck
# from src.models.card import Card
# from src.models.deckcard import DeckCard
# from src.models.deckcard import deck_cards_table
# from src.models.gamedeck import game_deck_table

import sqlalchemy
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
bp = Blueprint('decks', __name__, url_prefix='/decks')




# CREATE
@bp.route('/create', methods=['POST'])
def create_deck():

        if 'game.id' in request.json:
                game_id = request.json['game.id']
        new_deck = Deck()
        db.session.add(new_deck)
        db.session.commit()
        cardsQuery = Card.query.all()
        docs = []
        for card in cardsQuery:

                new_card = DeckCard(
                        card, deck_id=new_deck.id)
                print(new_card.serialize())
                docs.append(new_card)
        try:
                        stmt2 = sqlalchemy.insert(game_deck_table).values(
                                game_id=game_id, deck_id=new_deck.id)
                        db.session.execute(stmt2)

                        rt = []
                        for card in docs:
                                rt.append(card.serialize())
                                stmt = sqlalchemy.insert(deck_cards_table).values(deck_id=card.deck_id, card_id=card.id, used=False)
                                db.session.execute(stmt)


                        db.session.commit()
                        return jsonify(rt)


        except:
                return jsonify(False)

# READ BY ID
@bp.route('/read/<int:id>', methods=['GET'])
def get_by_id(id:int):
        d =Deck.query.get_or_404(id)
        try:
                j = deck_cards_table.join(Card)
                stmt = select([deck_cards_table, Card]).select_from(j).filter(deck_cards_table.c.deck_id == d.id)

                result = db.session.execute(stmt)
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
    decks = Deck.query.all()
    result = []
    for deck in decks:
        result.append(deck.serialize())
    if len(decks) == 0:
        return jsonify(False)
    return jsonify(result)


# UPDATE
# N/A   N/A     N/A


# DELETE
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):

        d = Deck.query.get_or_404(id)

        try:
                db.session.delete(d)
                db.session.commit()
                stmt = sqlalchemy.delete(game_deck_table).where(deck_id = d.id)
                db.session.execute(stmt)
                stmt2 = sqlalchemy.delete(deck_cards_table).where(deck_id = d.id)
                db.session.execute(stmt2)
                return jsonify(True)
        except:
                jsonify(False, {"message":"Something went wrong with Deck Delete"})

