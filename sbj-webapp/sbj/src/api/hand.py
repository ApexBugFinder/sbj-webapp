# import sqlalchemy
from flask import Blueprint, jsonify, abort, request
from flask_cors import CORS
from sbj.src.models.card import Card
from sbj.src.models.game import Game
from sbj.src.models.player import Player
from sbj.src.models.hand import Hand
from sbj.src.models.handcards import hand_cards_table
from sbj.src.models.players_hand import players_hand_table
import sqlalchemy
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

bp = Blueprint('hands', __name__, url_prefix='/api/hands')
CORS(bp)

# CREATE
@bp.route('/create', methods=['POST'])
def createHand():
        new_hand = None
        if 'user.id' in request.json:
                player_query = session.query(Player).filter(Player.id == request.json['user.id'])
                u = None
                for record in player_query:
                        u = record.serialize()
                new_hand = Hand(lim=u.limit)

        if 'game.id' in request.json:
                game_query = session.query(Game).filter_by(Game.id == request.json['game.id'])
                g = None
                for record in game_query:
                        g = record.serialize()
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

        # QUERY HAND:
        q_hand = session.query(Hand).filter(Hand.id == id)
        hand = None
        for record in q_hand:
                hand: Hand = record.serialize()
                print(record.serialize())

        # QUERY CARDS ALREADY IN HAND:
        cards_already_in_hand = []
        cards_already_in_hand_query = session.query(hand_cards_table).filter(hand_cards_table.c.hand_id ==id)
        for record in cards_already_in_hand_query:
                cardInfo = record['card_id']
                card_info_query = session.query(Card).filter(Card.id == cardInfo)
                for record in card_info_query:
                        cards_already_in_hand.append(record.serialize())

        # QUERY INCOMING CARDS AND ADD TO HAND CARDS TABLE:
        incoming_cards = []

        for record in request.json:
                p = session.query(Card).filter(Card.id==record['card.id'])
                c = None
                for q_rec in p:
                        c:Card = q_rec.serialize()
                        incoming_cards.append(c)
                        insert_card_stmt = hand_cards_table.insert().values(
                                hand_id=hand.id, card_id=c.id
                        )
                        session.execute(insert_card_stmt)
        print('CARDS IN HAND ALREADY: ', cards_already_in_hand)
        print('CARDS TO ADD: ', incoming_cards)

        # CREATE RET OBJECT and UPDATED HAND & CARDS
        all_cards =  []
        all_cards.append(cards_already_in_hand)
        all_cards.append(incoming_cards)
        hand.add_to_hand(all_cards)

        #
        rt = dict()
        rt['hand'] = hand.serialize()
        rt['cards'].append(all_cards)


        # INSERT INTO hand_cards_table




        try:
                return jsonify(rt)
        except:
                return jsonify(False)



# UPDATE
@bp.route('/<int:id>', methods=['PUT'])
def update(id: int):
        try:
                q_hand = session.query(Hand).filter(Hand.id == id)
                hand = None
                for record in q_hand:
                        hand: Hand = record.serialize()
                        print(record.serialize())

                if 'status' in request.json:
                        hand.status = request.json['status']

                if 'player_limit' in request.json:
                        hand.player_limit = request.json['player_limit']

                if 'user.id' in request.json:
                        hand.user_id  = request.json['user.id']

                if 'game.id' in request.json:
                        hand.game_id = request.json['game.id']


                session.add(hand)
                session.commit()
                return jsonify(hand.serialize())
        except:
                return jsonify(False, {"message": "Something went wrong updating hand"})


# DELETE
@bp.route('/delete/<int:id>', methods =  ['DELETE'])
def delete(id: int):
        q_hand = session.query(Hand).filter(Hand.id == id)
        hand = None
        for record in q_hand:
                hand: Hand = record.serialize()
                print(record.serialize())

        try:
                session.delete(hand)
                session.commit()
        except:
                return jsonify(False, {"message": "Something went wrong with deleting your hand"})



