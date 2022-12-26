import sqlalchemy
from flask import Blueprint, jsonify, abort, request
from ..models import Deck, db, deck_cards_table, Card, DeckCard, game_deck_table
from sqlalchemy import insert, select

bp = Blueprint('decks', __name__, url_prefix='/decks')




# CREATE
@bp.route('create', methods=['POST', 'GET'])
def create_deck():

        if 'game.id' in request.json:
                game_id = request.json['game.id']
        new_deck = Deck()
        db.session.add(new_deck)
        db.session.commit()
        try:
                        stmt2 = sqlalchemy.insert(game_deck_table).values(
                                game_id=game_id, deck_id=new_deck.id)
                        db.session.execute(stmt2)



                        return jsonify(new_deck.serialize())


        except:
                return jsonify(False)

# READ BY ID
@bp.route('/<int:id>', methods=['GET'])
def get_by_id(id:int):
        d =Deck.query.get_or_404(id)

        return jsonify(d.serialize())

# READ ALL
@bp.route('', methods=['GET'])
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
                return jsonify(True)
        except:
                jsonify(False, {"message":"Something went wrong with Deck Delete"})

