
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
            return jsonify(True)
    else:

        if 'player.id' not in request.json:
            return abort(400, 'player id is not in request.json')
        elif 'dealer.id' not in request.json:
            return abort(400, 'dealer is not in request.json')
        else:
            # Collect IDs
            pid = request.json['player.id']
            did = request.json['dealer.id']

            # GET PLAYER
            p = session.query(Player).filter(Player.id==pid).limit(1)
            player = None

            for record in p:
                    print(p)
                    player  = record.serialize()

            # GET DEALER
            d = session.query(Player).filter(Player.id==did).limit(1)
            dealer = None
            for record in d:
                dealer = record.serialize()


            players = {"player": player, "dealer": dealer}
            new_game = Game(players)
            new_game.setplayerId(pid)
            new_game.setdealerId(did)
            print('NEW GAME STARTED AT: ', new_game.started_at)
            try:

                # insertstmt = sqlalchemy.insert(Game).values(
                #     game_status=new_game.game_status,
                #     started_at=new_game.started_at
                #     )


                session.add(new_game)
                session.commit()

                print('NEW game COMMITTTTED: ', new_game.serialize())
                insert_player = game_players_table.insert().values(game_id=new_game.id,  player_id=new_game.player_id)


                print(insert_player)
                session.execute(insert_player)


                insert_dealer = game_players_table.insert().values(game_id=new_game.id, player_id=new_game.dealer_id)
                session.execute(insert_dealer)

                session.commit()

                return jsonify(new_game.serialize())
            except:
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
    g = Game.query.get_or_404(id)
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
        return jsonify(False, {"message": "Operation failed to read game information"})



# UPDATE
@bp.route('/update/<int:id>', methods=['PUT'])
def update(id: int):
    g = Game.query.get_or_404(id)

    if 'game_status' in request.json:
        g.game_status = request.json['game_status']


# DELETE
@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete(id: int):
    g = Game.query.get_or_404(id)

    try:
        session.delete(g)
        session.commit()
        return jsonify(True)
    except:
        return jsonify(False, {"message": "Something went wrong deleting game"})
