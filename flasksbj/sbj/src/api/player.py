# import sqlalchemy
from flask import Blueprint, jsonify, abort, request

from ..models.player import Player
from ...wsgi import db

bp = Blueprint('players', __name__, url_prefix='/players')




@bp.route('create', methods=['POST'])
def create():
        if 'name' not in request.json:
                return abort(400, {'message':'Username not included'})
        if len(request.json['name'])<=3:
                return abort(400, {'message': 'Username too short'})
        new_player = Player(
              name = request.json['name']
        )
        try:
              db.session.add(new_player)
              db.session.commit()
              return jsonify(new_player.serialize())
        except:
                return jsonify(False, {'message': 'Something went wrong'})

# READ ALL
@bp.route('', methods=['GET'])
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

                players = db.session.query(Player).filter_by(name =username).limit(1)

                for record in players:
                      print(record.serialize())
                      results.append(record.serialize())


                if len(results) ==0:
                        return jsonify(False, {'message': 'Sorry, Player does not exist'})
                else:
                        return jsonify(results)
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
                db.session.add(player)
                db.session.commit()
                return jsonify(player.serialize())
        except:
                return jsonify(False, {'message': f'Something went wrong updating {player.id} '})


# DELETE
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):
          p = Player.query.get_or_404(id)

          try:
                    db.session.delete(p)
                    db.session.commit()
                    return jsonify(True)
          except:
                    return jsonify(False, {'message':f'Something went wrong deleting user {p.id}'})
