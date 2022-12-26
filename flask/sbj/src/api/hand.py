import sqlalchemy
from flask import Blueprint, jsonify, abort, request
from ..models import Hand, Player, Game, Card, db, hand_cards_table

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

                return jsonify(h.serialize())


