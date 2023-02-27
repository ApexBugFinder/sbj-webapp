from flask import Blueprint, jsonify, abort, request
from flask_cors import CORS
from sbj.src.models.player import Player

from sbj.db import db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql://qitqsyhs:OTaHwkfOkI2eAyjAm4LCmabNUjk6kfMd@mahmud.db.elephantsql.com/qitqsyhs', echo=True)

Sesson = sessionmaker(bind=engine)
session = Sesson()

bp = Blueprint('players', __name__, url_prefix='/api/players')
CORS(bp)


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
                session.rollback()
                return jsonify(False, {'message': 'Something went wrong'})

# READ ALL
@bp.route('/show_all', methods=['GET'])
def index():
        players = session.query(Player).all()
        result = []
        for player in players:
                result.append(player.serialize())

        if len(players) == 0:

                return jsonify(False, {'message': 'No players yet, Sorry'})

        return jsonify(result)

#  READ by id



@bp.route('/read/<int:id>', methods=['GET'])
def read_by_id(id: int):
        records = session.query(Player).filter(id = id)
        results = []
        for record in records:
                results.append(record.serialize())


        return jsonify(results[0])

# READ BY Name



@bp.route('/read_by_name/<username>', methods=['GET'])
def read_by_name(username:str):
        try:
                results = []

                players = session.query(Player).filter(Player.name==username).limit(1)
                print ('USERNAME: ', username)
                for record in players:
                        print('HELL')
                        results.append(record.serialize())

                print(results[0])
                if len(results) == 0:

                        abort(400, {'message': 'Username does not exist'})


                return jsonify(results[0])

        except:
                session.rollback()
                return abort(400,  'Something definitely went wrong')

# UPDATE
@bp.route('/update/<int:id>', methods=['PUT'])
def update(id: int):

        q = session.query(Player).filter(id=id).limit(1)
        aplayer = None
        for record in q:
                aplayer = record.serialize()
        #  User name is being updated
        if aplayer == None:

                abort(400 , "User does not exist")
        if 'name' in request.json:
                # Length of user name
                if len(request.json['name']) < 5:

                        abort(400, {'message': 'Username has to have 5 or more characters'})

                # Username update
                aplayer.name = request.json['name']

        # Limit is being updated
        elif 'limit' in request.json:
                if type(request.json['limit']) != int:

                        abort(400, {'message': 'Limit is incorrect type, it must be int'})
                # Limit is in range: not less than 0 and less than 21
                elif request.json['limit'] > 21 or request.json['limit'] < 0:

                        abort(400, {'message': 'Limit out of Range'})
                # Update Limit
                aplayer.limit = int(request.json['limit'])

        try:
                session.add(aplayer)
                session.commit()

                return jsonify(aplayer.serialize())
        except:
                session.rollback()
                return jsonify(False, {'message': f'Something went wrong updating {aplayer.id} '})


# DELETE
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):

        p = session.query(Player).where(Player.id == id).limit(1)
        result = []
        for player in p:
                result.append(player.serialize())
        if len(result) > 0:
                try:
                        session.delete(p)
                        session.commit()

                        return jsonify(True)
                except:
                        session.rollback()
                        return abort(400, f"Something went wrong deleting user {p.id}")
        else:
                session.rollback()
                return jsonify(False, {"message": "Player does not exist"})