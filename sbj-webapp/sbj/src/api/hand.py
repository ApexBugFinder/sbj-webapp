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
from sqlalchemy import create_engine, select, join, insert, update
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo=True)

Sesson = sessionmaker(bind=engine, autoflush=True)
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
        with Sesson() as session:
                new_hand = None
                print('HELLLLLLLLOOOOOooo:', request.json)
                gid = request.json['game.id']
                pid = request.json['user.id']
                u: Player = None
                if 'user.id' in request.json:
                        print('user id in json request:   ',pid)
                        player_query = session.query(Player).filter(Player.id == pid)

                        for record in player_query:
                                u = record
                                print(u.serialize())
                        if u:
                                print(u)
                                new_hand = Hand(lim=u.limit)
                                print(new_hand.serialize())





                try:
                        print('POINT  >>>>>>>>>>>>>>>>>>2')
                        # session.close()
                        # session.begin()
                        # session.begin()
                        # session.refresh()
                        print('POINT >>>>>>>>>>>>>>>>>>>3')
                        session.add(new_hand)
                        session.flush()
                        # session.close()

                        # insert_handstmt = sqlalchemy.insert(Hand).values(
                        #         player_limit=new_hand.player_limit,
                        #         status=new_hand.status,
                        #         h_value=new_hand.h_value,
                        #         l_value=new_hand.l_value)
                        # p = session.execute(insert_handstmt)
                        print('POINT >>>>>>>>>>>>>>>>>>>>>4')

                        # session.commit()
                        # session.refresh()
                        # session.begin()


                        print('POINT >>>>>>>>>>>>>>>5',new_hand.id)

                        insert_player_stmt = sqlalchemy.insert(players_hand_table).values(
                        hand_id=new_hand.id,  player_id=u.id
                        )
                        print(insert_player_stmt)
                        result = session.execute(insert_player_stmt)


                        print('Maid It')

                        session.flush()
                        session.commit()
                        new_hand.user_id = u.id;
                        new_hand.set_game_id(gid);
                        print(new_hand.serialize_plus_userid_gameid())
                        ret = new_hand.serialize_plus_userid_gameid()

                        session.close()

                        print(ret);
                        return jsonify(ret)
                except:
                        print('ERROR')
                        session.rollback()
                        session.close()
                        return jsonify(False, {'message': 'Something went wrong'})



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
                        a = None

                        for record in h:
                                rt.append(record.serialize())
                                a = record

                        return jsonify(a.serialize())
                except:

                        return jsonify({"message": "Show Hand by ID method failed"})




# READ HaND INFO BY ID
@bp.route('/read/cards/<int:id>', methods=['GET'])
def read_handcards(id: int):
        try:
                join_stmt = hand_cards_table.join(Card).join(Hand)
                select_stmt = select([Hand, hand_cards_table, Card ]).select_from(join_stmt)
                filter_stmt = select_stmt.filter(hand_cards_table.c.hand_id==id)

                a = { "cards": []}
                i=0
                result = session.execute(filter_stmt)
                for record in result:
                        i=1+i
                        a["hand"]=record['Hand'].serialize()
                        a["cards"].append(record['Card'].serialize())


                print(a)

                return jsonify(a)
        except:

                return jsonify({"message": "Show Hand Information by ID method failed"})




# GET HAND INFO OF PLAYER AND CARD
@bp.route('/read/info/<int:id>', methods=['GET'])
def get_handinfo_by_id(id:int):
        print('===============================================HAND --- GET HAND INFO=============================')
        j = hand_cards_table.join(Hand).join(Card).join(players_hand_table, players_hand_table.c.hand_id==hand_cards_table.c.hand_id).join(Player, Player.id==players_hand_table.c.player_id)
        select_stmt = select([Player,players_hand_table, Hand, hand_cards_table, Card]).select_from(j)
        filter_stmt = select_stmt.filter(Hand.id == id)
        result = session.execute(filter_stmt)
        rt = []
        a = {"cards": {}}
        i=0
        for record in result:
                i=i+1
                print(record)
                if (record['Hand']):
                        print(record['Hand'].serialize())
                        a["hand"]=record['Hand'].serialize()
                if (record['Player']):
                        print(record['Player'].serialize())
                        a["player"]=record['Player'].serialize()
                if (record['Card']):
                        print(record['Card'].serialize())
                        a["cards"][i]=record['Card'].serialize()
                rt.append(a)
        print('========================================RETURN OF HAND INFO++++++++++++++==============')
        print(rt)
        print(a)
        try:

                return jsonify(rt[0])
        except:

                return jsonify(False)

