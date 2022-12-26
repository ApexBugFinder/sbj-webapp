import sqlalchemy
from flask import Blueprint, jsonify, abort, request
from ..models import Deck, db, deck_cards_table, Card, DeckCard, game_deck_table
from sqlalchemy import insert,select

bp = Blueprint('decks', __name__, url_prefix='/decks')


@bp.route('', methods=['GET'])
def index():
        decks = Deck.query.all()
        result = []
        for deck in decks:
                result.append(deck.serialize())
        if len(decks)== 0:
            return jsonify(False)
        return jsonify(result)


@bp.route('create', methods=['POST'])
def create_deck():
        if 'game.id' in request.json:
                game_id = request.json['game.id']
        new_deck = Deck()
        db.session.add(new_deck)
        db.session.commit()
        deckofcards = Card.query.all()
        doc = []
        for card in deckofcards:
                doc.append( DeckCard(card, new_deck.id))
        if len(doc) == 52:
                try:
                        stmt2 = sqlalchemy.insert(game_deck_table).values(game_id=game_id, deck_id=new_deck.id)
                        db.session.execute(stmt2)
                        db.session.commit()
                        for record in doc:
                                stmt = sqlalchemy.insert(deck_cards_table).values(card_id =record.id, deck_id =record.deck_id , used=False)
                                db.session.execute(stmt)
                                db.session.commit()

                        selectstmt = sqlalchemy.select(deck_cards_table).where(deck_id=new_deck.id)
                        myfulldeck = db.session.execute(selectstmt)
                        db.session.commit()
                        returnstmt = ''
                        for deckc in myfulldeck:
                                returnstmt += '{\n'+ deckc.serialize() +'\n},\n'


                        return jsonify(returnstmt)
                except:
                        return jsonify(False)


        return jsonify(new_deck.serialize())

@bp.route('/get-full-deck', methods=['GET', 'POST'])
def get_full_deck():
        new_deck = Deck()
        db.session.add(new_deck)
        db.session.commit()

        result = []
        cardsreturn = Card.query.all()
        for card in cardsreturn:
              card.set_deck_id(new_deck.id)
              print(card.serialize())
              print(card.deck_id)



        return jsonify(cardsreturn)
        # for card in cardsreturn:
        #       print(card)
        # deckreturn = create_deck()
        # for deck in deckreturn:
        #         new_deck = Deck(
        #           id=deck['id'], created_at=deck['created_at']
        #           )



# mydeck = create_deck()

# for deck in mydeck:
#       new_deck = Deck(id=deck['id'], created_at=deck['created_at'])
#       print(new_deck.serialize())
