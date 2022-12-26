import sqlalchemy
from flask import Blueprint, jsonify, abort, request
from ..models import Game, GameStatus, Player, db

bp = Blueprint('games', __name__, url_prefix='/games')

# CREATE
@bp.route('create_game', methods=['POST'])
def create():
        if 'player.id' not in request.json:
                return abort(400, 'player not in request json')
        elif 'dealer.id' not in request.json:
                return abort(400, 'dealer not in request.json')
        else:
                player = Player.query.get_or_404(request.json['player.id'])
                dealer = Player.query.get_or_404(request.json['dealer.id'])
                players = {"player": player, "dealer": dealer}
                new_game = Game(players)
                try:
                        db.session.add(new_game)
                        db.session.commit()
                        return jsonify(new_game.serialize())
                except:
                        return jsonify(False)

# GET ALL
@bp.route('', methods=['GET'])
def index():
        games = Game.query.all()
        result = []
        for game in games:
                result.append(game.serialize())
        if len(games)== 0:
            return jsonify(False,{'message':'No games yet, Sorry'})
        return jsonify(result)



# GET BY ID
@bp.route('/<int:id>', methods=['GET'])
def get_by_id(id: int):
        g = Game.query.get_or_404(id)

        return jsonify(g.serialize())


# UPDATE
@bp.route('/update/<int:id>', methods=['PUT'])
def update(id:int):
                g = Game.query.get_or_404(id)

                if 'game_status' in request.json:
                        g.game_status = request.json['game_status']


# DELETE
@bp.route('/delete/</int:id>', methods=['DELETE'])
def delete(id:int):
                g = Game.query.get_or_404(id)

                try:
                        db.session.delete(g)
                        db.session.commit()
                        return jsonify(True)
                except:
                        return jsonify(False, {"message": "Something went wrong deleting game"})