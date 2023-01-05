# import sqlalchemy
from flask import Blueprint, jsonify, abort, request
from sbj.src.models.card import Card
from sbj.src.models.hand import Hand
from sbj.src.models.player import Player
from sbj.src.models.game import Game

from sbj.src.dbObjects.handcards import hand_cards_table
from sbj.src.dbObjects.players_hand import players_hand_table
from ...wsgi import db
bp = Blueprint('hands', __name__, url_prefix='/hands')


# CREATE
@bp.route('/create', methods=['POST'])
def createHand():
        new_hand = None
        if 'user.id' in request.json:
                u = Player.query.get_or_404(request.json['user.id'])
                new_hand = Hand(lim=u.limit)

        if 'game.id' in request.json:
                g = Game.query.get_or_404(request.json['game.id'])
                new_hand.set_game_id(g.id)

        if 'cards' in request.json:
                handcards_init =[]
                for card in request.json['cards']:
                        newCard = Card(
                                id = card['id'],
                                face = card['face'],
                                suite = card['suite'],
                                value = card['h_value'],
                                h_value = card['h_value'],
                                l_value = card['l_value'],
                                url = card['url'],
                                deck_id = card['deck_id']
                                )

                        handcards_init.append(newCard)
                new_hand.add_to_hand(handcards_init)
        try:
                db.session.add(new_hand)
                db.session.commit()
                for card in new_hand.cards:
                        stmt = sqlalchemy.insert(hand_cards_table).values(hand_id=new_hand.id, card_id=card.id)
                        db.session.execute(stmt)
                return jsonify(new_hand.serialize())
        except:
                return jsonify(False)

# READ ALL
@bp.route('', methods=['GET'])
def index():
        records = Hand.query.all()
        result = []
        for record in records:
                result.append(record.serialize())
        if len(records)== 0:
                return jsonify(False,{'message':'No Hands yet, Sorry'})
        return jsonify(result)


# READ BY ID
@bp.route('/<int:id>', methods=['GET'])
def read_by_id(id: int):
                h = Hand.query.get_or_404(id)
# help needed my docker is dead
                return jsonify(h.serialize())

@bp.route('/get_cards/<int:id>', methods=['GET'])
def get_hand_cards(id:int):
        hand = Hand.query.all()
        j = Player.join(players_hand_table).join(Hand).join(hand_cards_table).join(Card)
        stmt = select([Player,players_hand_table, Hand, hand_cards_table, Card]).select_from(j).filter(Player.c.id)
        try:
                return jsonify(True)
        except:
                return jsonify(False)
# UPDATE
@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
        h = Hand.query.get_or_404(id)

        if 'status' in request.json:
                h.status = request.json['status']

        if 'player_limit' in request.json:
                h.player_limit = request.json['player_limit']

        if 'user.id' in request.json:
                h.user_id  = request.json['user.id']

        if 'game.id' in request.json:
                h.game_id = request.json['game.id']

        try:
                db.session.add(h)
                db.session.commit()
                return jsonify(True)
        except:
                return jsonify(False)

# DELETE
@bp.route('/delete/<int:id>', methods =  ['DELETE'])
def delete(id: int):
        h = Hand.query.get_or_404(id)

        try:
                db.session.delete(h)
                db.session.commit()
        except:
                return jsonify(False, {"message": "Something went wrong with deleting your hand"})



