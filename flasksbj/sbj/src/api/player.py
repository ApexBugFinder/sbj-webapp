from flask import Blueprint, jsonify, abort, request

from sbj.src.models.player import Player

from sbj.db import db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo=True)

Sesson = sessionmaker(bind=engine)
session = Sesson()

bp = Blueprint('players', __name__, url_prefix='/api/players')



# CREATE METHOD
@bp.route('/create', methods=['POST'])
def create():
        if 'name' not in request.json:
                return abort(400, {'message':'Username not included'})
        if len(request.json['name'])<=3:
                return abort(400, {'message': 'Username too short'})
        new_player = Player(
              name = request.json['name']
        )
        try:
              session.add(new_player)
              session.commit()
              return jsonify(new_player.serialize())
        except:
                return jsonify(False, {'message': 'Something went wrong'})

# READ ALL
@bp.route('/show_all', methods=['GET'])
def index():
        players = Player.query.all()
        result = []
        for player in players:
                result.append(player.serialize())
        if len(players) == 0:
                return jsonify(False, {'message': 'No players yet, Sorry'})
        return jsonify(result)

#  READ by id
@bp.route('read/<int:id>', methods=['GET'])
def read_by_id(id: int):
        p = Player.query.get_or_404(id)
        return jsonify(p.serialize())

# READ BY Name
@bp.route('read_by_name/<string:username>', methods=['GET'])
def read_by_name(username:str):
        try:
                results = []
                print ('USERNAME: ', username)
                players = session.query(Player).filter_by(name =username).limit(1)
                a = None
                for record in players:
                        print(record.serialize())
                        a = record.serialize()
                        results.append(record.serialize())

                return a
                # if len(results) ==0:
                #         return jsonify(False, {'message': 'Sorry, Player does not exist'})
                # else:
                #         return jsonify(results)
        except:
                                return jsonify(False, {'message': 'Something went wrong'})

# UPDATE
@bp.route('update/<int:id>', methods=['PUT'])
def update(id: int):
        player = Player.query.get_or_404(id)

        #  User name is being updated
        if 'name' in request.json:
                # Length of user name
                if len(request.json['name']) < 5:
                        abort(400, {'message': 'Username has to have 5 or more characters'})

                # Username update
                player.name = request.json['name']

        # Limit is being updated
        elif 'limit' in request.json:
                if type(request.json['limit']) != int:
                        abort(400, {'message': 'Limit is incorrect type, it must be int'})
                # Limit is in range: not less than 0 and less than 21
                elif request.json['limit'] > 21 or request.json['limit'] < 0:
                        abort(400, {'message': 'Limit out of Range'})
                # Update Limit
                player.limit = int(request.json['limit'])

        try:
                session.add(player)
                session.commit()
                return jsonify(player.serialize())
        except:
                return jsonify(False, {'message': f'Something went wrong updating {player.id} '})


# DELETE
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):
        p = Player.query.get_or_404(id)
        p = session.query(Player).where(Player.id == id)
        result = []
        for player in p:
                result.append(player.serialize())
        if len(result) > 0:
                try:
                        session.delete(p)
                        session.commit()
                        return jsonify(True)
                except:
                        return jsonify(False, {'message':f'Something went wrong deleting user {p.id}'})
        else:
                return jsonify(False, {"message": "Player does not exist"})