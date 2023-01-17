# import sqlalchemy
from flask import Blueprint, jsonify, abort, request

from sbj.src.models.card import Card
from sbj.src.models.game import Game
from sbj.src.models.player import Player
from sbj.src.models.hand import Hand
from sbj.src.models.handcards import hand_cards_table
from sbj.src.models.players_hand import players_hand_table

from sqlalchemy import create_engine, select, join
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo=True)

Sesson = sessionmaker(bind=engine)
session = Sesson()

# from src.models.card import Card
# from src.models.game import Game
# from src.models.player import Player
# from src.models.hand import Hand
# from src.models.handcards import hand_cards_table
# from src.models.players_hand import players_hand_table

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
                session.add(new_hand)
                session.commit()
                for card in new_hand.cards:
                        stmt = sqlalchemy.insert(hand_cards_table).values(hand_id=new_hand.id, card_id=card.id)
                        session.execute(stmt)
                return jsonify(new_hand.serialize())
        except:
                return jsonify(False)
# # ADD CARDS TO HAND
# @bp.route('/add/<int:id>', methods=['POST'])
# def addtohands(id: int):
#        # 1. Query Hand
#        h = session.query(Hand).where(Hand.id==id)
# #        .first_or_404()

#        # 2. Add cards to hand
#         data = request.json.dumps
#         for record in data:
#                 newHand = Hand(record['player_limit'], userid=record['userid'])


# READ ALL
@bp.route('/read/show_all', methods=['GET'])
def index():

        try:

                records = session.query(Hand).all()
                result = []
                for record in records:
                        print(record.serialize())
                        result.append(record.serialize())
                if len(records)== 0:
                        return jsonify(False,{'message':'No Hands yet, Sorry'})
                return jsonify(result)
        except:
                return jsonify({"message": "Show all Hands method failed"})

# READ BY ID
@bp.route('/read/<int:id>', methods=['GET'])
def read_by_id(id: int):

                try:
                        h = session.query(Hand).filter(Hand.id == id)
                        rt = []


                        for record in h:
                                rt.append(record.serialize())
                        return jsonify(rt)
                except:
                        return jsonify({"message": "Show Hand by ID method failed"})




# READ HaND INFO BY ID
@bp.route('/read/cards/<int:id>', methods=['GET'])
def read_handcards(id: int):
        try:
                join_stmt = hand_cards_table.join(Card).join(Hand)
                select_stmt = select([Hand, hand_cards_table, Card ]).select_from(join_stmt)
                filter_stmt = select_stmt.filter(hand_cards_table.c.hand_id==id)

                a = { "cards": {}}
                i=0
                result = session.execute(filter_stmt)
                for record in result:
                        i=1+i
                        a["hand"]=record['Hand'].serialize()
                        a["cards"][i]=record['Card'].serialize()


                print(a)
                return jsonify(a)
        except:
                return jsonify({"message": "Show Hand Information by ID method failed"})




# GET HAND INFO OF PLAYER AND CARD
@bp.route('/read/info/<int:id>', methods=['GET'])
def get_handinfo_by_id(id:int):

        j = hand_cards_table.join(Hand).join(Card).join(players_hand_table, players_hand_table.c.hand_id==hand_cards_table.c.hand_id).join(Player, Player.id==players_hand_table.c.player_id)
        select_stmt = select([Player,players_hand_table, Hand, hand_cards_table, Card]).select_from(j)
        filter_stmt = select_stmt.filter(Hand.id == id)
        result = session.execute(filter_stmt)
        rt = []
        a = {"cards": {}}
        i=0
        for record in result:
                i=i+1
                a["player"]=record['Player'].serialize()
                a["hand"]=record['Hand'].serialize()
                a["cards"][i]=record['Card'].serialize()
                rt.append(a)

        print(a)
        try:
                return jsonify(rt[0])
        except:
                return jsonify(False)

# ADD TO HAND
@bp.route('/add_to_hand/<int:id>', methods=['PUT'])
def add_to_hand(id: int):
        # QUERY CARDS:
        cards = []
        for record in request.json:
                print(record['card.id'])

                p = session.query(Card).filter(Card.id==record['card.id'])
                c = None
                for q_rec in p:
                        c=q_rec.serialize()
                        cards.append(c)
                        print(c)
        print('CARDS TO ADD: ', cards)

        # QUERY HAND:
        q_hand = session.query(Hand).filter(Hand.id ==id)
        hand=None
        for record in q_hand:
                print(record.serialize())
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
                session.add(h)
                session.commit()
                return jsonify(True)
        except:
                return jsonify(False)


# DELETE
@bp.route('/delete/<int:id>', methods =  ['DELETE'])
def delete(id: int):
        h = Hand.query.get_or_404(id)

        try:
                session.delete(h)
                session.commit()
        except:
                return jsonify(False, {"message": "Something went wrong with deleting your hand"})



