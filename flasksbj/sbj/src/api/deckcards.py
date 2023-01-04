from flask import Blueprint, jsonify, abort, request
from ..models.deck import Deck
from ..models.card import Card
from ..models.deckcard import DeckCard
from ..dbObjects.deckcard import  deck_cards_table
from ..dbObjects.gamedeck import game_deck_table
game_deck_table
from ...wsgi import db
# from sqlalchemy import select,join

bp = Blueprint('deckcards', __name__, url_prefix='/deckcards')


# READ BY DECK ID

@bp.route('', methods=['GET'])
def get_all():
        dc = deck_cards_table.select()
        results = db.session.execute(dc)
        try:

                rt = []
                for row in results:
                        a = {
                                "deck.id": row['deck_id'],
                                "card.id": row['card_id'],
                                "used": row['used']
                        }
                        rt.append(a)
                return jsonify(rt)
        except:
                return jsonify(False, {"message": "Something went wrong with getting all deckcards"})


@bp.route('/<int:id>', methods=['GET'])
def get_deck_cards_by_deck_id(id: int):
    print(str(id))
    d = Deck.query.get_or_404(id)
    try:

        j = deck_cards_table.join(Card)
        stmt = select([deck_cards_table,Card]).select_from(j).filter(deck_cards_table.c.deck_id==d.id)


        print(stmt)
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
        return jsonify(False)