# ADD TO HAND
@bp.route('/add_to_hand/<int:id>', methods=['PUT'])
def add_to_hand(id: int):
        all_cards = []
        # QUERY HAND:
        q_hand = session.query(Hand).filter(Hand.id == id)
        hand = None
        for record in q_hand:
                hand = Hand(record.player_limit)
                hand.id =record.id
                hand.status = record.status
                hand.h_value = record.h_value
                print(record.l_value)
                hand.l_value = int(str(record.l_value))


                print('HANDCARDS WILL BE ADDED TO THIS HAND >>>',hand.serialize())

        # QUERY CARDS ALREADY IN HAND:
        cards_already_in_hand = []
        cards_already_in_hand_query = session.query(hand_cards_table).filter(hand_cards_table.c.hand_id ==id)
        for record in cards_already_in_hand_query:
                cardInfo = record['card_id']
                print('WOOOOOOO', record)
                card_info_query = session.query(Card).filter(Card.id == cardInfo)
                for record in card_info_query:
                        alreadyInHand = Card(record.face,record.suite, record.h_value, record.l_value, record.url )
                        alreadyInHand.id = record.id
                        print('WATCH THIS....\n\n')
                        print(alreadyInHand)
                        print(record)
                        cards_already_in_hand.append(record.serialize())
                        all_cards.append(record)

        # QUERY INCOMING CARDS AND ADD TO HAND CARDS TABLE:

        incoming_cards = []

        for record in request.json:
                print(record['card.id'])
                cardid = record['card.id']
                p = session.query(Card).filter(Card.id==cardid)
                c = Card()
                for q_rec in p:

                        c = Card(q_rec.face, q_rec.suite, q_rec.h_value, q_rec.l_value, q_rec.url)
                        c.id = q_rec.id
                        print('HELLLLLLO', q_rec.serialize())
                        print('HELLLLLLO', c.serialize())
                        print('HELLLLLLO', type(c.l_value))

                        incoming_cards.append(c)
                        all_cards.append(c)
                        print('HELLLLLLO', len(incoming_cards))
                        insert_card_stmt = hand_cards_table.insert().values(
                                hand_id=hand.id, card_id=c.id
                        )
                        session.execute(insert_card_stmt)
        print('CARDS IN HAND ALREADY: ', cards_already_in_hand)
        for record in incoming_cards:
                print('CARD TO ADD: ', record.serialize())
                print(type(record.l_value))

        # CREATE RET OBJECT and UPDATED HAND & CARDS

        print('PRINTING ALL CARDS BEFORE ADD: ', all_cards)

        hand.add_to_hand(all_cards)
        # for record in incoming_cards:
        #         print(record.face)
        #         all_cards.append(record)
        # hand.add_to_hand(all_cards)
        # print(hand.serialize())
        #
        rt = dict()
        rt['hand'] = hand.serialize()
        # rt['cards'].append(all_cards)







        try:

                return jsonify(hand.serialize())
        except:

                return jsonify(False)



# UPDATE
@bp.route('updatehandstatus/<int:id>', methods=['PUT'])
def updatehandstatus(id: int):
        try:
                q_hand = session.query(Hand).filter(Hand.id == id)
                hand = None
                for record in q_hand:
                        print('pulled from query: ', record.id)
                        hand = Hand(lim=record.player_limit)
                        hand.id = record.id
                        hand.player_limit = record.player_limit
                        hand.h_value = record.h_value
                        hand.l_value = int(str(record.l_value))
                        hand.status = record.status
                        print('reconstructed HAND>>>', hand.serialize())

                        print('UPDATE HAND STATUS HAND', hand.serialize())

                if 'status' in request.json:
                        hand.status = request.json['status']

                if 'player_limit' in request.json:
                        hand.player_limit = request.json['player_limit']




                update_stmt = update(Hand).where(hand.id == hand.id).values(
                        status = hand.status, player_limit = hand.player_limit,
                )
                session.execute(update_stmt)
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

                return jsonify(True)
        except:

                return jsonify(False, {"message": "Something went wrong with deleting your hand"})



