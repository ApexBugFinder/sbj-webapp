from flask import Blueprint, jsonify, abort, request
from flask_cors import CORS
from sbj.src.models.deck import Deck
from sbj.src.models.card import Card
from sbj.src.models.deckcard import DeckCard
from  sbj.src.models.deckcard import  deck_cards_table
from  sbj.src.models.gamedeck import game_deck_table

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo=True)

Sesson = sessionmaker(bind=engine)
session = Sesson()

from sqlalchemy import select,join

bp = Blueprint('deckcards', __name__, url_prefix='/api/deckcards')
CORS(bp)

# READ BY DECK ID

@bp.route('', methods=['GET'])
def get_all():
        dc = deck_cards_table.select()
        results = session.execute(dc)
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


                session.rollback()
                return jsonify(False, {"message": "Something went wrong with getting all deckcards"})


# GET DECK CARDS BY DECK ID
@bp.route('/<int:id>', methods=['GET'])
def get_deck_cards_by_deck_id(id: int):
        print(str(id))

        try:
                print('IN TRY: ', id)
                j = deck_cards_table.join(Card).join(Deck, Deck.id==deck_cards_table.c.deck_id)
                c = select([deck_cards_table, Card]).select_from(j)


                print('POST QUERY: ', c)
                fil = c.filter(deck_cards_table.c.deck_id == id)
                print('POST FILTER', fil)
                res= session.execute(fil)
                result = []
                for record in res:
                        print(record)
                        print(record['Card'].serialize())
                        a = {
                                        "deck.id": record['deck_id'],
                                        "used": record['used'],
                                        "card": record['Card'].serialize()
                                }
                        result.append(a)

                print(result)


                return jsonify(result)

        except:


                session.rollback()
                return jsonify(False)


# PUT CHANGE DECKCARD USED
@bp.route('/change_to_usedpile', methods=['PUT'])
def change_to_used():
        try:
                if 'card.id' not in request.json:
                        return jsonify({"message": "Card id is not included in the request"})

                if 'deck.id' not in request.json:
                        return jsonify({"message":"Deck ID is not included in the request"})

                c = request.json['card.id']
                d = request.json['deck.id']
                print(c, d)
                p = session.query(deck_cards_table).filter(deck_cards_table.c.deck_id==d, deck_cards_table.c.card_id==c)


                for record in p:
                        print(record)
                        if not record['used']:

                                session.query(deck_cards_table).filter(deck_cards_table.c.deck_id == d, deck_cards_table.c.card_id == c).update(
                                        {deck_cards_table.c.used: True}, synchronize_session=False
                                )


                # REQUERY TO GET UPDATED VALUES & RETURn PRoof
                q = session.query(deck_cards_table).filter(deck_cards_table.c.deck_id == d, deck_cards_table.c.card_id == c)

                proof = {}
                for record in q:
                        print(record)
                        proof['card.id']=record['card_id']
                        proof['deck.id']=record['deck_id']
                        proof['used']=record['used']


                return jsonify(proof)
        except:
                session.rollback()
                return jsonify({"Message": "Something went wrong changing card to the used pile"})


# PUT CHANGE DECKCARD USED
@bp.route('/change_to_unused_pile', methods=['PUT'])
def change_to_unused():
        try:
                # GET THE IDs from the request.json for the deckcards
                if 'card.id' not in request.json:
                        return jsonify({"message": "Card id is not included in the request"})

                if 'deck.id' not in request.json:
                        return jsonify({"message": "Deck ID is not included in the request"})

                c = request.json['card.id']
                d = request.json['deck.id']
                print(c, d)
                p = session.query(deck_cards_table).filter(deck_cards_table.c.deck_id == d, deck_cards_table.c.card_id ==c)

                # UPDATE USED from TRUE TO FALSE
                for record in p:

                        if record['used']:
                        # if record is true set it to false
                                session.query(deck_cards_table).filter(deck_cards_table.c.deck_id == d, deck_cards_table.c.card_id == c).update(
                                {deck_cards_table.c.used: False}, synchronize_session=False
                                )

                # REQUERY TO GET UPDATED VALUES & RETURn PRoof
                q = session.query(deck_cards_table).filter(
                deck_cards_table.c.deck_id == d, deck_cards_table.c.card_id == c)

                proof = {}
                for record in q:

                        proof['card.id'] = record['card_id']
                        proof['deck.id'] = record['deck_id']
                        proof['used'] = record['used']

                return jsonify(proof)
        except:
                session.rollback()
                return jsonify({"Message": "Something went wrong changing card to the un-used pile"})