
from flask import Blueprint, jsonify, abort, request
from flask_cors import CORS
from sbj.src.models.game import Game
from sbj.src.models.player import Player
from sbj.src.models.gameplayers import game_players_table
from flask_cors import CORS, cross_origin
# from db import db
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy
engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo=True)

Sesson = sessionmaker(bind=engine)
session = Sesson()

bp = Blueprint('games', __name__, url_prefix='/api/games')
CORS(bp)
# CREATE


@bp.route('/create_game', methods=['POST', 'GET'])
def create():
    pid = request.json['player.id']
    did = request.json['dealer.id']
    if pid == 1 or did == 1:
            return jsonify(False)
    else:

        if 'player.id' not in request.json:
            return abort(400, 'Player ID is not in request.json')
        elif 'dealer.id' not in request.json:
            return abort(400, 'Dealer ID is not in request.json')
        else:
            # Collect IDs
            pid = request.json['player.id']
            did = request.json['dealer.id']

            # GET PLAYER
            p = session.query(Player).filter(Player.id==pid).limit(1)
            player:Player = None
            print('HEEEEEEEEEEEEEEEEEEEEE', p)

            for record in p:
                    print(record)
                    player  = record

            # GET DEALER
            d = session.query(Player).filter(Player.id==did).limit(1)
            dealer:Player = None
            for record in d:
                dealer = record


            players = {"player": player, "dealer": dealer}
            print('DEALER in NEW GAME:', dealer.serialize())
            new_game = Game(players)
            new_game.setplayerId(id=player.id)
            new_game.setdealerId(id=dealer.id)
            print('NEW GAME UPDATED BY PLAYERS: ', new_game.serialize())
            try:

                session.add(new_game)
                session.commit()
                session.begin()


                print('NEW game COMMITTTTED: ', new_game.serialize())
                insert_player = game_players_table.insert().values(game_id=new_game.id,  player_id=new_game.player_id)


                print(insert_player)
                session.execute(insert_player)


                insert_dealer = game_players_table.insert().values(game_id=new_game.id, player_id=new_game.dealer_id)
                session.execute(insert_dealer)



                return jsonify(new_game.serialize_w_users())
            except:
                session.rollback()
                return jsonify(False)

# GET ALL
@bp.route('/show_all', methods=['GET'])
def index():
    games = session.query(Game).all()

    result = []
    for game in games:
        result.append(game.serialize())
    if len(games) == 0:

        return jsonify(False, {'message': 'No games yet, Sorry'})

    return jsonify(result)


# GET BY ID
@bp.route('/read/<int:id>', methods=['GET'])
def get_by_id(id: int):

    query = session.query(Game).filter(Game.id == id)
    g = None
    for record in query:
        g = record.serialize()
    print(g)
    try:
        j = Game.join(game_players_table, Game.c.id == game_players_table.c.game_id).join(Player, game_players_table.c.player_id == Player.c.id)

        stmt = select([Game, game_players_table, Player]).select_from(j).filter(Game.id ==g.id)
        results = session.execute(stmt)
        session.commit()
        rt = []
        for rec in results:
                print(rec)
                a = {
                    "game.id": rec['id'],
                    "started_at": rec['started_at'],
                    "game_status": rec['game_status'],
                    "finished_at": rec['finished_at'],

                }
                rt.append(a)

        return jsonify(rt)
    except:
        session.rollback()
        return jsonify(False, {"message": "Operation failed to read game information"})



# UPDATE
@bp.route('/update/<int:id>', methods=['PUT'])
def update(id: int):

        query = session.query(Game).filter(Game.id == id)
        g = None
        for record in query:
            g = record.serialize()
        print(g)

        try:
            if 'game_status' in request.json:
                g.game_status = request.json['game_status']
            else:
                abort(400, "Game Status is a required and only field you can update")

            session.add(g)
            session.commit()

            return jsonify(g)
        except:
            session.rollback()
            return jsonify(g, {"message": "Update failed"})

# DELETE
@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete(id: int):

        query = session.query(Game).filter(Game.id == id)
        g = None
        for record in query:
            g = record.serialize()
        print(g)

        try:
            session.delete(g)
            session.commit()

            return jsonify(True)
        except:
            session.rollback()
            return jsonify(False, {"message": "Something went wrong deleting game"})
